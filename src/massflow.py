import numpy as np 
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def massflow(T_1,p_1,h_1,s_1,A_t,resmin,mix,state,options):
    throat_state = solver.enthalpy_entropy_solver(resmin,h_1,s_1,mix,state,"massflow",options)

    T_t,p_t,v_t = throat_state.solution(T_1,p_1,"lower",[T_1,p_1],1.)
    setup.mixture_states(mix)[state].equilibrate(T_t,p_t)
    mf = setup.mixture_states(mix)[state].density()*v_t*A_t

    return mf