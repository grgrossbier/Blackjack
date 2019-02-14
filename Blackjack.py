from Deck52 import Card, Deck
from player_login import PlayerLogin
import numpy as np
import pandas as pd
import math


class Hand:
	def __init__(self,deck,*args):
		self.cards = []
		self.count = 0
		self.bust = False
		self.blackjack = False
		self.soft = 0
		self.deck = deck
		for each in args:
			if type(each) != Card:
				raise ValueError("You must pass type 'cards' into your Hand()")
			else:
				self.cards.append(each)
				self.count += each.value
				if each.rank == "A":
					self.count += 10
					self.soft += 1
				if self.count == 21:
					self.blackjack = True
				self.check_count()
		labels = ['total', 'win', 'loss', 'push']
		self.results = pd.Series(np.array([1] + [0] *3), labels)
		self.actions = pd.Series(np.array([self.count_code(), [], 0, False]), ['first_count', 'hit_counts', 'stay_count', 'doubled'])

	def __repr__(self):
		return f"{self.cards} -- {'Soft' if self.soft > 0 else ''} {self.count}"

	def check_count(self):
		while self.count > 21 and self.soft > 0:
			self.soft -= 1
			self.count -= 10
		if self.count > 21: self.bust = True

	def add_card(self):
		new_card = self.deck.deal_card()
		self.cards.append(new_card)
		self.count += new_card.value
		if new_card.rank == "A":
			self.count += 10
			self.soft += 1
		self.check_count()

	def count_code(self):
		return self.count+self.soft*100


class Player:
	def __init__(self, profile, login=False):
		if login:
			self.login = True
			self.profile = profile
			self.name = profile.name
			self.bank = profile.bank
		else:
			self.login = False
			self.name = profile
			self.bank = 0
		self.reset_hands()
		self.computer_player = False

	def __repr__(self):
		return f"{self.name} is sitting at the table with {len(self.hands)} hand(s).\n He/She is betting {self.bets} and has {self.bank} in their pocket."

	def hit(self,hand_num=0):
		self.hands[hand_num].add_card()
		if self.hands[hand_num].bust == True:
			self.stay[hand_num] = True
		return

	def tell_stay(self,hand_num=0):
		self.stay[hand_num] = True
		return

	def split(self,hand_num=0):
		splitting = self.hands[hand_num].cards
		print("Splitting...")
		split_bet = self.bets[hand_num]
		deck = self.deck[hand_num]
		if len(splitting) > 2:
			print("Can't split a hand with more than 2 cards.\n")
			return
		if splitting[0].rank != splitting[1].rank:
			print("Can only split the same rank")
			return
		self.clear_hand(hand_num)
		self.bank -= split_bet
		self.bets.insert(hand_num,split_bet)
		self.bets.insert(hand_num,split_bet)
		self.get_hand(Hand(deck,splitting[0],deck.deal_card()),hand_num)
		self.get_hand(Hand(deck,splitting[1],deck.deal_card()),hand_num)
		self.hands[hand_num].actions['hit_counts'].append(splitting[0].value if splitting[0].rank != 'A' else 11)
		self.hands[hand_num+1].actions['hit_counts'].append(splitting[1].value if splitting[0].rank != 'A' else 11)
		return

	def get_hand(self,hand,i=None):
		if i != None and type(i) == int:
			self.hands.insert(i,hand)
			self.stay.insert(i,False)
			self.thinking.insert(i,True)
			self.deck.insert(i,hand.deck)
			self.doubled.insert(i,False)
			while len(self.hands) > len(self.bets):
				self.bets.insert(i,0)
		else:
			self.hands.append(hand)
			self.stay.append(False)
			self.thinking.append(True)
			self.deck.append(hand.deck)
			self.doubled.append(False)
			while len(self.hands) > len(self.bets):
				self.bets.append(0)
		return

	def bet(self,bet=-1,hand_num=0):
		if bet == -1:
			print(f"Current bet is {self.bets}")
			return
		if bool(self.hands) == False:
			self.bank -= bet
			self.bets.append(bet)
			if self.login: self.profile.bank = self.bank
		else:
			print("Can't bet after seeing your cards cheater...")
		return

	def double_down(self,hand_num=0):
		if len(self.hands[hand_num].cards) == 2 and self.doubled[hand_num] == False:
			self.bank -= self.bets[hand_num]
			self.bets[hand_num] *= 2
			self.doubled[hand_num] = True
		else:
			print("Can't double after hitting on a hand")
		return

	def auto_think(self,hand_num=0,soft17hit=False):
		if self.hands[hand_num].count > 17:
			self.stay[hand_num] = True
		if self.hands[hand_num].count == 17 and self.hands[hand_num].soft == 0:
			self.stay[hand_num] = True
		if self.hands[hand_num].count == 17 and self.hands[hand_num].soft > 0 and soft17hit == False:
			self.stay[hand_num] = True
		self.thinking[hand_num] = False
		return

	def result(self,hand_num=0,payment=0):
		self.clear_hand(hand_num)
		self.bank += payment

	def clear_hand(self, hand_num=0):
		del self.hands[hand_num]
		del self.stay[hand_num]
		del self.bets[hand_num]
		del self.thinking[hand_num]
		del self.deck[hand_num]
		del self.doubled[hand_num]

	def reset_hands(self):
		self.hands = []
		self.stay = []
		self.bets = []
		self.thinking = []
		self.deck = []
		self.doubled = []


