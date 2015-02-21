#!/usr/bin/python3

from Games.Game import Game
import time
import random
from math import ceil, floor;

if __name__ == "__main__":
	raise Exception("You cannot run this file directly")

class Demo(Game):
	def __init__(self, players):
		self.filename = "Games/Demo"
		self.load()
		self.players = players
		self.players
		
	def addPlayer(self, player):
		self.players.append(player)
		return self
	
	def start(self):
		self.preparePlayers()
		return self
	
	def preparePlayers(self):
		values = []
		
		for player in self.players:
			player.data['dataGame'] = {"summary": random.randint(5,15)}
			tmp = self.randomizeValues(player.data['dataGame']['summary']) + self.randomizeValues(player.data['dataGame']['summary'])
			player.data['dataGame']['count'] = len(tmp)
			values = values + tmp
		
		random.shuffle(values)
		
		for player in self.players:
			player.data['dataGame']['values'] = values[0:player.data['dataGame']['count']]
			values = values[player.data['dataGame']['count']:]
		
		for player in self.players:
			print(player.data)
			
		return self
			
	
	def randomizeValues(self,summary):
		ret = []
		remain = summary
		while remain > 0:
			number = round(random.normalvariate(floor(summary/3), summary/3))
			if number > 0:
				if number >= remain:
					number = remain
				remain = remain - number
				ret.append(number)
		if len(ret) > summary/2:
			return self.randomizeValues(summary)
		return ret
	
	def destroy(self):
		pass

"""
players = [ {"name" : "player"}, {"name" : "player2"} ]
demo = Demo(players);
demo.start()
demo.destroy()
print(Game.getGamesArray())
"""
