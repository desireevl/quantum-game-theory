import numpy as np

from enum import Enum

from qiskit.extensions import XGate, YGate, SGate, ZGate, HGate, TGate, RZGate, RYGate, IdGate
from qiskit.circuit import Gate
from qiskit.circuit import QuantumRegister


def gen_predefined_payoffs(game_name: str, num_players: int):
    '''Generates payoff table based on game name'''
    num_players = 4
    payoff_table = {}
    if game_name == "minority":
        for i in range(2**num_players):
            outcome = format(i, '0'+str(num_players)+'b')
            payoff = np.zeros(num_players)
            if outcome.count('0') != 1 and outcome.count('1') != 1:
                payoff_table[outcome] = tuple(payoff)
            else:
                if outcome.count('0') == 1:
                    win_ind = outcome.find('0')
                    payoff[win_ind] = 1
                    payoff_table[outcome] = tuple(payoff)
                if outcome.count('1') == 1:
                    win_ind = outcome.find('1')
                    payoff[win_ind] = 1
                    payoff_table[outcome] = tuple(payoff)
    elif game_name == "chicken":
        for i in range(2**num_players):
            outcome = format(i, '0'+str(num_players)+'b')
            if outcome.count('1') == 0:
                payoff_table[outcome] = tuple(np.zeros(num_players))
            elif outcome.count('1') == 1:
                payoff = np.array([])
                for j in range(num_players):
                    if outcome[j] == '0':
                        payoff = np.append(payoff, -1)
                    else:
                        payoff = np.append(payoff, 1)
                payoff_table[outcome] = tuple(payoff)
            else:
                payoff = np.array([])
                for j in range(num_players):
                    if outcome[j] == '0':
                        payoff = np.append(payoff, 0)
                    else:
                        payoff = np.append(payoff, -10)
                payoff_table[outcome] = tuple(payoff)
    elif game_name == 'prisoner':
        return {'00': (-1, -1),
                '01': (-3, 0),
                '10': (0, -3),
                '11': (-2, -2)}
    elif game_name == 'BoS':
        return {'00': (3, 2),
                '01': (0, 0),
                '10': (0, 0),
                '11': (2, 3)}
    return payoff_table


class WGate(Gate):
    """ Creates the custom W gate """

    def __init__(self):
        """Create new W gate."""
        super().__init__("W", 1, [])

    def _define(self):
        """
        gate W a {
        Rz(-3*pi/8) a; Rz(pi/2) a; Ry(pi/2)
        }
        """
        definition = []
        q = QuantumRegister(1, "q")
        rule = [
            (RZGate(-3 * np.pi / 8), [q[0]], []),
            (RZGate(np.pi / 2), [q[0]], []),
            (RYGate(np.pi / 2), [q[0]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition


unitary_gates = {"X": XGate(),
                 "Y": YGate(),
                 "S": SGate(),
                 "Z": ZGate(),
                 "H": HGate(),
                 "T": TGate(),
                 "I": IdGate(),
                 "W": WGate(),
                 "Rz1": RZGate(-3 * np.pi / 8),
                 "Rz2": RZGate(np.pi/2),
                 "Ry1": RYGate(np.pi/2)}


class Protocol(Enum):
    """
    The various different quantum/classical game theory game protocols
    """
    EWL = "EWL quantization protocol"
    MW = "MW quantization protocol"
    Classical = "Classical protocol"

    def describe(self):
        # self is the member here
        return self.name, self.value