class Dealer(Player):
	def __init__(self, name="House"):
		super().__init__(name)

	def get_hand(self,hand):
		self.hands.append(hand)
		self.stay.append(False)
		self.thinking.append(True)
		self.deck.append(hand.deck)
		self.doubled.append(False)
		self.bets.append(0)
		self.up_card = hand.cards[1]
		self.hole_card = hand.cards[0]

	def bet(self):
		print("Dealer doesn't bet")


class Machine_Learner(Player):
	def __init__(self, profile="Machine_Learner", login=False, strategy=(0, 0, 0, 0)):
		''' Strategy = (Insurance, Double, Split, Hit/Stay)'''
		super().__init__(profile, login)
		self.computer_player = True
		self.strategy = strategy

	def decide_bet(self, bet=10):
		return str(bet)

	def decide_insurance(self):
		strategy = self.strategy[0]
		"""  0 = Never Buy; 1 = Always Buy; 2 = Machine Learning Decision """
		if strategy == 0: return "no"
		elif strategy == 1:	return "yes"
		else:
			pass

	def decide_double_down(self, hand_num, up_card_value):
		strategy = self.strategy[1]
		"""  0 = Never Double; 1 = Always Double; 2 = Machine Learning Decision """
		if strategy == 0: return "no"
		elif strategy == 1:	return "yes"
		else:
			count_code = self.hands[hand_num].count_code()
			p_double = self.profile.player_df.loc[up_card_value].loc[count_code]['double_won'] / \
					 self.profile.player_df.loc[up_card_value].loc[count_code]['double_total']
			print(f"p_double = {p_double}")
			if p_double > .5 or p_double == 0 or math.isnan(p_double):
				print("Lets do it")
				return "yes"
			else:
				return "no"

	def decide_split(self, hand_num, up_card_value):
		strategy = self.strategy[2]
		"""  0 = Never Split; 1 = Always Split; 2 = Machine Learning Decision """
		if strategy == 0: return "no"
		elif strategy == 1:	return "yes"
		else:
			count_code = self.hands[hand_num].count_code()
			new_hand_val = self.hands[hand_num].cards[0].value
			if new_hand_val == 1: new_hand_val = 11
			p_split = self.profile.player_df.loc[up_card_value].loc[new_hand_val]['hit_won'] / self.profile.player_df.loc[up_card_value].loc[new_hand_val]['hit_total']
			p_stay = self.profile.player_df.loc[up_card_value].loc[count_code]['stay_won'] / self.profile.player_df.loc[up_card_value].loc[count_code]['stay_total']
			p_hit = self.profile.player_df.loc[up_card_value].loc[count_code]['hit_won'] / self.profile.player_df.loc[up_card_value].loc[count_code]['hit_total']
			p_keep = max([p_stay, p_hit])
			print(f"p_split:  {p_split}  --  p_keep:  {p_keep}")
			if p_split*2*2-1 > p_keep*2 or p_split == 0 or math.isnan(p_split):
				print("Split that shit")
				return "yes"
			else:
				return "no"


	def decide_hit_or_stay(self, hand_num, up_card_value):
		strategy = self.strategy[3]
		"""  0 = Always Stay;  1 = Always Hit; 3 = Dealer Strategy;  2 = Machine_Learning_Decision  """
		if strategy == 0: return "stay"
		elif strategy == 1:	return "hit"
		else:
			count_code = self.hands[hand_num].count_code()
			if self.profile.player_df.loc[up_card_value].loc[count_code]['hit_total'] == 0: return "hit"
			if self.profile.player_df.loc[up_card_value].loc[count_code]['stay_total'] == 0: return "stay"
			p_hit = self.profile.player_df.loc[up_card_value].loc[count_code]['hit_won'] / \
					self.profile.player_df.loc[up_card_value].loc[count_code]['hit_total']
			p_stay = self.profile.player_df.loc[up_card_value].loc[count_code]['stay_won'] / \
					 self.profile.player_df.loc[up_card_value].loc[count_code]['stay_total']
			print(f"p_hit:  {p_hit}  --  p_stay:  {p_stay}")
			if p_hit > p_stay or p_hit == 0 or math.isnan(p_hit):
				return "hit"
			else:
				return "stay"

