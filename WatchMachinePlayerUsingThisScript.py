import Blackjack as bj
from importlib import reload
import player_login as pl
import sys
import os
reload(bj)


def input_number(message):
	while True:
		try:
			user_input = int(input(message))
		except ValueError:
			print("Not an integer! Try again.")
			continue
		else:
			return user_input

# Disable
def block_print():
	sys.stdout = open(os.devnull, 'w')

# Restore
def enable_print():
	sys.stdout = sys.__stdout__


message = "\n How many hands would you like to watch FromScratchLearner play?  --  "
num = input_number(message)

Machine = pl.PlayerLogin("FromScratchLearner")
Machine.bank = 0
a = bj.Machine_Learner(profile=Machine, login=True, strategy=[0, 2, 2, 2])
g = bj.Game([a])
print(f"\nStarting cash in hand = {Machine.bank}")

for j in range(num):
	print(f"\n\n\nTHIS IS HAND {j + 1}")
	g.new_deck()
	g.play()
g.save_profiles()

print(f"\nFinal cash in hand = {Machine.bank}")


