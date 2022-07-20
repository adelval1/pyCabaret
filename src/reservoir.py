import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def reservoir(T_1,p_1,h_1,s_1,resmin,mix,state,options):
    reservoir_state = solver.enthalpy_entropy_solver(resmin,h_1,s_1,mix,state,"reservoir",options)

    return reservoir_state.solution(T_1,p_1,"lower",[T_1,p_1])

# mix = setup.setup_mpp()
# print(reservoir(5000.,10000.,4319.4480729,1.0e-05,mix))