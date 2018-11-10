#-*- coding=utf8 -*-
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class girls_tag(db.Model):
    '''
    标签表
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(256))
    tag = db.Column(db.String(48), nullable=False, unique=True)
    albums = db.relationship('girls_album', backref="tag", lazy="dynamic")

    def __repr__(self):
        return '<girls_tag {}>'.format(self.tag)




class girls_album(db.Model):
    '''
    女孩相册表
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    cover_img = db.Column(db.String(256), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String(512))
    girls_tag_id = db.Column(db.Integer, db.ForeignKey('girls_tag.id'))
    imgs = db.relationship('girls_img', backref="album", lazy="dynamic")

    def __repr__(self):
        return '<girls_album {}>'.format(self.tag)



class girls_img(db.Model):
    '''
    图片表
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    img_path = db.Column(db.String(256),nullable=False, unique=True)
    #爬虫相关 1:初始状态  2:正在进行   3:已完成
    img_status = db.Column(db.Integer, default=1, nullable=False)
    init_url = db.Column(db.String(48))

    def __repr__(self):
        return '<girls_img {}>'.format(self.tag)