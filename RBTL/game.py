import os
import random
import threading
import time


class Player:

	def __init__(self, name):
		self.name = name


class Room:

	def __init__(self, hostID, name, socket):

		self.players = {}
		self.player_names = set()
		self.hostID = hostID
		self.name = name
		self.active = False
		self.socket = socket

	def addPlayer(self, playerID, player_name):

		if self.active or player_name in self.player_names: return 0
		if player_name in self.player_names: return 1

		self.players[playerID] = Player(name = player_name)
		self.player_names.add(player_name)
		return 2

	def info(self):

		return {'room_name': self.name,	'host': self.players[self.hostID].name}

	def startGame(self):

		self.active = True
		self.mainThread = threading.Thread(target = self.gameLoop)

		self.mainThread.start()

	def get_madlib(self): # TEMPORARY FUNCTION

		return 'The cat sat on the _ while the _ went for a _, in the _.'

	def fill_madlib(self, data):

		index = data['index']
		if index in self.filledIndexes: return 0

		# get client ID
		# send filled in message for them -> edit the player_names to a dict carefully
		socket.emit('playerFilledIndex', room = data['user'])



	def gameLoop(self):

		while self.active: 

			self.filledIndexes = {}

			self.socket.emit('roundStart', data = {'madlib': self.get_madlib()}, room = self.name)
			time.sleep(15)

			self.socket.emit('votingStart', data = {}, room = self.name)
			time.sleep(5)

			self.socket.emit('roundResults', data = {}, room = self.name)
			time.sleep(3)

			# send round starting message
			# wait for input
			# return filled out message
			# evaluate votes
			# return votes + announce winner of round
			# restart

		# gameOver msg


		

