#!/usr/bin/python3

import socket

if __name__ == "__main__":
	raise Exception("You cannot run this file directly")

import socket

class Player(object):
	
	def __init__(self, socket, nick):
		self.socket = socket
		self.room = None
		self.id = id(self)
		self.nick = nick
		self.data = {}
		
	def addToRoom(self, room):
		self.room = room
		return self
	
	def removeFromRoom(self):
		self.room = None
		return self
	
	def setNick(self, nick):
		self.nick = nick
		return self
	
	def sendMessage(self, data):
		print(data)
		pass

"""
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ja = Player(s)
print(ja.addToRoom(s))
"""
