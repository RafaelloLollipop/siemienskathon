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
		self.playable = False
		self.started = False
		self.winner = False
		
	def addPlayer(self, player):
		self.players.append(player)
		return self
	
	def doAction(self, data):
		print(data)
		update = False
		try:
			player = self.getPlayerById(data['from'])
		except KeyError:
			player = False
		
		try:
			value = data['value']
		except KeyError:
			value = False
			
		default = {
			"action": "none"
		}
		
		if not self.playable:
			if not self.started:
				pass
			else:
				if player:
					player.sendMessage({
						"gameStatus": "end",
						"action": "updateStatus",
						"winner": self.winner,
					})
			update = True
		
		if data['action'] == "start":
			if not self.playable:
				self.start()
				for player in self.players:
					player.sendMessage({
						"action": "updateStatus",
						"gameStatus": "playable",
						"playerData": self.getPlayerUpdate(player)
					})
			update = True
			
		elif data['action'] == "moveValueToWeight":
			try:
				weight = data['weight']
			except KeyError:
				weight = False
				
			if weight and player and value:
				data['success'] = self.moveValueToWeight(player, value, weight)
			else:
				data['success'] = False
				
			data['playerData'] = self.getPlayerUpdate(player)
			
			if player:
				player.sendMessage(data)
			update = True
				
		elif data['action'] == "moveValueFromWeight":
			try:
				weight = data['weight']
			except KeyError:
				weight = False
				
			if weight and player and value:
				data['success'] = self.moveValueFromWeight(player, value, weight)
			else:
				data['success'] = False
				
			data['playerData'] = self.getPlayerUpdate(player)
			
			if player:
				player.sendMessage(data)
			update = True
				
		elif data['action'] == "setProposition":
			try:
				playerTo = self.getPlayerById(data['to'])
			except KeyError:
				playerTo = False
				
			if playerTo and player and value:
				data['success'] = self.setProposition(player, playerTo, value)
			else:
				data['success'] = False
			
			if player and playerTo:
				data['playerData'] = self.getPlayerUpdate(player)
				player.sendMessage(data)
				data['action'] = "update"
				data['playerData'] = self.getPlayerUpdate(playerTo)
				playerTo.sendMessage(data)
			update = True
				
		elif data['action'] == "removeProposition":
			try:
				playerTo = self.getPlayerById(data['to'])
			except KeyError:
				playerTo = False
				
			if playerTo and player and value:
				data['success'] = self.removeProposition(player, playerTo, value)
			else:
				data['success'] = False
			
			if player and playerTo:
				data['playerData'] = self.getPlayerUpdate(player)
				player.sendMessage(data)
				data['action'] = "update"
				data['playerData'] = self.getPlayerUpdate(playerTo)
				playerTo.sendMessage(data)
			update = True
		
		if update:
			if self.checkWinStatement():
				for player in players:
					player.sendMessage({
						"gameStatus": "end",
						"action": "updateStatus",
						"winner": self.winner
					})
			return True
		
		return False
	
	def start(self):
		self.prepareTeams()
		self.preparePlayers()
		self.winner = False
		self.playable = True
		self.started = True
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
			return True
		except ValueError:
			return False
	
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
		#print(self.checkWinStatement())
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
	
	def checkWinStatement(self):
		if self.winner:
			return True
		if not self.playable:
			return False
		for team in self.teams:
			win = True
			for player in team.players:
				if sum(player.data['dataGame']['weight1']) == player.data['dataGame']['summary'] and sum(player.data['dataGame']['weight2']) == player.data['dataGame']['summary']:
					pass
				else:
					win = False
			if win:
				self.playable = False
				self.winner = team
				return True
		return False
	
	def getPlayerById(self, id_):
		ret = [player for player in self.players if id(player) == id_]
		if len(ret) == 1:
			return ret[0]
		return False
	
	def getPlayerUpdate(self, player):
		team = player.team
		return {
			"players": [{"name": player.nick, "id": player.id} for player in self.players if player.team == team],
			"values": player.data['dataGame']['values'],
			"weight1": player.data['dataGame']['weight1'],
			"weight2": player.data['dataGame']['weight2'],
			"from": [{"id": p.id, "value": player.data['dataGame']['propositions']['from'][p]} for p in player.data['dataGame']['propositions']['from'].keys()],
			"to": [{"id": p.id, "value": player.data['dataGame']['propositions']['to'][p]} for p in player.data['dataGame']['propositions']['to'].keys()]
		};
	
	def destroy(self):
		pass

"""
players = [ {"name" : "player"}, {"name" : "player2"} ]
demo = Demo(players);
demo.start()
demo.destroy()
print(Game.getGamesArray())
"""
