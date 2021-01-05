from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class Tracks(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    artists = DB.Column(DB.String, nullable=False)
    name = DB.Column(DB.String, nullable=False)


def __repr__(self):
    return f'<Record: {self.name}>'