"""
Prebuilt decks
"""
from card_game.card import Card, Deck
import card_game.constants as constants

__all__ = ["GET_SIMPLE_DECK"]

def GET_SIMPLE_DECK():
	"""
	because otherwise the deck runs out of cards and my unit tests start to fail
	"""
	return Deck("simple deck", CARDS_SIMPLE)


CARDS_SIMPLE = []
for c in constants.CARD_COLORS:
	for v in constants.CARD_VALUES:
		CARDS_SIMPLE.append(Card(v, c))
