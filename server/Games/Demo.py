#!/usr/bin/python3

from Game import Game

if __name__ == "__main__":
	raise Exception("You cannot run this file directly")

class Demo(Game):
	def __init__(self, players):
		self.filename = "Demo"
		self.load()
		self.players = players
	def start(self):
		print("players in game")
		for player in self.players:
			print(player['name'])
	def destroy(self):
		pass

"""
players = [ {"name" : "player"}, {"name" : "player2"} ]
demo = Demo(players);
demo.start()
demo.destroy()
print(Game.getGamesArray())
"""
