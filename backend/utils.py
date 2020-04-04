from enum import Enum

import numpy as np

from qiskit.extensions import XGate, YGate, SGate, ZGate, HGate, TGate, RZGate, RYGate, IdGate
from qiskit.circuit import Gate
from qiskit.circuit import QuantumRegister


def gen_predefined_payoffs(game_name: str, num_players: int, payoff_input: dict):
    """Generates payoff table based on game name"""
    num_players = num_players
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
        payoff_table = {'00': (-1, -1),
                        '01': (-3, 0),
                        '10': (0, -3),
                        '11': (-2, -2)}
    elif game_name == 'BoS':
        payoff_table = {'00': (3, 2),
                        '01': (0, 0),
                        '10': (0, 0),
                        '11': (2, 3)}
    elif game_name == 'custom':
        payoff_table = {key: tuple(map(int, value.split(','))) for key, value in payoff_input.items()}
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

def parse_angle(angle_str: str) -> float:
    numbers=['']
    for i in range(len(angle_str)):
        if angle_str[i].isdigit() or angle_str[i]=='.' or (angle_str[i]=='-' and i==0):
            numbers[-1] = numbers[-1]+angle_str[i]
        elif angle_str[i]=='*' and angle_str[i-1].isdigit() and angle_str[i+1].isdigit():
            numbers.append('')
        elif angle_str[i] =='p':
            if i==0:
                pass
            elif angle_str[i-1].isdigit():
                pass
            else:
                raise ValueError(f'input {angle_str} is invalid (can only contain digits, ".", "*" and "pi", '
                                 f'and cannot start or end with "*")')
        elif angle_str[i] =='i' and angle_str[i-1] =='p':
            numbers.append(np.pi)
            if i != len(angle_str):
                numbers.append('')
        else:
            raise ValueError(f'{angle_str} is invalid (can only contain digits, ".", "*" and "pi"')
    angle = 1
    for number in numbers:
        angle *= float(number)
    return angle


def generate_unitary_gate(gate_name: str) -> Gate:
    # Rx, Ry and Rz gates
    if gate_name[0]=='R' and gate_name[2]=='(':
        angle = parse_angle(gate_name[2:-1])
        if gate_name[1]=='x':
        elif gate_name[1] == 'y'
        elif gate_name[1] == 'z'
    else:
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
        return unitary_gates[gate_name]


class Protocol(Enum):
    """
    The various different quantum/classical game theory game protocols
    """
    EWL = "EWL quantization protocol"
    MW = "MW quantization protocol"
    Classical = "Classical protocol"

    def describe(self):
        # Self is the member here
        return self.name, self.value
