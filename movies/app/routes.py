from app import application
from flask import Flask, render_template
from flask import jsonify, make_response
from flask import request, abort
import logging as lg 
import requests
from config import Config

import app.utils as ut

# url_eval = "http://127.0.0.1:5001"
# url_eval = Config.url_eval
@application.route('/movies/all', methods=['GET'])
@application.route('/movies', methods=['GET'])
@application.route('/movies/', methods=['GET'])
@application.route('/', methods=['GET'])

def all_movies():
    """
    Returns all movie  in the database for Movies
    service
    """
    movies = ut.get_movies()
    if len(movies) == 0:
        abort(404)
    return make_response(jsonify({"movies":movies}),200)


@application.route('/movies/<movie_id>', methods=['GET'])
def movie(movie_id):
    """
    Returns a movie  given a movie id 
    :param movie_id:
    :return: A Movie
    """
    movie = ut.get_movie(movie_id)
    if movie is None:
        abort(404)
    return make_response(jsonify({"movie": movie.serialize()}),200)


@application.route('/movies/add', methods=['POST'])
@application.route('/movies', methods=['POST'])
def create_movie():
    """ 
    Create a movie object.
    :param movie_id:
    :param request.json: a dictionnary containing fields
    'name' and 'year.

    :return: if success the created Movie object
    """
    requested_fields = {'name', 'year'}
    included_fields = set(request.json.keys())
    if not request.json or not ut.test_intersection(requested_fields,included_fields):
        abort(400)
    movie_name = request.json['name']
    movie_year = request.json['year']

    movie = ut.add_movie(movie_name, movie_year)
    return make_response(jsonify({"movie": movie.serialize()}),201)


@application.route('/movies/update/<movie_id>', methods=['PUT'])
@application.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """
    Updates a movie based on its id.
    :param movie_id:
    :param request.json: a dictionnary containing fields
    'name' and 'year.
    :return: if success the updated Movie object
    """
    requested_fields = {'name', 'year'}
    included_fields = set(request.json.keys())

    movie = ut.get_movie(movie_id)
    if movie is None:
        abort(404)

    if not request.json:
        abort(400)

    if not ut.test_intersection(requested_fields,included_fields):
        abort(400)

    movie_name = request.json['name']
    movie_year = request.json['year']

    included_fields = set(request.json.keys())
    movie = ut.update_movie_by_id(movie_id,movie_name,movie_year)
    return make_response(jsonify(movie.serialize()))

@application.route('/movies/delete/<movie_id>', methods=['DELETE'])
@application.route('/movies/<movie_id>', methods=['DELETE'])
def del_movie(movie_id):
    """
    Deletes a movie based on its id. Then calls the Evaluations service
    to delete all the evaluations related to this movie
    :param movie_id:
    :return: 
    """
    movie = ut.get_movie(movie_id)
    if movie is None:
        abort(404)
    ut.delete_movie_by_id(movie_id)

    #TODO replace with amqp protocol?
    try:
        requests.delete("{}/evaluations/movies/{}".format(Config.evaluations_url,movie_id))
    except requests.exceptions.ConnectionError:
        return make_response(jsonify({"error":"The Evaluations service is unavailable."}), 503)

    return make_response(jsonify({"Deleted":True}),200)

@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@application.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

