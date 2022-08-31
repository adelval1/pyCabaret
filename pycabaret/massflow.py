import numpy as np 
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def massflow(T_1,p_1,h_1,s_1,A_t,resmin,mix,state,options):
    """
    Function that solves the conservation equations for the computation of the massflow along the nozzle.

    Parameters
    ----------
    T_1 : float
        Temperature.
    p_1: float
        Pressure.
    h_1: float
        Free stream enthalpy.
    s_1: float
        Free stream entropy.
    A_t: float
        Cross-section of the nozzle throat.
    resmin: float
        Residual.
    mix: object
        Mixture object.
    state: string
        Name of the state being computed, in this case "massflow".
    options: dictionary
        Options for the computation of the shocking module. Comes from the input file.

    Output
    ----------   
    mf: float
        Mass flow.  
    """
    throat_state = solver.enthalpy_entropy_solver(resmin,h_1,s_1,mix,state,"massflow",options)

    T_t,p_t,v_t = throat_state.solution(T_1,p_1,1.)
    setup.mixture_states(mix)[state].equilibrate(T_t,p_t)
    mf = setup.mixture_states(mix)[state].density()*v_t*A_t

    return mf