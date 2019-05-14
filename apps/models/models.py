#-*- coding=utf8 -*-
'''
write by xii
'''
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    # __tablename__ = 'User'
    # __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True, server_default='', index=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(24), nullable=False)
    login_time = db.Column(db.Integer)
    headshot = db.Column(db.String(128))
    real_avatar = db.Column(db.String(128))
    _password = db.Column(db.String(128), nullable=False)
    isDelete = db.Column(db.Integer, default=0, nullable=False)
    # field1 = db.Column(db.String(128))
    articles = db.relationship("Articles", backref="author")
    comment_id = db.relationship('Comment',backref='user',foreign_keys="Comment.user_id")
    reply_cid = db.relationship('Comment',backref='reply_user',foreign_keys="Comment.reply_uid")


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


class girls_tag(db.Model):
    '''
    标签表
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(256))
    tag = db.Column(db.String(48), nullable=False, unique=True)
    albums = db.relationship('girls_album', backref="tag", lazy="dynamic")
    cover_img = db.Column(db.String(1024))
    local_cover_img = db.Column(db.String(1024))

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
        return '<girls_album {}>'.format(self.title)



class girls_img(db.Model):
    '''
    图片表
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    img_path = db.Column(db.String(256))
    #爬虫相关 0:初始状态  1:正在进行   2:已完成
    img_status = db.Column(db.Integer, default=0, nullable=False)
    # init_url = db.Column(db.String(1024))
    img_url = db.Column(db.String(1024))
    local_img_url = db.Column(db.String(1024))
    girls_album_id = db.Column(db.Integer ,db.ForeignKey('girls_album.id'))

    def __repr__(self):
        return '<girls_img {}>'.format(self.img_url)




'''
文章标签关联表
'''
article_tags = db.Table('article_tags',
                         db.Column('article_id',db.Integer,db.ForeignKey('articles.id'),primary_key=True),
                         db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),primary_key=True)
                         )

class Comment(db.Model):
    '''
    用户评论模型
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(256),nullable=True)
    article_id = db.Column(db.Integer,db.ForeignKey('articles.id'))#评论主题的id oneToMany
    parent_id = db.Column(db.Integer,db.ForeignKey('comment.id'))#主评论id oneToMany
    parent = db.relationship("Comment",backref="comment",remote_side=[id])
    reply_uid = db.Column(db.Integer,db.ForeignKey('user.id'))#评论目标user的id oneToMany
    restore_time = db.Column(db.DateTime, default=datetime.now)#回复时间
    # users =db.relationship('User',primaryjoin="or_(Comment.id==User.comment_id, Comment.reply_uid==User.reply_cid)")
    # field1 = db.Column(db.DateTime, default=datetime.now)#回复时间

    def __init__(self,user_id,content,article_id,parent_id,reply_uid):
        self.user_id = user_id
        self.content = content
        self.article_id = article_id
        self.parent_id = parent_id
        self.reply_uid = reply_uid

    def __repr__(self):
        return "<Comment %r>"%(self.content)

    @staticmethod
    def add(comment):
        db.session.add(comment)
        return db.session.commit()




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
    comment = db.relationship('Comment',backref='articles',lazy="dynamic")
    field1 = db.Column(db.Integer,default=0)


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





def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
