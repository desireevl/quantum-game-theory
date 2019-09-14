from QuantumGameTheory import Game, QuantumGameCircuit
from qiskit import Aer, execute
from qiskit.quantum_info import Operator
from qiskit.extensions import XGate, YGate, SGate, ZGate, HGate, TGate, RZGate, RYGate
import numpy as np

class Backend():
    def __init__(self, type):
        self.lookup_table = self._gen_lookup_table()
        self.game = Game(type)
        self.backend = Aer.get_backend("qasm_simulator")
        self.img_path = "assets/circuit.png"

    def _gen_lookup_table(self):

        op1 = RZGate(-3 * np.pi / 8)
        op2 = RYGate(np.pi / 2)
        op3 = RZGate(np.pi / 2)
        result = {"X": XGate(), "Y": YGate(), "S": SGate(), "Z": ZGate, "H": HGate(), "T": TGate(), "W": self._gen_w_gate(),
                  "Rz1": RZGate(-3 * np.pi / 8), "Rz2": RZGate(np.pi/2), "Ry1": RYGate(np.pi/2)}
        return result

    def _gen_w_gate(self):
        I = np.matrix('1 0; 0 1')
        X = np.matrix('0 1; 1 0')
        Y = np.matrix('0 -1j; 1j 0')
        Z = np.matrix('1 0; 0 -1')

        a = (1 / np.sqrt(2)) * np.cos(np.pi / 16) * (I + 1j * X) - (1j / np.sqrt(2)) * np.sin(np.pi / 16) * (Y + Z)
        return Operator(a)

    def _simulation(self, qgc):
        job_sim = execute(qgc.circ, self.backend, shots=1)
        res_sim = job_sim.result()
        counts = res_sim.get_counts(qgc.circ)
        return [int(s) for s in list(counts.keys())[0]]

    def play(self, player_gates):

        player_gate_objects = []
        for i in range(len(player_gates)):
            player_gate_objects.append([])
            for j in player_gates[i]:
                player_gate_objects[i].append(self.lookup_table[j])

        qgc = QuantumGameCircuit(player_gate_objects)
        qgc.draw_circuit(self.img_path)
        choices = self._simulation(qgc)
        game_result = self.game.get_result(choices)

        return game_result, self.img_path
