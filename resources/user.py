from flask_restful import Resource,reqparse
from flask import jsonify, make_response
import pymysql
import traceback
from server import db
from models import UserModel
from dotenv import load_dotenv
import os
load_dotenv()

parser = reqparse.RequestParser()
#請求放行的白名單
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')
parser.add_argument('deleted')

class User(Resource):
    def db_init(self):
        # db = pymysql.connect(
        #     host = r'localhost',
        #     user =  r'root',
        #     password =  r'mysql',
        #     database =  r'api',
        #     )
        db = pymysql.connect(
            host = os.getenv('DB_HOST'),
            user =  os.getenv('DB_USER'),
            password =  os.getenv('DB_PASSWORD'),
            database =  os.getenv('DB_SCHEMA'),
            )
        #將拿到的資料dict化
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From api.users where id = {} and deleted is not True""".format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()

        return jsonify({'data':user})

    def patch(self, id):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        # user = {
        #     'name': arg['name'],
        #     'gender': arg['gender'],
        #     'birth': arg['birth'],
        #     'note': arg['note'],
        # }

        # query = []
        # for key, value in user.items():
        #     if value:
        #         query.append(f"`{key}` = '{value}'")

        # query = ", ".join(query)
        # sql = """
        #     UPDATE `api`.`users` SET {} WHERE `id`='{}'
        # """.format(query, id)

        user = UserModel.query.filter_by(id=id, deleted=None).first()
        if arg['name'] != None:
            user.name = arg['name']

        response = {}
        try:
            # cursor.execute(sql)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        # db.commit()
        # db.close()
        return jsonify(response)

    def delete(self, id):
        # db, cursor = self.db_init()
        # sql = """
        #     DELETE FROM `api`.`users` WHERE `id`='{}';
        # """.format(id)
        # sql = """
        #     UPDATE `api`.`users` SET `deleted`='1' WHERE `id`='{}';
        # """.format(id)


        response = {}
        try:
            # user = UserModel.query.filter_by(id=id, deleted=None).first()
            # db.session.delete(user)
            # db.session.commit()

            user = UserModel.query.filter_by(id=id, deleted=None).first()
            user.deleted = True
            db.session.commit()

            # cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        # db.commit()
        # db.close()
        return jsonify(response)

class Users(Resource):
    def db_init(self):
        # db = pymysql.connect(
        #     host = r'localhost',
        #     user =  r'root',
        #     password =  r'mysql',
        #     database =  r'api',
        #     )
        db = pymysql.connect(
            host = os.getenv('DB_HOST'),
            user =  os.getenv('DB_USER'),
            password =  os.getenv('DB_PASSWORD'),
            database =  os.getenv('DB_SCHEMA'),
            )
        #將拿到的資料dict化
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        # db, cursor = self.db_init()
        # arg = parser.parse_args()
        # sql = 'Select * From api.users where deleted is not True'
        # if arg['gender'] != None:
        #     sql += ' and gender = "{}"'.format(arg['gender'])
        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()

        # return make_resposne(jsonify({'data':users}))

        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})
    
    def post(self):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or "1900-01-01",
            'note': arg['note'] or None,
        }

        # sql = """
        #     INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        # """.format(user['name'], user['gender'], user['birth'], user['note'])

        response = {}
        status_code = 200

        try:
            new_user = UserModel(name=user['name'], gender=user['gender'], birth=user['birth'], note=user['note'])
            db.session.add(new_user)
            db.session.commit()
            # cursor.execute(sql)
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'

        # db.commit()
        # db.close()
        return make_response(jsonify(response), status_code)
