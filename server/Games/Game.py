#!/usr/bin/python3

import json
import os
import glob

if __name__ == "__main__":
	raise Exception("You cannot run this file directly")

class Game(object):
	def __init__(self):
		self.data = {
			"name" : "",
			"description" : "",
			"author" : "",
			"version" : ""
		}
		self.filename = ""
		print(self.data)
		raise Exception("Init function not implement in game %s v.%s by %s" %(self.data['name'], self.data['version'], self.data['author']))
		pass
	def start(self):
		raise Exception("Start function not implement in game %s v.%s by %s" %(self.data['name'], self.data['version'], self.data['author']))
		pass
	
	def destroy(self):
		raise Exception("Destroy function not implement in game %s v.%s by %s" %(self.data['name'], self.data['version'], self.data['author']))
		pass
	
	def load(self):
		try:
			if not self.filename:
				raise Exception("Filename must be set to properly relative path without extension")
		except AttributeError:
			raise Exception("Filename must be set to properly relative path without extension")
		try:
			self.data = json.load(open("%s.json" %self.filename));
		except:
			raise Exception("%s.json have bad JSON format" %self.filename)
		pass
	
	@staticmethod
	def getGamesArray():
		games = []
		for file in glob.glob("*.json"):
			if(file):
				try:
					games.append(json.load(open(file)))
				except ValueError as e:
					print("%s have bad JSON format" %file)
		return games
