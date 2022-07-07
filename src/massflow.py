import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def massflow(T_1,p_1,v_1,A_t,resmin,mix):
    setup.mixture_states(mix)["free_stream"].equilibrate(T_1,p_1)
    h_1 = setup.mixture_states(mix)["free_stream"].mixtureHMass() + (0.5*(v_1**2))
    s_1 = setup.mixture_states(mix)["free_stream"].mixtureSMass()
    throat_state = solver.enthalpy_entropy_solver(resmin,h_1,s_1,mix)

    T_t,p_t,v_t = throat_state.solution(T_1,p_1,1.)
    setup.mixture_states(mix)["throat"].equilibrate(T_t,p_t)
    mf = setup.mixture_states(mix)["throat"].density()*v_t*A_t

    return mf

# mix = setup.setup_mpp()
# print(massflow(5000.,10000.,4319.4480729,9.621e-04,1.0e-06,mix))