#!/usr/bin/python3

from Games.Game import Game
import time
import random
from math import ceil, floor;
from Team import Team

if __name__ == "__main__":
	raise Exception("You cannot run this file directly")

class Demo(Game):
	def __init__(self, players):
		self.filename = "Games/Demo"
		self.load()
		self.players = players
		self.teams = []
		
	def addPlayer(self, player):
		self.players.append(player)
		return self
	
	def doAction(self, action):
		message = {}
		return message
	
	def start(self):
		self.prepareTeams()
		self.preparePlayers()
		return self
	
	def prepareTeams(self, teamNumber = 2):
		random.shuffle(self.players)
		for i in range(teamNumber):
			self.teams.append(Team())
		counter = 0
		for player in self.players:
			self.teams[counter % teamNumber].addPlayer(player)
			counter = counter  + 1;
		return self
	
	def preparePlayers(self):
		for team in self.teams:
			values = []
			
			for player in team.players:
				player.data['dataGame'] = {"summary": random.randint(5,15), "propositions": {"from": {}, "to": {}}, "weight1": [], "weight2": []}
				tmp = self.randomizeValues(player.data['dataGame']['summary']) + self.randomizeValues(player.data['dataGame']['summary'])
				player.data['dataGame']['count'] = len(tmp)
				values = values + tmp
			
			random.shuffle(values)
			
			for player in team.players:
				player.data['dataGame']['values'] = values[0:player.data['dataGame']['count']]
				values = values[player.data['dataGame']['count']:]
			
			for player in team.players:
				print([player.nick, player.data, player.team.id])
			
		return self
	
	def moveValueToWeight(self, player, value, weight):
		try:
			index = player.data['dataGame']['values'].index(value)
			val = player.data['dataGame']['values'][index]
			weight.append(val)
			del player.data['dataGame']['values'][index]
			return self
		except ValueError:
			return self
	
	def moveValueFromWeight(self, player, value, weight):
		try:
			index = weight.index(value)
			val = weight[index]
			player.data['dataGame']['values'].append(val)
			del weight[index]
			return self
		except ValueError:
			return self
	
	def setProposition(self, playerFrom, playerTo, value):
		try:
			tmp = playerFrom.data['dataGame']['propositions']['to'][playerTo] or playerTo.data['dataGame']['propositions']['from'][playerFrom]
			return False
		except KeyError:
				try:
					index = playerFrom.data['dataGame']['values'].index(value)
					playerFrom.data['dataGame']['propositions']['to'][playerTo] = playerFrom.data['dataGame']['values'][index]
					playerTo.data['dataGame']['propositions']['from'][playerFrom] = playerFrom.data['dataGame']['values'][index]
					del playerFrom.data['dataGame']['values'][index];
					try:
						valueToPlayerFrom = playerTo.data['dataGame']['propositions']['to'][playerFrom]
						valueToPlayerTo = playerFrom.data['dataGame']['propositions']['to'][playerTo]
						playerTo.data['dataGame']['values'].append(valueToPlayerTo)
						playerFrom.data['dataGame']['values'].append(valueToPlayerFrom)
						del playerTo.data['dataGame']['propositions']['to'][playerFrom]
						del playerTo.data['dataGame']['propositions']['from'][playerFrom]
						del playerFrom.data['dataGame']['propositions']['to'][playerTo]
						del playerFrom.data['dataGame']['propositions']['from'][playerTo]
						return True
					except KeyError:
						pass
					return True
				except ValueError:
					return False
	
	def removeProposition(self, playerFrom, playerTo):
		try:
			valueFrom = playerFrom.data['dataGame']['propositions']['to'][playerTo]
			playerFrom.data['dataGame']['values'].append(valueFrom)
			del playerFrom.data['dataGame']['propositions']['to'][playerTo]
			del playerTo.data['dataGame']['propositions']['from'][playerFrom]
			return True
		except KeyError:
			return False
			
	
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
