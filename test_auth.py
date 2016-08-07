from flask import Flask
from flask_httpauth import HTTPBasicAuth
import sys

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
    sys.stderr.write('Password ...')
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run(host="localhost", port=3752, debug=True)