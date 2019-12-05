from qiskit.extensions import XGate, YGate, SGate, ZGate, HGate, TGate, RZGate, RYGate
from enum import Enum
import numpy as np
import math

predefined_games = {"chicken": {'00': ( 0 ,   0), 
                                '01': ( -1,   1), 
                                '10': (  1,  -1), 
                                '11': (-10, -10)},
                    "prisoner": {'00': (-1, -1), 
                                 '01': (-3,  0), 
                                 '10': (0 , -3), 
                                 '11': (-2, -2)},
                    "BoS": {'00': (3, 2), 
                            '01': (0, 0), 
                            '10': (0, 0), 
                            '11': (2, 3)},
                    "4-minority": {'0000': (0, 0, 0, 0), 
                                   '0001': (0, 0, 0, 1),
                                   '0010': (0, 0, 1, 0),
                                   '0011': (0, 0, 0, 0),
                                   '0100': (0, 1, 0, 0),
                                   '0101': (0, 0, 0, 0),
                                   '0110': (0, 0, 0, 0),
                                   '0111': (1, 0, 0, 0),
                                   '1000': (1, 0, 0, 0),
                                   '1001': (0, 0, 0, 0),
                                   '1010': (0, 0, 0, 0),
                                   '1011': (0, 1, 0, 0),
                                   '1100': (0, 0, 0, 0),
                                   '1101': (0, 0, 1, 0),
                                   '1110': (0, 0, 0, 1),
                                   '1111': (0, 0, 0, 0)}}

unitary_gates = {"X": XGate(), 
                 "Y": YGate(), 
                 "S": SGate(), 
                 "Z": ZGate(), 
                 "H": HGate(), 
                 "T": TGate(), 
                 #"W": self._gen_w_gate(),
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
