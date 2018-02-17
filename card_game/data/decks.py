"""
Prebuilt decks using constants.py
"""
from card_game.card import Card, Deck
from card_game.action import *
import card_game.constants as constants

__all__ = ["GET_SIMPLE_DECK", "GET_UNO_DECK"]

def GET_SIMPLE_DECK():
	"""
	because otherwise the deck runs out of cards and my unit tests start to fail
	"""
	return Deck("simple deck", GET_SIMPLE_CARDS())

def GET_UNO_DECK():
	"""
	"""
	cards = []
	cards.extend(GET_SIMPLE_CARDS())
	cards.extend(GET_ACTION_CARDS())
	return Deck("uno deck", cards)

def GET_SIMPLE_CARDS():
	output = []
	for c in constants.CARD_COLORS:
		for v in constants.CARD_VALUES:
			card = Card(v, c)
			# add the play card action to each card
			card.actions.append(Action(card, "Play Card", [PlayCard]))
			output.append(card)
	return output

# get all action cards for every color
def GET_ACTION_CARDS():
	output = []
	for col in constants.CARD_COLORS:
		# reverse
		card = Card(constants.CARD_REVERSE, col)
		card.actions.append(Action(card, "Reverse", [PlayCard, Reverse]))
		output.append(card)
		# skip
		card = Card(constants.CARD_SKIP, col)
		card.actions.append(Action(card, "Skip", [PlayCard, Skip]))
		output.append(card)
		# draw two
		card = Card(constants.CARD_DRAW_TWO, col)
		card.actions.append(Action(card, "Draw two", [PlayCard, PlusTwo]))
		output.append(card)
		# wild card
		card = Card(constants.CARD_WILD, constants.CARD_BLACK)
		card.actions.append(Action(card, "Change to Blue", [PlayCard, ChangeSuitBlue]))
		card.actions.append(Action(card, "Change to Red", [PlayCard, ChangeSuitRed]))
		card.actions.append(Action(card, "Change to Yellow", [PlayCard, ChangeSuitYellow]))
		card.actions.append(Action(card, "Change to Purple", [PlayCard, ChangeSuitPurple]))
		output.append(card)
		# draw four
		card = Card(constants.CARD_DRAW_FOUR, constants.CARD_BLACK)
		card.actions.append(Action(card, "Draw four Blue", [PlayCard, ChangeSuitBlue, PlusFour]))
		card.actions.append(Action(card, "Draw four Red", [PlayCard, ChangeSuitRed, PlusFour]))
		card.actions.append(Action(card, "Draw four Yellow", [PlayCard, ChangeSuitYellow, PlusFour]))
		card.actions.append(Action(card, "Draw four Purple", [PlayCard, ChangeSuitPurple, PlusFour]))
		output.append(card)
	return output