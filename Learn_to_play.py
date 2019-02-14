import Blackjack as bj
from importlib import reload
reload(bj)

def count_code(cards):
    count = sum([each.value for each in cards])
    soft = sum([1 if each.value == 1 else 0 for each in cards])
    while count > 21 and soft > 0:
        count =