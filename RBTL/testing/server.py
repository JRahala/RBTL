# what is the difference between emitting and sending, since sending did not work???

import flask
from flask import Flask, render_template, jsonify

from flask_socketio import *
import threading
import time

threads = {}

app = Flask(__name__)
socketio = SocketIO(app)

def task():
	print('Thread started')
	time.sleep(1)
	socketio.emit('task_fin')

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('join_game')
def join_game(json):
    print('received json: ' + str(json))
    room = json['room']    
    join_room(room)
    emit('new_user', json, room=room)

@socketio.on('host_game')
def host_game(json):
    print('received json: ' + str(json))
    room = json['room']    
    join_room(room)
    emit('new_user', json, room=room)

@socketio.on('connect')
def connected():
	print('User connected')

@socketio.on('send_msg')
def send_msg(json):
	print('Sending message')
	room = json['room']
	emit('recieve_msg', json, room=room)

@socketio.on('start_task')
def start_task(json):
	print('Starting task')
	new_thread = threading.Thread(target=task)
	threads[json['user']] = new_thread
	new_thread.start()




if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', port = 5000)