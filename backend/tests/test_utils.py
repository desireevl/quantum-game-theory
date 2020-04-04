import pytest
import numpy as np

from backend.utils import Protocol, parse_angle


def test_Protocol():
    protocol_names = ['EWL', 'MW', 'Classical']
    for name in protocol_names:
        protocol = Protocol[name]
        if name == 'Classical':
            assert protocol.describe() == ('Classical', 'Classical protocol')
        else:
            assert protocol.describe() == (name, name + ' quantization protocol')

def test_parse_angle():
    assert parse_angle('2') == 2
    assert parse_angle('-1') == -1
    assert parse_angle('3.7') == 3.7
    assert parse_angle('.364') == .364
    assert parse_angle('pi') == np.pi
    assert parse_angle('6.23*.98') == 6.23 * .98
    assert parse_angle('6.23/.98') == 6.23 / .98
    assert parse_angle('-.14*1.84/pi*2/3') == -.14*1.84/np.pi*2/3
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
