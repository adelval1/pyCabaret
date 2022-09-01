import numpy as np
import sys
import pycabaret

from pycabaret.reservoir import reservoir
import pycabaret.rebuilding_setup as setup

options = {"pressure": 10000.0, "temperature": 100.0, "robust": "Yes"}

T_1 = 3500.0
p_1 = 5000.0
M_1 = 2.0

mix = setup.setup_mpp()
setup.mixture_states(mix)["reservoir"].equilibrate(T_1, p_1)
v_1 = M_1 * setup.mixture_states(mix)["reservoir"].equilibriumSoundSpeed()
h_1 = setup.mixture_states(mix)["reservoir"].mixtureHMass() + (0.5 * v_1**2)
s_1 = setup.mixture_states(mix)["reservoir"].mixtureSMass()

print(reservoir(T_1, p_1, h_1, s_1, 1.0e-06, mix, "reservoir", options))
