"""
manual testing area
"""
from card_game import constants
from card_game.player import Player
from card_game.util import Logger
from card_game.engine import GameManager
from card_game.rules import SimpleRules
from card_game.data.decks import DECK_SIMPLE

def main():
	# set up all the things necessary to run the game
	player1 = Player("Jason")
	player2 = Player("Kelly")
	player3 = Player("Garth")
	players = [player1, player2, player3]

	gm = GameManager(players, DECK_SIMPLE, SimpleRules)

	constants.DEBUG = False
	gm.run()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		Logger.debug("Game Over", "GAME")
