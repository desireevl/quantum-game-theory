from qiskit import *
from qiskit.extensions import *
import numpy as np

class QuantumGameCircuit:
    
    def __init__(self, player_gates):
        self.player_gates = player_gates
        self.num_players = len(player_gates)
        self.circ = self._make_circuit(player_gates)
        
    def _make_circuit(self, player_gates):
        circ = QuantumCircuit(self.num_players,self.num_players)
        circ = self._entangle_qubits(circ)
        circ.barrier()
        for i in range(self.num_players):
            circ = self._add_player_gates(circ, i, player_gates[i])
        circ.barrier()
        circ = self._unentangle_qubits(circ)
        circ.barrier()
        circ.measure(range(self.num_players),range(self.num_players))
        return circ

    def _entangle_qubits(self, circ):
        circ.h(0)
        for i in range(self.num_players-1):
            circ.cx(0,i+1)
        circ.rz(np.pi/2, 0)
        return circ

    def _add_player_gates(self, circ, player_num, gates):
        for i in range(len(gates)):
            circ.append(gates[i],[player_num])
        return circ

    def _unentangle_qubits(self, circ):
        circ.rz(-np.pi/2, 0)
        for i in range(self.num_players-1,0,-1):
            circ.cx(0,i)
        circ.h(0)      
        return circ
    
    def draw_circuit(self):
        self.circ.draw(output='mpl')