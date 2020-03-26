from flask import Flask
from flask import request, abort
import datetime as dt
import time

app = Flask(__name__)

messages = [
    {'username': "alina", 'text': 'hello', 'time': 0.0}
]

users = {
    'Alina': '123'
}

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/status")
def status():
    current_time = dt.datetime.now()
    common_users = len(users)
    common_messages = len(messages)
    return {
        'status': True,
        'name': 'meow',
        'time': current_time.isoformat(),
        'common users': common_users,
        'common messages': common_messages,
    }

@app.route("/send", methods=['POST'])
def send():
    """
    receive json
    {
        "username": str
        "password": str
        "text": str
    }
    :return: JSON {"ok": true}
    """
    username = request.json['username']
    password = request.json['password']

    if username in users:
        if password != users[username]:
            return abort(401)
    else:
        users[username] = password
    text = request.json['text']
    current_time = time.time()
    message = {'username': username, 'text': text, 'time': current_time}
    messages.append(message)
    print(messages)
   # print(request.json)
    return {"ok": True}

@app.route("/messages")
def messages_view():
    """
    receive ?after=float

    :return: JSON{
        "message": [
            {"username": str, "text": str, "time": float},
            ]
    }
    """
    after = float(request.args.get('after'))
    #
    # filtered_messages = []
    # for message in messages:
    #     if message['time'] > after:
    #         filtered_messages.append(message)

    filtered_messages = [message for message in messages if message['time'] > after]
    return {
        'messages': filtered_messages,
    }

app.run()
