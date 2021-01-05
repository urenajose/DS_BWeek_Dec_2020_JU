from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import process
import numpy as np
import pandas as pd
import pickle
from models import DB, Tracks
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reco_tracks.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DB.init_app(app)


spotify = pd.read_csv('./csv/spotify_tracks.csv')
spotify_matrix = np.loadtxt("./csv/spotify_matrix.csv", delimiter=",")
# spotify numpy.array with standardize data

filename = './csv/spotify_track_neighbors.urenaj'
model_knn = pickle.load(open(filename, 'rb'))
# pickle spotify model NearestNeighbors

@app.route("/hello")
@app.route("/", methods=["GET","POST"])
def song_recomender():
    if request.method == "POST":
        DB.create_all()
        print(request.form)
        name_song = request.form.get("ssong")
        id_track = process.extractOne(name_song, spotify['name'])[2]
        print('Song selected', spotify['name'][id_track], 'id:', id_track)
        print('searching for recomendation....')
        # extracting the index numbers (rows) from the model
        distances, ids = model_knn.kneighbors(spotify_matrix[[id_track]], 
                                              n_neighbors=20)
        # extracting the list of the matrix, and creating a list of list.
        spotify_ids = list(ids[0])
        # creating a df with index return and desire columns
        recomendation = spotify[['artists', 'name', 'id']].loc[spotify_ids]
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
        recomendation
        recomendation.to_sql('tracks', con=engine, if_exists="replace", index=False)
        return redirect("/TracksReco")
    else:
        return render_template('form.html')

@app.route("/TracksReco")
def TracksReco():
    tracks = Tracks.query.all()
    return render_template('reco.html', tracks=tracks)

@app.route('/refresh')
def reset():
    DB.drop_all()
    return render_template('refresh.html', title='reset')


if __name__ == "__main__":
    app.run()