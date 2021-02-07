from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource):
    def db_init(self):
        db = pymysql.connect(
            host = r'127.0.0.1',
            user =  r'root',
            password =  r'mysql',
            database =  r'api',
            )

        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """SELECT * FROM api.users where id = {} and deleted is not True;""".format(id)
        try:
            cursor.execute(sql)
            db.commit()
            user = cursor.fetchone()
            db.close()
            return jsonify({'data': user})
        except :
            # traceback.print_exc()
            return "Your id can't find result"

    def patch(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note'],
        }

        query = []

        for key, value in user.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))
        query = ", ".join(query)
        sql = """
            UPDATE `api`.`users` SET {} WHERE (`id` = '{}');
        """.format(query, id)

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except :
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)

class Users(Resource):
    def db_init(self):
        db = pymysql.connect(
            host = r'127.0.0.1',
            user =  r'root',
            password =  r'mysql',
            database =  r'api',
            )

        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        sql = 'Select * From api.users where deleted is not True'
        if arg['gender'] != None:
            sql += ' and gender = "{}"'.format(arg['gender'])
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()

        return jsonify({'data': users})

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note'] or None,
            'deleted':arg['deleted'] or 0,
        }

        sql = """
            INSERT INTO `users` (`name`, `gender`, `birth`, `note`, `deleted`) VALUES ('{}', '{}', '{}', '{}', '{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'], user['deleted'])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except :
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)



