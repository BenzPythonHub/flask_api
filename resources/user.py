from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')


class Users(Resource):
    def db_init(self):
        db = pymysql.connect(
            host = r'localhost',
            user =  r'flask',
            password =  r'HFY3m2Ce5E4wCfdM',
            database =  r'flask',
            )

        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        db, cursor = self.db_init()
        sql = 'Select * From flask.users'
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
            'note': arg['note'] or 0,
        }

        sql = """
            INSERT INTO `users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])

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



