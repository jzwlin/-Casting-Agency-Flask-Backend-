import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from env_var import find_key

database_name = os.environ['database_name']
database_path = os.environ['database_path']
database_url = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # uncomment the below line first run
    #db.create_all()

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String, nullable=False)
    release_date = Column(db.Date)
    #movie_cast = db.relationship('Movie_cast', backref="Movie", lazy=True)

    def __int__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    #def __repr__(self):
     #   return '<Movie{}>'.format(self.title)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    #movie_cast = db.relationship('Show', backref="Artist", lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

  #  def __repr__(self):
    #    return '<Actor {}>'.format(self.name)

    def format(self):
        return {
            'id': self.id,
            'name':self.name,
            'age': self.age,
            'gender': self.gender
        }


''' Save this part for future work'''
'''
class Movie_cast(db.Model):
  __tablename__ = 'Movie_cast'
  id = db.Column(db.Integer, primary_key=True)
  actor_id = db.Column(db.Integer, db.ForeignKey(
    'Actor.id'), nullable=False)
  movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
  role = db.Column(db.String(120))
  movie = db.relationship('Movie')
  artist = db.relationship('Actor')

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def __repr__(self):
    return '<Movie_cast {}{}>'.format(self.actor_id, self.movie_id)
'''




