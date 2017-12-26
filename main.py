"""
manual testing area
"""
import logging

from card_game import constants
from card_game.player import Player
from card_game.engine import GameManager
from card_game.rules import MelbourneRules as RULES
from card_game.data.decks import GET_UNO_DECK as GET_DECK

def main():
	# set up all the things necessary to run the game
	player1 = Player("Jason")
	player2 = Player("Kelly")
	player3 = Player("Garth")
	players = [player1, player2, player3]

	gm = GameManager(players, GET_DECK(), RULES)

	constants.DEBUG = False
	gm.run()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		logging.debug("Game Over")
