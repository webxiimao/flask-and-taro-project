#-*- coding=utf8 -*-
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from .articles import Articles, Category


class User(db.Model):
    # __tablename__ = 'User'
    # __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True, server_default='', index=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(24), nullable=False)
    login_time = db.Column(db.Integer)
    headshot = db.Column(db.String(128))
    _password = db.Column(db.String(128), nullable=False)
    isDelete = db.Column(db.Integer, default=0, nullable=False)
    field1 = db.Column(db.String(128))
    articles = db.relationship("Articles", backref="author", lazy="dynamic")

    def __init__(self, username, password, email, nickname):
        self.username = username
        self._password = password
        self.email = email
        self.nickname = nickname

    def __repr__(self):
        return '<User %r>' % (self.username)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self,hash,  password):
        return check_password_hash(hash, password)

    def get(self, id):
        return self.query.filter_by(id=id).first()

    @staticmethod
    def add(user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()



def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason






if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.getcwd())))
    # reload(sys)

    # db.drop_all()
    db.create_all()