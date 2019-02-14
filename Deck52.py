import random

class Card:
	suit_allowed = ["Hearts", "Diamonds", "Clubs", "Spades"]
	rank_allowed = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

	def __init__(self, rank, suit):
		# Setting up the rank and suit of the card. 
		# Input can either be a string aligning to the full suit name and card rank abreviation.
		# Or can be a number representing card rank. A = 1, K = 13. Hearts = 1, Spades = 4.
		if (suit not in Card.suit_allowed and 
			suit not in list(range(1,len(Card.suit_allowed)+1))):
			raise ValueError("Invalid Suit2!")
		if (rank not in Card.rank_allowed and 
			rank not in list(range(1,len(Card.rank_allowed)+1))):
			raise ValueError("Invalid Card rank!")
		if type(suit) == int: 
			self.suit = Card.suit_allowed[suit - 1]
			self.suit_value = suit
		else:
			self.suit = suit
			self.suit_value = Card.suit_allowed.index(suit) + 1
		if type(rank) == int:
			self.rank = Card.rank_allowed[rank - 1]
			self.value = rank
			if self.value > 10: self.value=10
		else:
			self.rank = rank
			self.value = Card.rank_allowed.index(rank) + 1
			if self.value > 10: self.value=10

	def __repr__(self):
		return "%s of %s" % (self.rank, self.suit)


class Deck:
	cardset = []
	for n in range(len(Card.suit_allowed)):
		for m in range(len(Card.rank_allowed)):
			cardset.append(Card(Card.rank_allowed[m], Card.suit_allowed[n]))

	def __init__(self,cards=cardset.copy(),copies=1):
		self.cards = cards*copies
		self.count = len(self.cards)
		self.full_deck_size = len(self.cards)
		self.dealt_cards = []

	def __repr__(self):
		return "Deck of %s cards"  % self.count

	def iter(self):
		for card in self.cards:
			yield card

	def _deal(self,num):
		if self.count == 0:
			raise ValueError("All the cards have been dealt")
		if num <= self.count:
			hand = []
			for i in range(num):
				hand.append(self.cards.pop())
				self.count -= 1
		else: 
			hand = self.cards
			self.cards = []
			self.count = 0
		self.dealt_cards.append(hand)
		return hand

	def shuffle(self):
		if len(self.cards) == self.full_deck_size:
			random.shuffle(self.cards)
			random.shuffle(self.cards)
		else:
			raise ValueError("Only full decks can be shuffled.")

	def deal_card(self):
		h = self._deal(1)
		return h[0]

	def deal_hand(self,num):
		h = self._deal(num)
		return h



#x = Card("A","Spades")
#print(x)

