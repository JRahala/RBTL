from flask import Flask, render_template, jsonify, request
from flask_socketio import *

import uuid
import time
import threading 

from game import *

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}
rooms = {}


@app.route('/')
def index():
	return render_template('index.html')

''' Room functions '''

@socketio.on('createRoom')
def createRoom(data):

	clientID = request.sid
	clients[clientID] = [data]

	if data['room'] in rooms:
		socketio.emit('roomError', data = {'error': 'Room name is taken :('}, room = clientID)
		return 0

	room = Room(hostID = clientID, name = data['room'], socket = socketio)
	room.addPlayer(playerID = clientID, player_name = data['username'])

	rooms[data['room']] = room

	join_room(data['room'])
	socketio.emit('joinedRoom', room = clientID)
	socketio.emit('roomInfo', data = room.info(), room = clientID)


@socketio.on('joinRoom')
def joinRoom(data):

	clientID = request.sid
	clients[clientID] = [data]
	
	if not data['room'] in rooms:
		socketio.emit('roomError', data = {'error': 'Room does not exist :('}, room = clientID)
		return 0

	room = rooms[data['room']]
	response = room.addPlayer(playerID = clientID, player_name = data['username'])

	if response == 0:
		socketio.emit('roomError', data = {'error': 'Name is taken :/'}, room = clientID)
		return 0

	elif response == 1: 
		socketio.emit('roomError', data = {'error': 'Room is in game [get better friends] :/'}, room = clientID)
		return 0

	join_room(data['room'])
	socketio.emit('joinedRoom', room = clientID)
	socketio.emit('roomInfo', data = room.info(), room = clientID)


''' Chatting functions '''

@socketio.on('chatSend')
def chatSend(data):

	socketio.emit('chatRecieve', data = data, room = data['user']['room'], broadcast = True)


''' Game Loop functions '''

@socketio.on('startGame')
def startGame(data):

	socketio.emit('gameStarted', data = data, room = data['room'])
	room = data['room']
	room = rooms[room]

	room.startGame()

@socketio.on('fillMadlib')
def fillMadlib(data):

	room = data['room']
	room = rooms[room]

	result = room.fillMadlib(data)
	

if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', port = 5000, debug = True)
