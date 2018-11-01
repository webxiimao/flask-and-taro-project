#-*- coding=utf8 -*-
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError




class Articles(db.Model):
    '''
    文章模块的数据库类
    '''
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    content = db.Column(db.String(512))
    isDelete = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<Aritcle %r>' % (self.title)




class Category(db.Model):
    '''
    类别模块
    '''
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(12), nullable=True)
    article = db.relationship('Articles', backref='classname',lazy='dynamic')
    isDelete = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Category %r>' % (self.name)




def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
