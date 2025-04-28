from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
import random

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Prepare Alice's random choices
send_had = random.randint(0, 1)  # Whether to apply Hadamard
send_val = random.randint(0, 1)  # Bit value (0 or 1)

# Alice prepares the qubit
qc.reset(0)
if send_val:
    qc.x(0)  # NOT gate to flip to 1
if send_had:
    qc.h(0)

# Measure the qubit
qc.measure(0, 0)

# Now simulate the transmission with possible spy interference
sampler = Sampler()
job = sampler.run(qc)
result = job.result()

# Get the probability distribution
probabilities = result.quasi_dists[0]

# Spy intercepts (collapse happens here)
stolen_bit = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]

# Bob prepares his random basis
recv_had = random.randint(0, 1)

# Bob reconstructs the qubit after fiber transmission
qc2 = QuantumCircuit(1, 1)
if stolen_bit == '1':
    qc2.x(0)
if recv_had:
    qc2.h(0)
qc2.measure(0, 0)

# Bob reads the result
job2 = sampler.run(qc2)
result2 = job2.result()
final_result = list(result2.quasi_dists[0].keys())[0]

# Check for spy
if send_had == recv_had:
    if str(send_val) != final_result:
        print('Caught a spy!')
    else:
        print('No spy detected.')
else:
    print('Bases do not match; discard the result.')
