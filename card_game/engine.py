"""
All the code that makes the game run
"""
import random
import logging

import constants
from card import Pile, Card
from util import *

__all__ = ["GameManager", "TextInterface"]

class GameManager(object):
	"""Runs the game and maintains game-state

	:ivar list(Player) players: list of players in the game
	:ivar Deck deck: deck being used in-game
	:ivar Pile pile: pile of cards for the game
	:ivar Rules rules: ruleset for the game
	:ivar TextInterface interface: umm, probably can take this away TODO
	:ivar bool running: is the game running?
	"""

	def __init__(self, players, deck, rules):
		"""
		:param players:
		:type players: list(:class:`card_game.player.Player`)
		:param deck:
		:type deck: :class:`card_game.card.Deck`
		:param rules:
		:type rules: :class:`card_game.rules.Rules`
		"""
		self.players = []
		self.players.extend(players)
		self._current_player = 0
		self._direction = 1
		self.deck = deck
		self.pile = Pile()
		self.rules = rules
		self._context = {}
		self.interface = TextInterface
		self.running = False
		self._observers = []
	
	def get_context(self):
		"""
		:rtype: dict
		"""
		return self._context
	
	def next_player(self):
		"""change the current player"""
		self._current_player = (self._current_player + self._direction + len(self.players)) % len(self.players)
	
	def current_player(self):
		"""
		get the current player in the list
		
		:rtype: :class:`card_game.player.Player`
		"""
		return self.players[self._current_player]
	
	def change_direction(self):
		self._direction *= -1
	
	def who_shuffled(self):
		"""
		deal an appropriate amount of cards to each player
		"""
		to_deal = self.rules.cards_to_deal(self._context)
		assert self.deck.num_cards() > to_deal*len(self.players), "You tried to deal out too many cards"
		for p in self.players:
			for _ in range(to_deal):
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
		self._context[constants.CONTEXT.PLAYERS] = self.players
		self._context[constants.CONTEXT.CURRENT_EFFECT] = None
		self._context[constants.CONTEXT.CURRENT_EFFECT_VALUE] = 0
		self.who_shuffled()
		self.pile.play_card(self.deck.draw_card())
		logging.debug("starting game")
		self.running = True
	
	def display_status(self): #pragma: no cover
		"""TODO deprecated"""
		self.interface.render("##############################")
		self.interface.render("# Current turn: "+self.current_player().name)
		self.interface.render("# Top card: "+str(self.pile.top_card()))
		self.interface.render("##############################")
	
	def update_state(self):
		"""update things that need to every turn"""
		self._context[constants.CONTEXT.TOP_CARD] = self.pile.top_card()
		self._context[constants.CONTEXT.CURRENT_PLAYER] = self.current_player()
	
	def observe(self, observer):
		"""
		add the observer to the list, observer must have a .update

		:param object observer:
		"""
		update_method = getattr(observer, "update")
		assert callable(update_method)
		self._observers.append(observer)
	
	def deleteObserver(self, observer):
		"""
		remove observer from list

		:param object observer:
		"""
		if observer in self._observers:
			self._observers.remove(observer)
	
	def update_observers(self):
		"""give all the observers the updated game state"""
		for o in self._observers:
			o.update(self._context)

	def run(self): # pragma: no cover
		"""
		Play the game

		:return: the game context, this is to allow some anaytics to happen
		:rtype: dict
		"""
		self._preRun()
		while self.running:
			self.update_state()
			self.update_observers()
			# get current player
			player = self.current_player()
			# get list of valid options for player
			options = self.rules.get_options(player, self._context)
			# get option from player
			logging.debug("Asking "+player.name+" for choice")
			choice = self.interface.get_choice(options, "Choose an action: ", player)
			# act on that option
			logging.debug("Got option \""+str(choice)+'"')
			logging.debug("Running action "+str(choice.__class__.__name__))
			choice.run(self)
			# check for winner, break if there is one
			winner = self.rules.check_for_win(self._context)
			if winner:
				self._context[constants.CONTEXT.WINNER] = winner
				self.running = False
			self.next_player()
			# check if there's cards left in the deck
			if self.deck.need_to_shuffle():
				logging.debug("shuffling")
				self.shuffle()
		logging.debug("Game ended")
		return self._context

class TextInterface(object):
	"""Interacts with user over terminal"""
	@classmethod
	def render(cls, msg): # pragma: no cover
		"""
		display a string

		:param str msg:
		"""
		print msg
	
	@classmethod
	def get_input(cls, prompt=None, player=None):
		"""
		gets a string from the **correct** user

		:param str prompt:
		:param player: the user to get data from (makes more sense with multiple possible connections)
		:type player: :class:`card_game.player.Player`
		:rtype: str
		"""
		logging.debug("Taking input from user")
		return raw_input(prompt)

	@classmethod
	def get_int(cls, prompt=None, player=None):
		"""
		:rtype: int
		"""
		output = None
		while not output:
			output = None
			try:
				output = int(cls.get_input(prompt, player))
				logging.debug("Got "+str(output))
			except ValueError:
				logging.debug("That was not an integer")
		return output
	
	@classmethod
	def get_choice(cls, options, prompt="", player=None):
		"""
		get a choice from a user, choices displayed in 1-indexed form

		:param options: list of descriptions to present to the user
		:type options: list(:class:`card_game.action.Action`)
		:return: the action chosen from the list
		:rtype: :class:`card_game.actions.Action`
		"""
		for i in range(len(options)):
			cls.render("{}: {}".format(str(i+1), options[i]))
		choice = -1
		while not choice in range(len(options)):
			choice = cls.get_int(prompt, player)-1
		return options[choice]
