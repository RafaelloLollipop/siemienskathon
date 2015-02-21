#!/usr/bin/python3
import socket

if __name__ == "__main__":
	raise Exception("You cannot run this file directly")

import socket

class Player(object):
	
	def __init__(self, socket):
		self.socket = socket
		self.room = None
		
	def addToRoom(self, room):
		self.room = room
		return self
	
	def removeFromRoom(self):
		self.room = None
		return self

"""
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ja = Player(s)
print(ja.addToRoom(s))
"""
