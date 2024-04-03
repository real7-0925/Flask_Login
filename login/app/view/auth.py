#auth

from flask import Flask, render_template, request, session, Blueprint, make_response
from flask_restful import Api, Resource, reqparse
from marshmallow import ValidationError
from ..model.user import UserModel, UserSchema
from .abort_msg import abort_msg
from .. import db

auth = Blueprint('auth', __name__)
api = Api(auth)

users_schema = UserSchema()

class Signup(Resource):
    def post(self):
        try:
            #資料驗證
            user_data = users_schema.load(request.form, partial=True)
            #註冊
            new_user = UserModel(user_data)
            new_user.save_db()
            new_user.save_session()
            return {'msg': 'registration success'}, 200

        except ValidationError as error:
            return {'errors': error.messages}, 400
        
        except Exception as e:
            return {'errors': abort_msg(e)}, 500
    
    def get(self):
        return make_response(render_template('signup.html'))
    
# class Table(Resource):
#     def post(self):
#         try:
#             # uid = UserModel.get_user(uid)
#             # name = UserModel.get_user(name)
#             # role = UserModel.get_user(role)
#             # insert_time = UserModel.get_user(insert_time)
#             # content = [[uid, name, role, insert_time]][:100]
#             # labels = ['uid', 'name', 'role', 'insert_time']

#             uid = UserModel.query.first()
#             name = UserModel.query.first()
#             role = UserModel.query.first()
#             insert_time = UserModel.query.first()
#             content = [[uid, name, role, insert_time]][:100]
#             labels = ['uid', 'name', 'role', 'insert_time']


            

#         except ValidationError as error:
#             return {'errors': error.messages}, 400
        
#         except Exception as e:
#             return {'errors': abort_msg(e)}, 500
    
#     def get(self):
#             # uid = UserModel.query.first()
#             # name = UserModel.query.first()
#             # role = UserModel.query.first()
#             # insert_time = UserModel.query.first()
#             # content = [[uid, name, role, insert_time]][:100]
#             # labels = ['uid', 'name', 'role', 'insert_time']

#             # return make_response(render_template('table.html', content=content, labels=labels))
#             return make_response(render_template('table.html'))
#         #return render_template("table.html", content=content, labels=labels )
    
    

class Login(Resource):
    def post(self):
        try:
            # 資料驗證
            user_data = users_schema.load(request.form)
            name = user_data['name']
            password = user_data['password']
            
            #登入
            query = UserModel.get_user(name)
            if query != None and query.verify_password(password):
                query.save_session()
                return {'msg':'ok'},200
            
            else:
                return{'errors': 'incorrect username or password'}, 400
            
        except ValidationError as error:
            return {'errors': error.messages}, 400
        
        except Exception as e:
            return {'errors': abort_msg(e)}, 500
        
    def get(self):
        return make_response(render_template('login.html'))


class Logout(Resource):
    def get(self):
        UserModel.remove_session()
        return {'msg': 'logout'}, 200

api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
# api.add_resource(Table, '/table')

