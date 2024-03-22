# implementation of teleportation algorithm with xanadu

import strawberryfields as sf
from strawberryfields.ops import *
import numpy as np
import matplotlib.pyplot as plt

# set random seed for reproducibility
np.random.seed(47)

# initialize program on 3 registers
prog = sf.Program(3)

# teleport the coherent state state |alpha> = for alpha = 1 + 0.5j
alpha = 1 + 0.5j
r = abs(alpha)
phi = np.angle(alpha)

# prepare state with prog.context manager:
with prog.context as q:
    # prepare the initial state
    Coherent(r, phi) | q[0]

    # create an entangled pair
    Squeezed(-2) | q[1]
    Squeezed(2) | q[2]

    # apply the first part of the teleportation protocol
    BS = BSgate(np.pi/4, np.pi) 
    BS | (q[1], q[2])
    BS | (q[0], q[1])

    # homodyne measurement
    MeasureX | q[0]
    MeasureP | q[1]

    # feedforward the results
    Xgate(np.sqrt(2) * q[0].par) | q[2]
    Zgate(-np.sqrt(2) * q[1].par) | q[2]


# run the engine
# eng = sf.Engine('fock', backend_options={"cutoff_dim": 15}) 
    
# run the circuit
# extract the state from the results object
# state = results.state

# # calculate reduced density matrix for mode 2
# state_rdm = state.reduced_dm([2])

# # plot marginal fock probability
# plt.bar(range(15), state_rdm.diagonal())
# plt.xlabel('Fock state')
# plt.ylabel('Marginal probability')
# plt.title('Fock state probabilities of the teleported state')
# plt.savefig('teleportation.png')
# # plt.show()

# # alternatibely, we can also calculate the fock probabilities directly
# fock_probs = state.all_fock_probs()
# fock_probs.shape
# print(np.sum(fock_probs, axis=(0,1)))

eng = sf.RemoteEngine("simulon_gaussian")
# results = eng.run(prog, shots=1, modes=None, compile_options={})
results = eng.run(prog, shots=1)
print(results.samples)

