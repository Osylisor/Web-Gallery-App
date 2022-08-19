
from datetime import datetime
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    second_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(25))
    galleries = db.relationship('Gallery')


class Gallery(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    gallery_name = db.Column(db.String(25), nullable = False)
    date = db.Column(db.DateTime,  default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    images = db.relationship('Image')


class Image(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(50))
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))

