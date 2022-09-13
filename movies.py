from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from flask_migrate import Migrate
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/MovieDatabase'

class Development_Config(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/MovieDatabase'

class Production_Config(Config):
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://","postgresql://",1)# to replace it only 1 time use 1
    SQLALCHEMY_DATABASE_URI = uri

env = os.environ.get("ENV","Development")# if the env is set then use that else use development

if env == "Production":
    config_str = Production_Config
else:
    config_str = Development_Config

app = Flask(__name__)

app.config.from_object(config_str)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/MovieDatabase'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:1234@localhost/MovieDatabase'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    @staticmethod
    def add_movies(title,year,genre):
        new_movie = Movie(title=title,year=year,genre=genre)
        db.session.add(new_movie)
        db.session.commit()

    @staticmethod
    def get_movies():
        data = Movie.query.all()
        return data

    @staticmethod
    def get_movies_id(id):
        data = Movie.query.filter_by(id=id).first()
        return data

    @staticmethod
    def del_movies(id):
        data = Movie.query.filter_by(id=id).delete()
        db.session.commit()
        return data

    @staticmethod
    def put_movies(id, title, year, genre):
        movie = Movie.query.filter_by(id=id).first()
        print(movie)
        movie.title=title
        movie.year=year
        movie.genre=genre
        db.session.commit()
        return movie


class allmovies(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        Movie.add_movies(title = data["title"],year = data["year"],genre = data["genre"])
        return " "

    def get(self):
        data = Movie.get_movies()
        print(data)
        movieslst=[]

        for moviedata in data:
            moviedict = {'title':moviedata.title, 'year':moviedata.year, 'genre':moviedata.genre}
            movieslst.append(moviedict)
        return movieslst

class movie_id(Resource):
    def get(self,id):
        data = Movie.get_movies()
        for i in data:
            mov = {}
            if i.id==id:
                mov['title'] = i.title
                mov['year'] = i.year
                mov['genre'] = i.genre
                return jsonify((mov),{"status_msg":HTTPStatus.OK})
        else:
                return {'message':'movie not found','status':HTTPStatus.NOT_FOUND}


    def delete(self,id):
        data = Movie.del_movies(id)
        if data:
            return jsonify({"message":"movie got deleted","status_msg": HTTPStatus.OK})
        else:
            return {'message': 'id not found', 'status': HTTPStatus.NOT_FOUND}

    def put(self, id):
        data = request.get_json()
        print(data)
        result = Movie.put_movies(id=id, title= data['title'], year= data['year'], genre= data['genre'])
        if result:
            return jsonify({"message":"movie is updated", "status_msg": HTTPStatus.OK})
        else:
            return jsonify({"message":"id not found", "status_msg": HTTPStatus.NOT_FOUND})

api.add_resource(allmovies,"/movies")
api.add_resource(movie_id,"/movies/<int:id>")
if __name__ == "__main__":
    app.run()


#after adding the migrate package and migrate commands run below 3 commands
#flask --app movies.py db init
#flask --app movies.py db migrate
#flask --app movies.py db upgrade


#from flask_sqlalchemy_test import db
# db.create_all()
# from flask_sqlalchemy_test import Profile
# admin = Profile(username= "admin",email="shirish@email.com")
#Profile.query.all()
#Profile.query.filter_by(username = 'admin').first()
#add(request.get_json())
#jsonify({'message':'id not found','status':'404'})

#pip install psycopg2
#pip install gunicorn ---functionalities of http server is given by gunicorn