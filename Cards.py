import random

class Card:
	suit_allowed = ["Hearts", "Diamonds", "Clubs", "Spades"]
	number_allowed = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

	def __init__(self, number, suit):
		# Setting up the number and suit of the card. 
		# Input can either be a string aligning to the full suit name and card number abreviation.
		# Or can be a numerical number representing card number. A = 1, K = 13. Hearts = 1, Spades = 4.
		if (suit not in Card.suit_allowed and 
			suit not in list(range(1,len(Card.suit_allowed)+1))):
			raise ValueError("Invalid Suit2!")
		if (number not in Card.number_allowed and 
			number not in list(range(1,len(Card.number_allowed)+1))):
			raise ValueError("Invalid Card number!")
		if type(suit) == int: 
			self.suit = Card.suit_allowed[suit - 1]
			self.suit_value = suit
		else:
			self.suit = suit
			self.suit_value = Card.suit_allowed.index(suit) + 1
		if type(number) == int:
			self.number = Card.number_allowed[number - 1]
			self.value = number
		else:
			self.number = number
			self.value = Card.number_allowed.index(number) + 1

	def __repr__(self):
		return "%s of %s" % (self.number, self.suit)


class Deck:
	cardset = []
	for n in range(len(Card.suit_allowed)):
		for m in range(len(Card.number_allowed)):
			cardset.append(Card(Card.number_allowed[m], Card.suit_allowed[n]))

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
		dealt_cards.append(hand)
		return hand

	def shuffle(self):
		if len(self.cards) == self.full_deck_size:
			random.shuffle(self.cards)
			random.shuffle(self.cards)
			print("Shuffled")
		else:
			raise ValueError("Only full decks can be shuffled.")

	def deal_card(self):
		h = self._deal(1)
		return h

	def deal_hand(self,num):
		h = self._deal(num)
		return h



#x = Card("A","Spades")
#print(x)

