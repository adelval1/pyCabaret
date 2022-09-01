import numpy as np
import os

# NOT SURE WHAT THIS TEST IS ABOUT, BUT IT NEEDS TO BE UPDATED AND MOVE TO THE TESTS FOLDER.
import yaml

T = np.linspace(1000.0, 15000.0, 100)
P = np.linspace(500.0, 20000.0, 100)
M = np.linspace(1.05, 6.0, 100)

for i in range(100):

    with open("input.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    with open("input.in", "r") as f:
        lines = f.readlines()

    lines[27] = str(T[np.random.randint(0, 99)]) + "\n"
    lines[31] = str(P[np.random.randint(0, 99)]) + "\n"
    lines[35] = str(M[np.random.randint(0, 99)]) + "\n"

    with open("input.in", "w") as f:
        lines = f.writelines(lines)

    os.system("python3 cabaret.py")
