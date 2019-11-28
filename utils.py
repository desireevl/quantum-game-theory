from qiskit.extensions import XGate, YGate, SGate, ZGate, HGate, TGate, RZGate, RYGate
from enum import Enum
import numpy as np
import math

predefined_games = {"chicken": [( 0 ,   0), 
                                ( -1,   1), 
                                (  1,  -1), 
                                (-10, -10)],
                    "prisoner": [(-1, -1), 
                                 (-3,  0), 
                                 (0 , -3), 
                                 (-2, -2)],
                    "4-minority": [(0, 0, 0, 0), 
                                   (0, 0, 0, 1),
                                   (0, 0, 1, 0),
                                   (0, 0, 0, 0),
                                   (0, 1, 0, 0),
                                   (0, 0, 0, 0),
                                   (0, 0, 0, 0),
                                   (1, 0, 0, 0),
                                   (1, 0, 0, 0),
                                   (0, 0, 0, 0),
                                   (0, 0, 0, 0),
                                   (0, 1, 0, 0),
                                   (0, 0, 0, 0),
                                   (0, 0, 1, 0),
                                   (0, 0, 0, 1),
                                   (0, 0, 0, 0)]}

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
