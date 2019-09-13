import numpy as np


class Game:
    def __init__(self, type, payoff=None):
        # predefined games
        if type=="chicken":
            self.n_players = 2
            self.n_choices = 2
            self.payoff = PayoffTable(self.n_players, self.n_choices, [[(0,0), (1,-1)], [(-1,1), (-10,-10)]])
        elif type=="prisoner":
            self.n_players = 2
            self.n_choices = 2
            self.payoff = PayoffTable(self.n_players, self.n_choices, [[(-1, -1), (0, -3)], [(-3, 0), (-2, -2)]])
        elif type=="minority":
            self.n_players = 4
            self.n_choices = 2
            minority_table = [[[[(0,0,0,0), (1,0,0,0)], [(0,1,0,0), (0,0,0,0)]],
                               [[(0,0,1,0), (0,0,0,0)], [(0,0,0,0), (0,0,0,1)]]],
                              [[[(0,0,0,1), (0,0,0,0)], [(0,0,0,0), (0,0,1,0)]],
                               [[(0,0,0,0), (0,1,0,0)], [(1,0,0,0), (0,0,0,0)]]]]
            self.payoff = PayoffTable(self.n_players, self.n_choices, minority_table)
        else:
            if payoff==None:
                raise ("The specified game type is not currently known, please implement the game object manually")
            else:
                shape = np.shape(payoff)
                self.n_players = shape[-1]
                self.n_choices = shape[0]
                self.payoff = PayoffTable(self.n_players, self.n_choices, payoff)



class PayoffTable:
    # object that stores the data of a game theory game

    def __init__(self, n_players=2, n_choices=2, payoff=None):
        self.n_players = n_players
        self.n_choices = n_choices
        self.n_big = n_choices**n_players

        if payoff == None:
            self.payoff = np.zeros((self.n_big, n_players))
        else:
            self.payoff = np.reshape(payoff, (self.n_big, n_players))

    def set_payoff(self, tuple, payoff):
        # sets the payoff value for a given tuple of player choices
        self.payoff[self._get_index(tuple),:] = payoff

    def get_payoff(self, choices):
        # access the payoff tuple for a given tuple of choices
        return self.payoff[self._get_index(choices)]

    def _get_index(self, tuple):
        # gets the index from a given tuple of player choices
        sum = 0
        for i in range(len(tuple)):
            sum += tuple[i] * self.n_choices**i
        return sum

my_game = Game("prisoner")

