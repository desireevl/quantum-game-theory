from qiskit import *
from qiskit.extensions import *
import numpy as np
from qiskit.quantum_info import Operator


class QuantumGameCircuit:

    def __init__(self, player_gates):
        self.player_gates = player_gates
        self.num_players = len(player_gates)
        self.J, self.Jdg = self._make_J_operators()
        self.circ = self._make_circuit(player_gates)

    def _make_J_operators(self):
        I = np.identity(2**self.num_players)
        x = [[0, 1],
             [1, 0]]
        tensorX = x
        for i in range(self.num_players-1):
            tensorX = np.kron(tensorX, x)
        J = 1/np.sqrt(2)*(I+1j*tensorX)
        Jdg = 1/np.sqrt(2)*(I-1j*tensorX)
        J = Operator(J)
        Jdg = Operator(Jdg)
        return J, Jdg

    def _make_circuit(self, player_gates):
        circ = QuantumCircuit(self.num_players, self.num_players)
        circ.append(self.J, range(self.num_players))
        circ.barrier()
        for i in range(self.num_players):
            circ = self._add_player_gates(circ, i, player_gates[i])
        circ.barrier()
        circ.append(self.Jdg, range(self.num_players))
        circ.barrier()
        circ.measure(range(self.num_players), range(self.num_players))
        return circ

    def _add_player_gates(self, circ, player_num, gates):
        for i in range(len(gates)):
            circ.append(gates[i], [player_num])
        return circ

    def draw_circuit(self):
        self.circ.draw(output='mpl')
