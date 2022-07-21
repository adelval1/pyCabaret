import numpy as np
import scipy
import rebuilding_setup as setup
from scipy.optimize import minimize

resmin = 1.0e-06

def inner_loop_temp(T,P,RHS,mix):
    """
    Function that loops over the temperature to match the enthalpy.

    Parameters
    ----------
    T : float
        Temperature.
    P: float
        Pressure.
    RHS: float
        Right Hand Side of the energy conservation equation which we seek to match.
    mix: object
        Mixture object.

    Output
    ----------   
    dT: float
        Temperature step.  
    """
    if T<0.0: # To avoid unphysical values
        return 1.0e+16
    setup.mixture_states(mix)["post_shock"].equilibrate(T,P)

    h_eq = setup.mixture_states(mix)["post_shock"].mixtureHMass()
    cp_eq = setup.mixture_states(mix)["post_shock"].mixtureFrozenCpMass()

    dT = np.abs((h_eq-RHS)/cp_eq)

    return dT

    
def func_minimize(ratio,var,c,p_1,v_1,rho_1,h_1,T_1,mix,options):
    """
    Function that computes the differences in density ratios from one iteration to the next in order to solve the RH system.

    Parameters
    ----------
    ratio : float
        Density ratio.
    var: 1D array of size 2
        Temperature and pressure in the post-shock region.
    c: 1D array of size 3
        mass, momentum and energy of the pre-shock state, quantities to be conserved across the shock.
    p_1: float
        Free stream pressure.
    v_1: float
        Free stream velocity.
    rho_1: float
        Free stream density.
    h_1: float
        Free stream enthalpy.
    T_1: float
        Free stream temperature.
    mix: object
        Mixture.
    options: dictionary
        Options for the computation of the shocking module. Comes from the input file.

    Output
    ----------   
    res_ratio: float 
        Density ratio residual.  
    """

    var[1] = p_1 + c[0]*v_1*(1.-ratio)
    rho_eq = rho_1/ratio
    RHS  = h_1 + (0.5*v_1*v_1*(1. - (ratio*ratio)))

    init = var[0]
    if options["robust"] == "Yes":
        temp_loop = scipy.optimize.minimize(inner_loop_temp,var[0],args=(var[1],RHS,mix),method='Nelder-Mead',tol=resmin)

    else:
        temp_loop = scipy.optimize.root(inner_loop_temp,var[0],args=(var[1],RHS,mix),tol=resmin)

    var[0] = temp_loop.x
    setup.mixture_states(mix)["post_shock"].equilibrate(var[0],var[1])
    rho_eq = setup.mixture_states(mix)["post_shock"].density()

    # Density ratio update and residual
    old_ratio = ratio
    ratio = rho_1/rho_eq

    res_ratio = np.abs((ratio - old_ratio)/ratio)

    return res_ratio


def shock(preshock_state,mix,options):
    """
    Function that computes the post shock state.

    Parameters
    ----------
    preshock_state : 1D array of size 2
        Temperature and pressure of the pre shock state.
    mix: object
        Mixture.
    options: dictionary
        Options for the computation of the shocking module. Comes from the input file.

    Output
    ----------   
    1D array of shape 3
        Vector with the resulting post shock T,p and v.  
    """

    ## Initialization ##
    setup.mixture_states(mix)["free_stream"].equilibrate(preshock_state[0],preshock_state[1])
    rho_1 = setup.mixture_states(mix)["free_stream"].density()
    v_1 = preshock_state[2]*setup.mixture_states(mix)["free_stream"].equilibriumSoundSpeed()
    h_1 = setup.mixture_states(mix)["free_stream"].mixtureHMass()

    ## Conserved quantities ##
    mdot = rho_1*v_1
    momentum = mdot*v_1+preshock_state[1]
    E = h_1 + 0.5*v_1*v_1

    c = [mdot,momentum,E]

    # Initial Guess
    ratio = options["ratio"]
    T_eq = preshock_state[0]
    p_eq = preshock_state[1]
    u_eq = v_1

    var = [T_eq,p_eq]

    # Outer loop for Mass/Momentum
    ratio_init = ratio
    if options["robust"] == "Yes":
        result = scipy.optimize.minimize(func_minimize,ratio_init,args=(var,c,preshock_state[1],v_1,rho_1,h_1,preshock_state[0],mix,options),method='Nelder-Mead',tol=resmin)
        if result.success == False:
            print("Warning: convergence not guaranteed for shocking")
    else:
        result = scipy.optimize.root(func_minimize,ratio,args=(var,c,preshock_state[1],v_1,rho_1,h_1,preshock_state[0],mix,options),tol=resmin)
        if result.success == False:
            print("Warning: convergence not guaranteed for shocking")

    v_eq = v_1*result.x
    setup.mixture_states(mix)["post_shock"].equilibrate(var[0],var[1])
    M_eq = v_eq/setup.mixture_states(mix)["post_shock"].equilibriumSoundSpeed()

    postshock_state = [var[0][0],var[1][0],v_eq[0]] # T, P, V

    return postshock_state[0],postshock_state[1],postshock_state[2]