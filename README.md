# Full Stack Movie Actor Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
python3 -m venv venv 
source /venv/bin/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql movie_actor < movie_actor.psql
```

## Environment Variables Setup 
```bash 
source .bashrc
```


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Database 

There are total 2 data tables in this projectL Movie and Actor.

To setup the database, run:
```
dropdb movie_actor
createdb movie_actor 
psql movie_actor < movie_actor.psql  
```

## Endpoints 

There are total 8 endpoints in this projects: 
1. GET /actors 
2. GET /movies 
3. DELETE /actors/
4. DELETE /movies/
5. POST /actors/
6. POST/movies/
7. PATCH  /actors/
8. PATCH /actors/


## Roles

There are 3 roles in the project: Casting Assisnt, Casting Director, and Exectuive Producer 

Here is the permission table for each role: 
Casting Assistant: 1,2
Casting Director: 1,2,3,5,7,8
Exectuive Producer: 1,2,3,4,5,6,7,8 


## Testing
To run the tests, run

```
bash recreate_movie_test_sql  
python test_app.py
```
