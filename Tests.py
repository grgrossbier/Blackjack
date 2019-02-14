import unittest
import Blackjack as bj
from importlib import reload
import player_login as pl
reload(bj)
import sys, os


# Disable
def block_print():
	sys.stdout = open(os.devnull, 'w')


# Restore
def enable_print():
	sys.stdout = sys.__stdout__


## Set up some basic variables to toy around with.
d = bj.Deck()
d.shuffle()
h = bj.Hand(d,d.deal_card(), d.deal_card())
# print(f"Hand starts with... {str(h)}")
# while h.bust == False:
# 	h.add_card(d)
# 	print(f"Players hits and gets [{h.cards[-1]}] and now has {h.count}")
# print(f"Player busts...\n{str(h)}")


# ## Setting up a player
# p = bj.Player("Danielle")
# p.get_hand(h)

# while p.hands[0].cards[0].rank != p.hands[0].cards[1].rank:
# 	d = bj.Deck()
# 	d.shuffle()
# 	p = bj.Player("Danielle")
# 	p.reset_hands()
# 	p.bet(30)
# 	h = bj.Hand(d,d.deal_card(), d.deal_card())
# 	p.get_hand(h)

# print(p)
# print(p.hands)
# p.split()
# p.double_down(1)
# print(p)
# print(p.hands)

Machine = pl.PlayerLogin("FromScratchLearner")
Machine.bank = 0
#print(Machine)
a = bj.Machine_Learner(profile=Machine, login=True, strategy=[0, 2, 2, 2])
Grant = pl.PlayerLogin("Grant")
grant = bj.Player(Grant, True)
bad_mem = bj.Machine_Learner()
g= bj.Game([grant, a])
# block_print()
for j in range(1):
	for i in range(1):
		g.play()
		print(f"THIS IS HAND {j*5+i+1}")
	g.new_deck()
# enable_print()
g.save_profiles()
#rint(Machine)
Machine.player_df.to_csv('machine.csv')







# class ActiveTest(unittest.TestClass):

# if __name__ == "__main__":
# 	unittest.main()

# TO CALL
# exec(open("C:\Users\Cocytus\Dropbox\Code\Blackjack\Tests.py").read())