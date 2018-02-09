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
	return Deck("simple deck", CARDS_SIMPLE)

def GET_UNO_DECK():
	"""
	"""
	cards = []
	cards.extend(CARDS_SIMPLE)
	cards.extend(CARDS_ACTION)
	return Deck("uno deck", cards)

CARDS_SIMPLE = []
for c in constants.CARD_COLORS:
	for v in constants.CARD_VALUES:
		card = Card(v, c)
		# add the play card action to each card
		card.actions.append(Action(card, "Play Card", [PlayCard]))
		CARDS_SIMPLE.append(card)

# get all action cards for every color
CARDS_ACTION = []
for col in constants.CARD_COLORS:
	# reverse
	card = Card(constants.CARD_REVERSE, col)
	card.actions.append(Action(card, "Reverse", [PlayCard, Reverse]))
	CARDS_ACTION.append(card)
	# skip
	card = Card(constants.CARD_SKIP, col)
	card.actions.append(Action(card, "Skip", [PlayCard, Skip]))
	CARDS_ACTION.append(card)
	# draw two
	card = Card(constants.CARD_DRAW_TWO, col)
	card.actions.append(Action(card, "Draw two", [PlayCard, PlusTwo]))
	CARDS_ACTION.append(card)
	# wild card
	card = Card(constants.CARD_WILD, constants.CARD_BLACK)
	card.actions.append(Action(card, "Change to Blue", [PlayCard, ChangeSuitBlue]))
	card.actions.append(Action(card, "Change to Red", [PlayCard, ChangeSuitRed]))
	card.actions.append(Action(card, "Change to Yellow", [PlayCard, ChangeSuitYellow]))
	card.actions.append(Action(card, "Change to Purple", [PlayCard, ChangeSuitPurple]))
	CARDS_ACTION.append(card)
	# draw four
	card = Card(constants.CARD_DRAW_FOUR, constants.CARD_BLACK)
	card.actions.append(Action(card, "Draw four Blue", [PlayCard, ChangeSuitBlue, PlusFour]))
	card.actions.append(Action(card, "Draw four Red", [PlayCard, ChangeSuitRed, PlusFour]))
	card.actions.append(Action(card, "Draw four Yellow", [PlayCard, ChangeSuitYellow, PlusFour]))
	card.actions.append(Action(card, "Draw four Purple", [PlayCard, ChangeSuitPurple, PlusFour]))
	CARDS_ACTION.append(card)