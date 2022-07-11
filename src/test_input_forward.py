import numpy as np
import os

T = np.linspace(1000.,15000.,100)
P = np.linspace(500.,20000.,100)
M = np.linspace(1.05,6.0,100)

for i in range(100):
    with open('../input.in', 'r') as f:
        lines = f.readlines()

    lines[27] = str(T[np.random.randint(0,99)])+'\n'
    lines[31] = str(P[np.random.randint(0,99)])+'\n'
    lines[35] = str(M[np.random.randint(0,99)])+'\n'

    with open('../input.in', 'w') as f:
        lines = f.writelines(lines)

    os.system("python3 cabaret.py")