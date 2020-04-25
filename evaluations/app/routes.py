from app import app
from flask import Flask, render_template
from flask import jsonify, make_response
from flask import request, abort
import logging as lg 
from werkzeug.exceptions import NotFound, ServiceUnavailable
from config import Config
import requests

import app.utils as ut


@app.route('/', methods=['GET'])
@app.route('/evaluations', methods=['GET'])
@app.route('/evaluations/', methods=['GET'])
def all_evaluations():
    """
    Returns all movie evaluations in the database for Evaluations
    service
    """
    evaluations = ut.get_evaluations()
    if len(evaluations) == 0:
        abort(404)
    return make_response(jsonify({"evaluations":evaluations}),200)


@app.route('/evaluations/<evaluation_id>', methods=['GET'])
def evaluation(evaluation_id):
    """
    Returns a movie evaluation given an evaluation id 
    :param evaluation_id:
    :return: An Evaluation
    """
    evaluation = ut.get_evaluation(evaluation_id)
    if evaluation is None:
        abort(404)
    return make_response(jsonify({"evaluation": evaluation.serialize()}),200)


@app.route('/evaluations/movies/<movie_id>', methods=['GET'])
def movie_evaluations(movie_id):
    """
    Returns all evaluations for a given movie 
    :param movie_id:
    :return: List of Evaluation of the movie movie_id
    """

    try:
        response = requests.get("{}/movies/{}".format(Config.movies_url,movie_id))
        if response.status_code != 200:
            return make_response(jsonify({"error":"Movie not found"}),404)

        evaluations = ut.get_evaluations_movie_id(movie_id)
        if len(evaluations) == 0:
            return make_response(jsonify({"error":"No evaluations for this movie"}),404)

        return make_response(jsonify({"evaluations":evaluations}),200)

    except requests.exceptions.ConnectionError:
        # raise ServiceUnavailable("The Movies service is unavailable.")
        return make_response(jsonify({"error":"The Movies service is unavailable."}), 503)

    ## If not checking if movie still exists in movie services
    # evaluations = ut.get_evaluations_movie_id(movie_id)
    # if len(evaluations) == 0:
    #     return make_response(jsonify({"error":"No evaluations for this movie"}),404)
    # return make_response(jsonify({"evaluations":evaluations}),200)


@app.route('/evaluations/add/<movie_id>', methods=['POST'])
@app.route('/evaluations/<movie_id>', methods=['POST'])
def create_evaluation(movie_id):
    """
    First calls the Movies service to check if the movie exists.  
    Then add an evaluation to a movie.
    :param movie_id:
    :param request.json: a dictionnary containing a field
    'description.

    :return: if success the created Evaluation object
    """

    requested_fields = {'description'}
    included_fields = set(request.json.keys())
    if not request.json or not ut.test_intersection(requested_fields,included_fields):
        abort(400)
    description = request.json['description']
    try:
        response = requests.get("{}/movies/{}".format(Config.movies_url,movie_id))
        if response.status_code != 200:
            return make_response(jsonify({"error":"Movie not found"}),404)
        evaluation = ut.add_evaluation(description,movie_id)
        return make_response(jsonify({"evaluation": evaluation.serialize()}),201)

    except requests.exceptions.ConnectionError:
        # raise ServiceUnavailable("The Movies service is unavailable.")
        return make_response(jsonify({"error":"The Movies service is unavailable."}), 503)



    
    
        


@app.route('/evaluations/update/<evaluation_id>', methods=['PUT'])
@app.route('/evaluations/<evaluation_id>', methods=['PUT'])
def update_evaluation(evaluation_id):
    """
    Updates an evaluation based on its id.
    :param evaluation_id:
    :param request.json: a dictionnary containing a field
    'description.
    :return: if success the updated Evaluation object
    """

    requested_fields = {'description'}
    included_fields = set(request.json.keys())

    evaluation = ut.get_evaluation(evaluation_id)
    if evaluation is None:
        abort(404)

    if not request.json:
        abort(400)

    if not ut.test_intersection(requested_fields,included_fields):
        abort(400)

    description = request.json['description']

    included_fields = set(request.json.keys())
    evaluation = ut.update_evaluation_by_id(evaluation_id,description)
    return make_response(jsonify(evaluation.serialize()))

@app.route('/evaluations/delete/<evaluation_id>', methods=['DELETE'])
@app.route('/evaluations/<evaluation_id>', methods=['DELETE'])
def del_evaluation(evaluation_id):
    """
    Deletes an evaluation based on its id.
    :param evaluation_id:
    :return: 
    """
    evaluation = ut.get_evaluation(evaluation_id)
    if evaluation is None:
        abort(404)
    ut.delete_evaluation_by_id(evaluation_id)
    return make_response(jsonify({"Deleted":True}),200)

@app.route('/evaluations/movies/<movie_id>', methods=['DELETE'])
def del_evaluation_movie_id(movie_id):
    """
    Deletes all the evaluations of a given movie based on its id.
    :param movie_id:
    :return: 
    """
    if ut.check_movie_id_in_db(movie_id):
        ut.delete_evaluation_by_movie_id(movie_id)
        return make_response(jsonify({"Deleted":True}),200)
    else:
        return make_response(jsonify({"Error":"No evaluations for this movie"}), 404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

