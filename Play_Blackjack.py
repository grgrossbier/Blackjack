import Blackjack as bj
from importlib import reload
from player_login import *

reload(bj)

print("Hello, please login to your player profile.")
name = input("\nWhat is your name?   :   ")
player1 = PlayerLogin(name)
print(f"\nHi {name}, lets play.")

auto = True

d = bj.Deck()
d.shuffle()
a = bj.Player(name)
g = bj.Game([a])
while True:
    g.take_bets()
    g.deal_to_table()
    print(g)
    if g.dealer.up_card.rank == "A": g.ask_insurance()
    for each_player in g.players:
        g.play_all_hands_with_player(each_player)
    g.play_hand_with_dealer()
    g.pay_bets_to_players()
    g.reset_table()
