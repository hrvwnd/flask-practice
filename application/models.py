from application import db,login_manager
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(150),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    posts = db.relationship('Posts', backref = 'author', lazy = True)

    def __repr__(self):
        return ''.join([
            'User ID: ',str(self.id), '\r\n',
            'Email: ', self.email,
            'Name', self.first_name,' ', self.last_name
            ])


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(100), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    image = db.Column(db.String(100), nullable = False, unique = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    def __repr__(self):
        return ''.join([
            'User_ID: ', self.first_name, ' ', self.last_name, '\r\n',
            'Title: ', self.title, '\r\n', self.content
        ])


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))



#project tables start 
"""
class Artists(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    name = db.Column(db.String(100), nullable=False, unique= True)
    default_genre = db.Column(db.String(100),nullable = False, unique= True)

class Genres(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    folder_path = db.Column(db.String(100), nullable = False, unique = True)

class Tracks(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    title = db.Column(db.String(100), nullable = False)
    filename = db.Column(db.String(100), nullable = False, unique = True)
    album = db.Column(db.String(100), nullable = False)
    artist_id = db.Column(db.Integer,db.ForeignKey('artists.id)'))
    genre_id = db.Column(db.Integer,db.ForeignKey('genre.id'))

"""