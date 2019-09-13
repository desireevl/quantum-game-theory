from qiskit import QuantumCircuit, Aer, execute
from qiskit.extensions import *
import numpy as np

class QuantumGameCircuit:
    
    def __init__(self, player_gates):
        self.player_gates = player_gates
        self.num_players = len(player_gates)
        self.circuit = self._make_circuit(player_gates)
        
    def _make_circuit(self, player_gates):
        circuit = QuantumCircuit(self.num_players,self.num_players)
        circuit = self._entangle_qubits(circuit)
        circuit.barrier()
        for i in range(self.num_players):
            circuit = self._add_player_gates(circuit, i, player_gates[i])
        circuit.barrier()
        circuit = self._unentangle_qubits(circuit)
        circuit.barrier()
        circuit.measure(range(self.num_players),range(self.num_players))
        return circuit

    def _entangle_qubits(self, circuit):
        circuit.h(0)
        for i in range(self.num_players-1):
            circuit.cx(0,i+1)
        circuit.rz(np.pi/2, 0)
        return circuit

    def _add_player_gates(self, circuit, player_num, gates):
        for i in range(len(gates)):
            circuit.append(gates[i],[player_num])
        return circuit

    def _unentangle_qubits(self, circuit):
        circuit.rz(-np.pi/2, 0)
        for i in range(self.num_players-1,0,-1):
            circuit.cx(0,i)
        circuit.h(0)      
        return circuit
    
    def draw_circuit(self):
        self.circuit.draw(output='mpl')