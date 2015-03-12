#!/usr/bin/python3

import socket

if __name__ == "__main__":
    raise Exception("You cannot run this file directly")

class Team(object):
    def __init__(self):
        self.players = []
        self.id = id(self)
        self.name = False
    
    def addPlayer(self, player):
        self.players.append(player)
        player.team = self
        return self
    
    def removePlayer(self, player):
        try:
            index = self.players.index(player)
            player.team = None
            del self.players[index]
        except KeyError:
            return True
