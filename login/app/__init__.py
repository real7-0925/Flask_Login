#login main

from flask import Flask, abort, render_template, request, jsonify, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from .config.config import config
import sqlite3


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    #設定config
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    @app.route('/')
    def index():
        return 'success'
    
    @app.route('/create_all')
    def create_db():
        db.create_all()
        return 'success'
    
    #判斷權要需要normal以上
    @app.route('/normal_member')
    @check_login('normal')
    def member_normal_page():
        name = session.get('username')
        role = session.get('role')
        uid = session.get('uid')
        return f'type:normal,{name},{role},{uid}'
    
    #判斷權限需要admin以上
    @app.route('/admin_member')
    @check_login('admin')
    def member_admin_page():
        name = session.get('username')
        role = session.get('role')
        uid = session.get('uid')

        return f'type:admin,{name}, {role}, {uid}'
    
    @app.route('/table')
    def table():
        from .model.user import UserModel, UserSchema 
        # user_data = UserSchema.load(request.form, partial=True)

        # uid = user_data['uid']
        # name = user_data['name']
        # role = user_data['role']
        # insert_time = user_data['insert_time']

        # uid = UserModel.query.with_entities(UserModel.uid).all()
        # name = UserModel.query.with_entities(UserModel.name).all()
        # role = UserModel.query.with_entities(UserModel.role).all()
        # insert_time = UserModel.query.with_entities(UserModel.insert_time).all()
        # content = [[uid, name, role, insert_time]][:100]
        # print(content)

        uid = UserModel.query.with_entities(UserModel.uid, UserModel.name, UserModel.role, UserModel.insert_time).all()
        # uid_dict = vars(uid)
        content = [[uid]][:100]

        # users = UserModel.query.all()
        # schema = UserSchema(many=True)
        # users_data = schema.dump(users)

        labels = ['uid', 'name', 'role', 'insert_time']

        return render_template("table.html", content=content, labels=labels)
        # return  render_template('table.html', cotent=content, labels=labels)
    
    return app

def register_extensions(app):
    """Register extensions with the Flask application"""
    db.init_app(app)

def register_blueprints(app):
    """Register blueprints with the Flask application"""
    from .view.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')


def check_login(check_role):
    def decorator(func):
        def wrap(*args, **kw):
            user_role = session.get('role')
            print(user_role)
            print(type(user_role))

            if user_role == None or user_role == '':
                return abort(401)
            
            else :
                if check_role =='admin' and check_role == user_role:
                    return func(*args, **kw)
                if check_role =='normal':
                    return func(*args, **kw)
                
                else:
                    return abort(401)

        wrap.__name__ = func.__name__
        return wrap
    return decorator

