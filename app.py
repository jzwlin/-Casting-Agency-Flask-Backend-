import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

# set up db
def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # All route functions

  @app.route('/')
  def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Hello"
    if excited == 'true': greeting = greeting + "!!!!!"
    return greeting


  # get functions
  # get movies
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):
    try:
      movies = list(map(Movie.format, Movie.query.all()))

      if not movies:
        abort(404)
      result = {
        "success": True,
        "movies": movies
      }

      return jsonify(result)
    except:
      abort(422)

  # get actors
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    try:
      actors = list(map(Actor.format, Actor.query.all()))
      if not actors:
        abort(404)
    except Exception as e:
      print(e)
      abort(500)
    return jsonify({"success": True, "actors": actors})

  # delete movies
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_question(jwt, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)
      movie.delete()

      return jsonify({
        'success': True,
        'deleted': movie_id,
        'total_questions': len(Movie.query.all())
      })
    except:
      abort(422)

  # delete actors
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor_id,
        'total_questions': len(Actor.query.all())})
    except:
      abort(422)

  # post a movie
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(jwt):
    body = request.get_json()

    if not ('title' in body and 'release_date' in body):
      abort(422)

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)
    try:
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()

      return jsonify({
        'success': True,
        'created': movie.id
      })

    except:
      abort(422)

  # post an actor
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(jwt):
    body = request.get_json()

    if not ('name' in body and 'age' in body and 'gender' in body):
      abort(422)

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()

      return jsonify({
        'success': True,
        'create': actor.id,
        'total_actors': len(Actor.query.all())
      })

    except:
      abort(422)

  # patch a movie
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(jwt, id):
    title = request.get_json().get('title')
    release_date = request.get_json().get('release_date')

    # make sure some data was passed
    try:
        data = title or release_date
        if not data:
            abort(400)
    except (TypeError, KeyError):
        abort(400)

    # make sure movie exists
    movie = Movie.query.filter_by(id=id).first()
    if not movie:
        abort(404)

    # update
    try:
        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        abort(422)


  # patch a actor
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(jwt, id):
    name = request.get_json().get('name')
    age = request.get_json().get('age')
    gender = request.get_json().get('gender')

    # make sure some data was passed
    try:
        data = name or age or gender
        if not data:
            abort(400)
    except (TypeError, KeyError):
        abort(400)

    # make sure movie exists
    actor = Actor.query.filter_by(id=id).first()
    if not actor:
        abort(404)

    # update
    try:
        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        abort(422)

  # errors
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'Internal Server Error'
    }), 500

  @app.errorhandler(AuthError)
  def auth_error(e):
    return jsonify(e.error), e.status_code

  return app


APP = create_app()
# run the app
if __name__ == '__main__':
  APP.run(host='0.0.0.0', port=8080, debug=True)
