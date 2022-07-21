import numpy as np 
import enthalpy_entropy_solver as solver

def reservoir(T_1,p_1,h_1,s_1,resmin,mix,state,options):
    """
    Function that solves the conservation equations for the reservoir.

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
    resmin: float
        Residual.
    mix: object
        Mixture object.
    state: string
        Name of the state being computed, in this case "reservoir".
    options: dictionary
        Options for the computation of the shocking module. Comes from the input file.

    Output
    ----------   
    1D array of size 3
        T,p and v.  
    """
    reservoir_state = solver.enthalpy_entropy_solver(resmin,h_1,s_1,mix,state,"reservoir",options)

    return reservoir_state.solution(T_1,p_1)