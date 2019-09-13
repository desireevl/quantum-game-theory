import numpy as np
from qiskit import QuantumCircuit, Aer, execute
# from qiskit import *

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0,1)
circ.rz(np.pi/2, 1)

backend = Aer.get_backend('statevector_simulator')
job = execute(circ, backend)
result = job.result()
outputstate = result.get_statevector(circ, decimals=3)
print(outputstate)