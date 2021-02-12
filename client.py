import requests
import json
import jwt
import time

payload = "{\"user_id\":\"123\"}"
valid_token = jwt.encode({'user_id': '123', 'timestamp': int(time.time())}, 'GG30687', algorithm='HS256')
url = "http://0.0.0.0:5000/users"
print(valid_token)
headers = {
    'Content-Type': 'application/json',
    'auth': valid_token,
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
