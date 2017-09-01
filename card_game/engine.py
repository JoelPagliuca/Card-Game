"""
All the code that makes the game run
"""
import random

import constants
from card import Pile, Card
from util import *

__all__ = ["GameManager", "TextInterface"]

class GameManager(object):
	"""
	Runs the game
	"""
	TAG = "GAMEMANAGER"

	def __init__(self, players, deck, rules):
		"""
		:type players: list
		:type deck: Deck
		:type rules: Rules
		"""
		self.players = []
		self.players.extend(players)
		self._current_player = 0
		self._direction = 1
		self.deck = deck
		self.pile = Pile()
		self.rules = rules
		self._context = {}
		self.interface = TextInterface # FIXME do this better
	
	def next_player(self):
		"""
		change the current player
		"""
		self._current_player = (self._current_player + self._direction + len(self.players)) % len(self.players)
	
	def current_player(self):
		"""
		get the current player in the list
		:rtype: Player
		"""
		return self.players[self._current_player]
	
	def change_direction(self):
		self._direction *= -1
	
	def who_shuffled(self):
		"""
		deal an appropriate amount of cards to each player
		FIXME: make sure num_cards is a reasonable number
		"""
		num_cards = self.rules.cards_to_deal(self._context)
		for p in self.players:
			for _ in range(num_cards):
				p.take_card(self.deck.draw_card())
	
	def shuffle(self):
		"""
		shuffle the pile back into the deck
		"""
		self.deck.restock(self.pile.take_cards())

	def _preRun(self): # pragma: no cover
		"""
		set the game up ready to play
		"""
		self._current_player = 0
		self._context[constants.CONTEXT_PLAYERS] = self.players
		self.who_shuffled()
		self.pile.play_card(self.deck.draw_card())
		Logger.debug("starting game", self.TAG)
	
	def get_options(self, player):
		"""
		figure out what options to present to the user
		:type player: Player
		:rtype: list
		"""
		options = []
		for card in player.hand:
			if self.rules.can_be_played(card, self._context):
				options.append(card)
		options.append(constants.CHOICE_DRAW_CARD)
		return options

	def display_status(self): #pragma: no cover
		self.interface.render("Current turn: "+self.current_player().name)
		self.interface.render("Top card: "+str(self.pile.top_card()))
	
	def update_state(self):
		self._context[constants.CONTEXT_TOP_CARD] = self.pile.top_card()

	def run(self): # pragma: no cover
		"""
		Play the game
		:return: the game context
			this is to allow some anaytics to happen
		:rtype: dict
		"""
		self._preRun()
		while True:
			self.display_status()
			self.update_state()
			# get current player
			player = self.current_player()
			# get list of valid options for player
			options = self.get_options(player)
			# get option from player
			Logger.debug("Asking "+player.name+" for choice", self.TAG)
			choice = self.interface.get_choice(options, "Choose an action: ")
			# act on that option
			Logger.debug("Got option \""+str(options[choice])+'"', self.TAG)
			option = options[choice]
			action_type = type(option) # FIXME: don't do this
			if action_type is str:
				Logger.debug("Going to draw another card", self.TAG)
				player.take_card(self.deck.draw_card())
			elif action_type is Card:
				Logger.debug("Going to play a card")
				player.hand.remove(option)
				self.pile.play_card(option)
			# check for winner, break if there is one
			winner = self.rules.check_for_win(self._context)
			if winner:
				self._context[constants.CONTEXT_WINNER] = winner
				break
			self.next_player()
			# check if there's cards left in the deck
			if self.deck.need_to_shuffle():
				Logger.debug("shuffling", self.TAG)
				self.shuffle()
			self.interface.render("")
		return self._context

class TextInterface(object):
	"""
	Gets user input over terminal
	"""
	TAG = "INTERFACE"
	@classmethod
	def render(cls, msg): # pragma: no cover
		print msg
	
	@classmethod
	def get_input(cls, prompt=None):
		"""
		gets a string from the user
		:type prompt: str
		:rtype: str
		"""
		Logger.debug("Taking input from user", cls.TAG)
		return raw_input(prompt)

	@classmethod
	def get_int(cls, prompt=None):
		output = None
		while not output:
			output = None
			try:
				output = int(cls.get_input(prompt))
				Logger.debug("Got "+str(output), cls.TAG)
			except ValueError:
				Logger.debug("That was not an integer", cls.TAG)
		return output
	
	@classmethod
	def get_choice(cls, options, prompt=""):
		"""
		get a choice from a user
		user will see choices in 1 indexed form
		:param options: list of descriptions to present to the user
		:type options: list
		:return: the item chosen from the list (0 index)
		:rtype: int
		"""
		for i in range(len(options)):
			print "{}: {}".format(str(i+1), options[i])
		choice = -1
		while not choice in range(len(options)):
			choice = cls.get_int(prompt)-1
		return choice