class Game:
	def __init__(self, players, dealer=Dealer(), deck=Deck()):
		self.players = players
		self.num_players = len(players)
		self.dealer = dealer
		self.deck = deck
		self.deck.shuffle()
		self.bets = [[]]*self.num_players
		self.insurance = [0]*self.num_players
		self.blackjack_payout = 1.5
		print("\n\n\n\nA game is initiated!")

	def __repr__(self):
		string = "\nTable Overview \n"
		for each in self.players:
			string += f"  --  {each.name}:  "
			for hand in each.hands:
				string +=  f"{hand.cards}  --  Count: {'Soft' if hand.soft > 0 else ''} {hand.count}\n"
		string += f"  ##  Dealer up card: [{self.dealer.up_card}]"
		return string

	def new_deck(self):
		self.deck = Deck()
		self.deck.shuffle()

	def deal_to_table(self):
		cards_dealt = self.deck.deal_hand(self.num_players*2+2)
		count = 0
		for person in self.players+[self.dealer]:
			person.get_hand(Hand(self.deck,cards_dealt[count], cards_dealt[count+self.num_players+1]))
			count += 1
		return

	def play_hand_with_player(self, player, hand_num):
		print(f"\n\nHello {player.name}! You currently have the following hand:\n\t\t{str(player.hands[hand_num])}")
		check = self.check_blackjack(player, hand_num)
		if check: return
		response = self.ask_split(player, hand_num)
		if response == "yes": return
		response = self.ask_double_down(player, hand_num)
		if response == "yes": return
		while not player.stay[hand_num]:
			self.hit_or_stay(player, hand_num)
		self.check_for_bust(player, hand_num)
		return

	def play_hand_with_dealer(self):
		print(f"\nDEALER's Turn! Dealer has: \n\t\t{[str(each) for each in self.dealer.hands[0].cards]}")
		self.dealer.auto_think(soft17hit=False)
		while self.dealer.stay[0] == False:
			self.dealer.hit(0)
			self.dealer.auto_think(soft17hit=False)
			print(f"{self.dealer.hands[0]}")
		print(f"\nDealer finishes with {self.dealer.hands[0].count}. {' Bust!' if self.dealer.hands[0].bust == True else ''}")

	def play_all_hands_with_player(self,player):
		while all(player.stay) != True:
			curr_hand_num = player.stay.index(False)
			self.play_hand_with_player(player,curr_hand_num)

	def pay_bets_to_players(self):
		print("\n")
		for player in self.players:
			for i, hand in enumerate(player.hands):
				self.pay_bet(player,i)
			player.reset_hands()

	def pay_bet(self, player, hand_num):
		dealer_count = self.dealer.hands[0].count
		dealer_bust = self.dealer.hands[0].bust
		hand = player.hands[hand_num]
		if dealer_bust == True or hand.count > dealer_count:
			player.bank += 2*player.bets[hand_num]
			self.record_results(player, hand_num, 0)
			print(f"Congratz {player.name}! {hand.count} beats {dealer_count}. You win {player.bets[hand_num]}!")
		elif hand.count == dealer_count:
			player.bank += player.bets[hand_num]
			self.record_results(player, hand_num, 2)
			print(f"{player.name}, {hand.count} Is a push. Better than nothing.")
		else:
			self.record_results(player, hand_num, 1)
			print(f"Sorry {player.name}, dealer's {dealer_count} beats {hand.count}. Better luck next time.")
		if player.login == True:	player.profile.bank = player.bank

	def ask_insurance(self):
		if self.dealer.up_card.rank != "A":
			print("No need for insurance")
			return
		for player in self.players:
			response = ""
			if player.computer_player:
				response = player.decide_insurance()
			while response not in ["yes", "no"]:
				response = input(f"{player.name}, would you like to buy insurance? [Yes or No] ---  ")
				response = response.lower()
			if response == "yes":
				player_index = self.players.index(player)
				player.bank -= player.bets[0]/2
				if player.login == True:    player.profile.bank = player.bank
				self.insurance[player_index] = player.bets[0]/2
			else: print(f"{player.name} passes on insurance.")

		bj_bool = self.check_dealer_blackjack()
		return bj_bool

	def ask_double_down(self, player, hand_num):
		if len(player.hands[hand_num].cards) != 2 or player.doubled[hand_num] == True:
			print("Can't double down.")
			return
		response = ""
		if player.computer_player:
			response = player.decide_double_down(hand_num, self.dealer.up_card.value)
		while response not in ["yes", "no"]:
			response = input(f"{player.name}, would you like to double down? [Yes or No] ---  ") # You currently have {'Soft' if player.hands[hand_num].soft > 0 else ''} {player.hands[hand_num].count}
			response = response.lower()
		if response == "yes":
			player.double_down(hand_num)
			player.hands[hand_num].actions['doubled'] = True
			player.hands[hand_num].actions['hit_counts'].append(player.hands[hand_num].count_code())
			player.hit(hand_num)
			if not player.hands[hand_num].bust:
				player.hands[hand_num].actions['stay_count'] = player.hands[hand_num].count_code()
			player.stay[hand_num] = True
			print(f"Final Hand:  {[str(each) for each in player.hands[hand_num].cards]} -- Count: {player.hands[hand_num].count}.")
			self.check_for_bust(player, hand_num)
			return response
		else:
			return

	def ask_split(self, player, hand_num):
		if len(player.hands[hand_num].cards) != 2 or player.hands[hand_num].cards[0].rank != player.hands[hand_num].cards[1].rank:
			print("Can't split.")
			return
		response = ""
		if player.computer_player:
			response = player.decide_split(hand_num, self.dealer.up_card.value)
		while response not in ["yes", "no"]:
			response = input(f"{player.name}, you currently have two {player.hands[hand_num].cards[0].rank}\'s! Would "
								f"you like to split? [Yes or No] ---  ")
			response = response.lower()
		if response == "yes":
			player.split(hand_num)
			return response
		else:
			return

	def take_bets(self):
		for player in self.players:
			response = "N/A"
			if player.computer_player:
				response = player.decide_bet()
			while not response.isdigit():
				response = input(f"{player.name}, what would you like to bet? [Positive integer only]")
			bet = int(response)
			player.bet(bet,0)
			print(f"{player.name} bets {bet} bottlecaps")

	def check_blackjack(self, player, hand_num):
		if player.hands[hand_num].blackjack:
			current_bet = player.bets[hand_num]
			self.record_results(player, hand_num, lost=0, blackjack=True)
			player.clear_hand(hand_num)
			player.bank = current_bet*(1+self.blackjack_payout)
			if player.login == True:    player.profile.bank = player.bank
			print(f"{player.name} has Blackjack! {player.name} keeps his {current_bet} and earns {current_bet*self.blackjack_payout}. Congratz!")
			return True

	def check_for_bust(self,player,hand_num):
		if player.hands[hand_num].bust:
			print("I'm sorry, you've busted \n")
			self.record_results(player, hand_num, 1)
			player.clear_hand(hand_num)

	def check_dealer_blackjack(self):
		if self.dealer.hands[0].count == 21 and len(self.dealer.hands[0].cards) == 2:
			print("Dealer Blackjack. That sucks...")
			for player in self.players:
				if not player.hands[0].blackjack:
					self.record_results(player, 0, lost=1, blackjack=True)
					player.clear_hand()
				else:
					player.bank += player.bets[0]
					if player.login == True:    player.profile.bank = player.bank
					self.record_results(player, 0, lost=2, blackjack=True)
					player.clear_hand()
			self.pay_insurance()
			self.reset_table()
			return True
		return False

	def pay_insurance(self):
		print("Should've bought insurance, I guess.")
		for i, player in enumerate(self.players):
			player.bank += 2*self.insurance[i]
			if player.login == True:    player.profile.bank = player.bank

	def hit_or_stay(self, player, hand_num):
		response = ""
		if player.computer_player:
			response = player.decide_hit_or_stay(hand_num, self.dealer.up_card.value)
		while response not in ["hit", "stay"]:
			response = input(f"{player.name}, you currently have {'a Soft' if player.hands[hand_num].soft > 0 else ''} {player.hands[hand_num].count}. Would you like to 'hit' or 'stay'? ---  ")
			response = response.lower()
		if response == "hit":
			player.hands[hand_num].actions['hit_counts'].append(player.hands[hand_num].count_code())
			player.hit(hand_num)
			print(f"\t\t{player.hands[hand_num]}")
		else:
			player.hands[hand_num].actions['stay_count'] = player.hands[hand_num].count_code()
			player.tell_stay(hand_num)

	def record_results(self, player, hand_num, lost, blackjack=False):
		# 0 = win, 1 = lost, 2 = push
		if player.login:
			player.hands[hand_num].results[lost + 1] = 1
			up_card = self.dealer.up_card.value
			at_count = player.hands[hand_num].actions['first_count']
			for index in range(4):
				player.profile.player_df.loc[up_card].loc[at_count][index] += player.hands[hand_num].results[
					index]
			if not blackjack:
				for at_count in player.hands[hand_num].actions['hit_counts']:
					for index in range(4):
						player.profile.player_df.loc[up_card].loc[at_count][index+4] += player.hands[hand_num].results[index]
				at_count = player.hands[hand_num].actions['stay_count']
				if at_count != 0:
					for index in range(4):
						player.profile.player_df.loc[up_card].loc[at_count][index+8] += player.hands[hand_num].results[index]
				if player.hands[hand_num].actions['doubled']:
					at_count = player.hands[hand_num].actions['hit_counts'][-1]
					for index in range(4):
						player.profile.player_df.loc[up_card].loc[at_count][index + 12] += player.hands[hand_num].results[
							index]

	def play(self):
		self.take_bets()
		self.deal_to_table()
		print(self)
		if self.dealer.up_card.rank == "A":
			result = self.ask_insurance()
			if result: return
		for each_player in self.players:
			self.play_all_hands_with_player(each_player)
		self.play_hand_with_dealer()
		self.pay_bets_to_players()
		self.reset_table()

	def save_profiles(self):
		for player in self.players:
			if player.login: player.profile.save()

	def reset_table(self):
		for person in self.players+[self.dealer]:
			person.reset_hands()

