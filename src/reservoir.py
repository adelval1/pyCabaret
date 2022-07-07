import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def reservoir(T_1,p_1,v_1,resmin,mix):
    setup.mixture_states(mix)["free_stream"].equilibrate(T_1,p_1)
    h_1 = setup.mixture_states(mix)["free_stream"].mixtureHMass() + (0.5*v_1**2)
    s_1 = setup.mixture_states(mix)["free_stream"].mixtureSMass()
    reservoir_state = solver.enthalpy_entropy_solver(resmin,h_1,s_1,mix)

    return reservoir_state.solution(T_1,p_1)

# mix = setup.setup_mpp()
# print(reservoir(5000.,10000.,4319.4480729,1.0e-05,mix))