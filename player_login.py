import numpy as np
import pandas as pd
import pickle


class PlayerLogin():
    def __init__(self, name, new=False):
        self.name = name
        if not new:
            try:
                self.load()
            except FileNotFoundError:
                print(f"'{self.name}_loginsave.pickle' not found. FileNotFoundError.")
                new = True
            else:
                self.load()
        if new:
            self.new_player("yes")

    def __repr__(self):
        string = str(f"{self.name}'s Stats: \n"
                     f"Bank: {self.bank} bottlecap$\n"
                     f"{str(self.player_df.sum())}")
        return string

    def new_player(self,ans = "no"):
        if ans != "yes":
            ans = input("\nAre you sure you want to reset this player's profile?   ")
            if ans.lower() == "no":
                print("\nNo Change.")
                return
        else:
            self.build_database()
            ans = self.input_number("\nWhat is the starting cash?")
            self.bank = ans

    def save(self):
        with open(f"{self.name}_loginsave.pickle","wb") as filew:
            pickle.dump([self.player_df, self.bank], filew)

    def load(self):
        with open(f"{self.name}_loginsave.pickle","rb") as filer:
            self.player_df, self.bank = pickle.load(filer)

    def display_stats_graphically(self):
        pass

    def build_database(self):
        up_cards = list(range(1,11))
        count = list(range(2, 22)) + list(range(102, 122))
        up_cards_array = np.array([dealer for dealer in up_cards for player in count])
        count_array = np.array([player for dealer in up_cards for player in count])
        results_array = np.array(['first_total', 'first_won', 'first_lost', 'first_push',
                                  'hit_total', 'hit_won', 'hit_lost', 'hit_push',
                                  'stay_total', 'stay_won', 'stay_lost', 'stay_push',
                                  'double_total', 'double_won', 'double_lost', 'double_push'])
        self.player_df = pd.DataFrame(np.zeros((len(up_cards_array), len(results_array))),
                               [up_cards_array,count_array],
                               results_array)

    def input_number(self,message):
        while True:
            try:
                user_input = int(input(message))
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                return user_input

    def record_results(self, results):
        ''' Results should be list ['games_total', 'games_won', 'games_lost', 'games_push', 'double_total', 'double_won',
                            'double_lost', 'double_push']
                            '''


