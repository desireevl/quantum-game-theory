from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit.quantum_info import Operator
from qiskit.extensions import XGate, HGate
from QuantumGameTheory import Game
import pandas as pd
import numpy as np
import base64
from io import BytesIO


circ = QuantumCircuit(2,2)
circ.x(0)
circ.s(1)

# image = temp.draw(output='mpl1')
# print(image)

# buffered = BytesIO() 
# image.save(buffered, format="JPEG")

image = circ.draw(output='latex')

buffered = BytesIO()
image.save(buffered, format="JPEG")

print(base64.b64encode(buffered.getvalue()))
