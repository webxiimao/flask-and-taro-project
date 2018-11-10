#-*- coding=utf8 -*-
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


'''
文章标签关联表
'''
article_tags = db.Table('article_tags',
                         db.Column('article_id',db.Integer,db.ForeignKey('articles.id'),primary_key=True),
                         db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),primary_key=True)
                         )


class Articles(db.Model):
    '''
    文章模块的数据库类
    '''
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    content = db.Column(db.String(512))
    create_data = db.Column(db.DateTime, default=datetime.now)
    isDelete = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    tag = db.relationship('Tags',secondary=article_tags, backref='articles',lazy='dynamic')


    def __init__(self, title, content, user_id, category_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.category_id = category_id


    @staticmethod
    def add(article):
        db.session.add(article)
        return session_commit()


    def update(self):
        return session_commit()


    def __repr__(self):
        return '<Aritcle %r>' % (self.title)




class Category(db.Model):
    '''
    类别模块
    '''
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    name = db.Column(db.String(12), nullable=True, unique=True)
    article = db.relationship('Articles', backref='classname',lazy='dynamic')
    isDelete = db.Column(db.Integer,default=0)


    def __init__(self, name):
        self.name = name

    @staticmethod
    def return_category(name):
        id = self.query.filter_by(name=name).first()
        return id

    @staticmethod
    def add(category):
        db.session.add(category)
        return session_commit()

    def __repr__(self):
        return '<Category %r>' % (self.name)


class Tags(db.Model):
    '''
    标签模块
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    tag = db.Column(db.String(24), nullable=True, unique=True)

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '<Tags %r>' % (self.tag)




def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
