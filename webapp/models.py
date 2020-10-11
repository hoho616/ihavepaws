import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import db, login

class Pictures(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(64),
                      index=True,
                      unique=True,
                      nullable=False)

    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)
    path = db.Column(db.String(200))
    description = db.Column(db.String(200))
  #  comments = db.relationship('Comments', backref='pictures', lazy=True, passive_deletes=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(100), nullable=False),
    nickname = db.Column(db.String(256))
    created = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comments', backref='users', lazy=True, passive_deletes=True)
    pics = db.relationship('Pictures', backref='users', lazy=True, passive_deletes=True)
    password_hash = db.Column(db.String(128), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    pic_id  = db.Column(db.Integer, db.ForeignKey('pictures.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Integer)
    pic_id  = db.Column(db.Integer, db.ForeignKey('pictures.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))