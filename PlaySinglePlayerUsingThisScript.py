import Blackjack as bj
from importlib import reload
import player_login as pl
reload(bj)


print("\nWelcome to the Blackjack table at Hotel Git.")
loginname = input("\nWhat is your login name?  --  ")
profile = pl.PlayerLogin(loginname)
player = bj.Player(profile, True)
g = bj.Game([player])
print(f"\nStarting cash in hand = {profile.bank}")

ans = "yes"
while ans.lower() == "yes":
	g.new_deck()
	g.play()
	g.save_profiles()
	print(f"\nCash in hand = {profile.bank}")
	ans = input("\nGood Game.  Play again? ['yes' or 'no']  --  ")
	while ans.lower() not in ["yes", "no"]:
		ans = input("\nGood Game.  Play again? ['yes' or 'no']  --  ")

print("\n\nThanks for playing!\n\n")