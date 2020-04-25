import pytest
import numpy as np
from qiskit.extensions import XGate, YGate, SGate, ZGate, HGate, TGate, RXGate, RYGate, RZGate, IdGate

from backend.utils import parse_angle, generate_unitary_gate


def test_parse_angle():
    assert parse_angle(' 2 ') == 2
    assert parse_angle('-1') == -1
    assert parse_angle('3.7') == 3.7
    assert parse_angle('.364 ') == .364
    assert parse_angle(' pi') == np.pi
    assert parse_angle('6.23*.98') == 6.23 * .98
    assert parse_angle('6.23/ .98') == 6.23 / .98
    assert parse_angle('-.14*1.84 /pi*2/ 3') == -.14*1.84/np.pi*2/3
    with pytest.raises(ValueError):
        parse_angle('1..1')
    with pytest.raises(ValueError):
        parse_angle('p1i')
    with pytest.raises(ValueError):
        parse_angle('*2')
    with pytest.raises(ValueError):
        parse_angle('2*/1')
    with pytest.raises(ValueError):
        parse_angle('3-4')
    with pytest.raises(ValueError):
        parse_angle('p*i')


def test_generate_unitary_gate():
    assert generate_unitary_gate("X") == XGate()
    assert generate_unitary_gate("Y") == YGate()
    assert generate_unitary_gate("S") == SGate()
    assert generate_unitary_gate("Z") == ZGate()
    assert generate_unitary_gate("H") == HGate()
    assert generate_unitary_gate("T") == TGate()
    assert generate_unitary_gate("I") == IdGate()
    for i in np.arange(-10, -1, 0.1):
        for j in np.arange(1, 10, 0.1):
            # Rx Gates
            assert generate_unitary_gate(f'Rx(pi*{j})') == RXGate(np.pi * j)
            assert generate_unitary_gate(f'Rx({i}/ {j}*pi)') == RXGate(i / j * np.pi)
            assert generate_unitary_gate(f'Rx( {i}*{j}/pi )') == RXGate(i * j / np.pi)
            assert generate_unitary_gate(f'Rx( {i} / {j}/pi)') == RXGate(i / j / np.pi)
            # Ry Gates
            assert generate_unitary_gate(f'Ry(pi*{j})') == RYGate(np.pi * j)
            assert generate_unitary_gate(f'Ry({i}/ {j}*pi)') == RYGate(i / j * np.pi)
            assert generate_unitary_gate(f'Ry( {i}*{j}/pi )') == RYGate(i * j / np.pi)
            assert generate_unitary_gate(f'Ry( {i} / {j}/pi)') == RYGate(i / j / np.pi)
            # Rz Gates
            assert generate_unitary_gate(f'Rz(pi*{j})') == RZGate(np.pi * j)
            assert generate_unitary_gate(f'Rz({i}/ {j}*pi)') == RZGate(i / j * np.pi)
            assert generate_unitary_gate(f'Rz( {i}*{j}/pi )') == RZGate(i * j / np.pi)
            assert generate_unitary_gate(f'Rz( {i} / {j}/pi)') == RZGate(i / j / np.pi)