from typing import List, Tuple
import pytest
import numpy as np
from qiskit import Aer, execute
from qiskit.extensions import XGate, HGate, IdGate

from backend.logic import PayoffTable, QuantumGame
from backend.utils import Protocol

# User prisoner's dilemma payoff
sample_payoff_table = {'00': (-1, -1),
                       '01': (-3, 0),
                       '10': (0, -3),
                       '11': (-2, -2)}


def test_PayoffTable():
    payoff_table = PayoffTable(n_players=2, n_choices=2, payoff=sample_payoff_table)
    assert payoff_table.get_payoff_table() == sample_payoff_table
    for key, value in sample_payoff_table.items():
        assert payoff_table.get_payoffs(key) == value
        payoff_table.set_payoffs(key, (int(key,2), int(key,2)))
        assert payoff_table.get_payoffs(key) == (int(key,2), int(key,2))


def make_QuantumGame_test_cases() -> List[Tuple]:
    gates = [[[IdGate()], [XGate()]],
             [[XGate()], [IdGate()]],
             [[HGate()], [HGate()]]]
    amplitudes = {"EWL": [[0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [0.5, 0.5, 0.5, 0.5]]}
    cases = []
    for protocol in amplitudes.keys():
        for i in range(len(gates)):
            cases.append((gates[i], protocol, amplitudes[protocol][i]))
    return cases


@pytest.mark.parametrize("player_gates, protocol, amplitudes", make_QuantumGame_test_cases())
def test_QuantumGame(player_gates: List, protocol: str, amplitudes: List):
    # EWL Protocol
    quantum_game = QuantumGame(player_gates, Protocol[protocol])
    quantum_game.circ.remove_final_measurements()
    backend = Aer.get_backend('statevector_simulator')
    job_sim = execute(quantum_game.circ, backend)
    result = job_sim.result()
    outputstate = result.get_statevector(quantum_game.circ, decimals=3)
    for i in range(len(outputstate)):
        assert np.isclose(np.abs(outputstate[i]), np.abs(amplitudes[i]))