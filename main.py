from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql
import traceback
#json web token
import jwt
import time
from server import app

# app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')

api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == "NotFound":
        status_code = 404
    elif type(error).__name__ == "TypeError":
        status_code = 500

    return jsonify({'msg': type(error).__name__}), status_code

# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     # valid_token = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'GG30687', algorithm='HS256').decode('utf-8')
#     valid_token = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'GG30687', algorithm='HS256')
#     print(token)
#     print(valid_token)
#     if token == valid_token:
#         pass
#     else:
#         return {
#             'msg': 'invalid token'
#         }

@app.route('/')
def index():
    return 'Bello World XD'

@app.route('/user/<user_id>/account/<id>/deposit', methods=['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = 'Update api.accounts Set balance = {} Where id = {} and deleted is not True'.format(balance, id)

    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'

    db.commit()
    db.close()
    return jsonify(response)

@app.route('/user/<user_id>/account/<id>/withdraw', methods=['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response = {}
    if balance < 0:
        response['msg'] = 'money not enough'
        return jsonify(response)
    else:
        sql = 'Update api.accounts Set balance = {} Where id = {} and deleted is not True'.format(balance, id)

        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)

def get_account(id):
    db = pymysql.connect(
        host = r'localhost',
        user =  r'root',
        password =  r'mysql',
        database =  r'api',
        )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """Select * From api.accounts where id = {} and deleted is not True""".format(id)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)