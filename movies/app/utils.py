# from src.models.movies import Movie
# import src.models.movies as m

from app.models import Movie
from app import db

import logging as lg 


def test_intersection(set_a, set_b):
    intersection = set_a.intersection(set_b) 
    return intersection == set_a



def get_movie_year_by_name(movie_name, Movie):
    movies = Movie.query.filter(Movie.name == movie_name).all()
    movie = movies[0]
    return str(movie.year)

def get_movies():
    movies = Movie.query.all()
    movies = [m.serialize() for m in movies]
    return movies

def get_movie(movie_id):
    movie = db.session.query(Movie).get(movie_id)
    # return movie.serialize()
    return movie




def add_movie(movie_name, year):
    movie = Movie(movie_name, year)
    db.session.add(movie)
    db.session.commit()
    # movies = Movie.query.filter(Movie.id == movie.id)
    # return db.session.query(Movie).get(movie.id).serialize()
    return db.session.query(Movie).get(movie.id)




def delete_movie_by_id(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).first()
    db.session.delete(movie)
    db.session.commit()

def update_movie_by_id(movie_id,movie_name,movie_year):
    x = db.session.query(Movie).get(movie_id)
    x.name = movie_name
    x.year = movie_year
    db.session.commit()
    # return x.serialize()
    return x
