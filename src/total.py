import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def total(T,p,v,resmin,mix,state):
    setup.mixture_states(mix)["post_shock"].equilibrate(T,p)
    h = setup.mixture_states(mix)["post_shock"].mixtureHMass() + (0.5*v**2)
    s = setup.mixture_states(mix)["post_shock"].mixtureSMass()

    total_state = solver.enthalpy_entropy_solver(resmin,h,s,mix,state,"total")

    return total_state.solution(T,p,"lower",[T,p])

# mix = setup.setup_mpp()
# Tt,pt,vt = total(6545.53,96738.05,678.32,1.0e-05,mix)
# print(Tt,pt)
# setup.mixture_states(mix)["post_shock"].equilibrate(Tt,pt)
# print(setup.mixture_states(mix)["post_shock"].mixtureHMass())