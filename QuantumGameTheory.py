import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from protocols import Protocol
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

    def get_result(self, choices):
        return self.payoff.get_payoff(choices)


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


class QuantumGameCircuit:
    def __init__(self, player_gates, protocol: Protocol = Protocol.EWL):
        self.protocol = protocol
        self.player_gates = player_gates
        self.num_players = len(player_gates)
        self.J, self.Jdg = self._make_J_operators()
        self.circ = self._make_circuit(player_gates)

    def _make_J_operators(self):
        I = np.identity(1 << self.num_players)
        X = np.matrix([[0, 1], [1, 0]])
        tensorX = X

        for i in range(self.num_players - 1):
            tensorX = np.kron(tensorX, X)

        J = Operator(1 / np.sqrt(2) * (I + 1j * tensorX))
        Jdg = Operator(1 / np.sqrt(2) * (I - 1j * tensorX))

        return J, Jdg

    def _make_circuit(self, player_gates):
        circ = QuantumCircuit(self.num_players, self.num_players)
        circ.append(self.J, range(self.num_players))
        circ.barrier()
        for i in range(self.num_players):
            circ = self._add_player_gates(circ, i, player_gates[i])
        circ.barrier()
        if self.protocol == Protocol.EWL:
            circ.append(self.Jdg,range(self.num_players))
            circ.barrier()
        circ.measure(range(self.num_players), range(self.num_players))
        print(circ)
        return circ

    def _add_player_gates(self, circ, player_num, gates):
        for i in range(len(gates)):
            circ.append(gates[i], [player_num])
        return circ

    def draw_circuit(self, filepath):
        self.circ.draw(filename=filepath, output='mpl')
