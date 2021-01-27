from flask_restful import Resource
import pymysql

class Users(Resource):
    def db_init(self):
        db = pymysql.connect(r'127.0.0.1', r'flask', r'HFY3m2Ce5E4wCfdM', r'flask')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor