"""
Prebuilt decks
"""
from card_game.card import Card, Deck
import card_game.constants as constants

__all__ = ["DECK_SIMPLE"]

CARDS_SIMPLE = []
for c in constants.CARD_COLORS:
	for v in constants.CARD_VALUES:
		CARDS_SIMPLE.append(Card(v, c))

DECK_SIMPLE = Deck("simple deck", CARDS_SIMPLE)