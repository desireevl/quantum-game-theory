from backend.utils import Protocol


def test_Protocol():
    protocol_names = ['EWL', 'MW', 'Classical']
    for name in protocol_names:
        protocol = Protocol[name]
        if name == 'Classical':
            assert protocol.describe() == ('Classical', 'Classical protocol')
        else:
            assert protocol.describe() == (name, name + ' quantization protocol')