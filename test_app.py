import os
import requests
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from env_var import find_key
from flask_cors import CORS
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc

from app import create_app
from datetime import datetime
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

class MovieTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'movie_test'
        self.database_path = os.environ['HEROKU_POSTGRESQL_BROWN_URL']
        setup_db(self.app)

        # new variable
        self.new_movie = {'title': 'A new movie', 'release_date': datetime.now().strftime('%Y-%m-%d')}
        self.new_actor = {'name': 'Lyn', 'age': 35, 'gender': 'female'}

        #new variable for modify
        self.new_movie_modify = {'title': 'Modify Movie', 'release_date': datetime.now().strftime('%Y-%m-%d')}
        self.new_actor_modify = {'name': 'Jane', 'age': 29, 'gender': 'male'}

        # token for each role
        self.casting_assistant = os.environ['casting_assistant']
        self.casting_director = os.environ['casting_director']
        self.executive_producer = os.environ['executive_producer']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # uncomment it at the first run
            #self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test functions for each route
    # one test for success behavior of each endpoint
    # one test for error behavior of each endpoint

    # test for 'gets' method
    def test_get_movies(self):
        res = self.client().get('/movies',headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data.decode("utf-8"))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_beyond_valid_movie(self):
        res = self.client().get('/movies/a',headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors(self):
        res = self.client().get('/actors',headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_beyond_valid_actor(self):
        res = self.client().get('/actors/a',headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # test for 'post' methods
    def test_create_new_movie(self):
        total_movies_before = len(list(map(Movie.format, Movie.query.all())))
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                 json=self.new_movie)
        data = json.loads(res.data)
        total_movies_after = len(list(map(Movie.format, Movie.query.all())))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(total_movies_after, total_movies_before + 1)

    def test_422_if_movie_creation_fails(self):
        new_movie = {'release_date': datetime.now()}
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                 json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_actor(self):
        total_actors_before = len(Actor.query.all())
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                 json=self.new_actor)
        data = json.loads(res.data)
        total_actors_after = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(total_actors_after, total_actors_before + 1)

    def test_422_if_actor_creation_fails(self):
        new_actor = {'age': 99}
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                         json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # test for deletes
    def test_delete_movie(self):
        res = self.client().delete('/movies/1',
                                   headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)


    def test_422_if_deleting_movie_does_not_exist(self):
        res = self.client().delete('/movies/a',
                                   headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_422_if_deleting_actor_does_not_exist(self):
        res = self.client().delete('/actors/a',
                                   headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    # test for patch
    def test_edit_movie(self):
        total_movies_before = len(Movie.query.all())
        res = self.client().patch('/movies/2',
                                  headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                  json=self.new_movie_modify)
        data = json.loads(res.data)
        total_movies_after = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(total_movies_after, total_movies_before)


    def test_fail_edit_movie(self):
        new_movie = {'release_date': datetime.now()}
        res = self.client().patch('/movies/5000',
                                  headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                  json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_edit_actor(self):
        total_actors_before = len(Actor.query.all())
        res = self.client().patch('/actors/2',
                                  headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                  json=self.new_actor_modify)
        data = json.loads(res.data)
        total_actors_after = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(total_actors_after, total_actors_before)

    def test_fail_edit_actor(self):
        new_actor = {'age': 99}
        res = self.client().patch('/actors/500',
                                  headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                  json=new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # tests of RBAC for each role
    # casting assistant
    # test for 'get' an actor
    def test_get_actor_casting_assistant(self):
        res = self.client().get('/actors',
                                headers={"Authorization": "Bearer {}".format(self.casting_assistant)},
                                json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # test for 'post' an actor
    def test_create_new_actor_casting_assistant(self):
        new_actor = {'name': 'Mary', 'age': 22, 'gender': 'female'}
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.casting_assistant)},
                                 json=new_actor)

        self.assertEqual(res.status_code, 401)


    # casting director
    # test for post an actor
    def test_create_new_actor_casting_director(self):
        new_actor = {'name': 'Harry Potter', 'age': 23, 'gender': 'male'}
        total_actors_before = len(Actor.query.all())
        res = self.client().post('/actors',
                                 headers={"Authorization": "Bearer {}".format(self.casting_director)},
                                 json=new_actor)
        data = json.loads(res.data)
        total_actors_after = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(total_actors_after, total_actors_before + 1)


    # test for post a movie
    def test_create_new_movie_casting_director(self):
        new_movie = {'title': 'test movie name', 'release_date': datetime.now().strftime('%Y-%m-%d')}
        res = self.client().post('/movies',
                                 headers={"Authorization": "Bearer {}".format(self.casting_director)},
                                 json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    # executive producer
    # test for post a movie
    def test_create_new_movies_executive_producer(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(self.executive_producer)},
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_a_movie_executive_producer(self):
        res = self.client().delete('/movies/4',
                                   headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertEqual(movie, None)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
