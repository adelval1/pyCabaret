import numpy as np 

# Based on Modified Newtonian Theory
def velocity_gradient(p_t2,p_1,rho_t2,reff):
    """
    Function that computes the velocity gradient needed for heat flux computations.

    Parameters
    ----------
    p_t2 : float
        Stagnation pressure.
    p_1: float
        Free stream pressure.
    rho_t2: float
        Stagnation density.

    Output
    ----------   
    float
        Velocity gradient.  
    """
    return np.sqrt(2*(p_t2 -p_1)/rho_t2)/reff

# Based on Fay-Riddell
def heatflux(mix, pr, L, p_1, p_t2, T_t2, h_t2, reff, T_w):
    """
    Function that computes the heat flux.

    Parameters
    ----------
    mix : object
        Mixture.
    pr: float
        Prandtl number.
    L: float
        Lewis number.
    p_1: float
        Free stream pressure.
    p_t2: float
        Stagnation pressure.
    T_t2: float
        Stagnation temperature.
    h_t2: float
        Stagnation enthalpy
    reff: float
        Effective radius.
    T_w: float
        Wall temperature.

    Output
    ----------   
    float
        Heat flux in W/m2  
    """

    # Boundary layer edge state
    mix.equilibrate(T_t2, p_t2)

    rho_t2 = mix.density()
    eta_t2 = mix.viscosity()

    # Wall state
    mix.equilibrate(T_w, p_t2)

    eta_w = mix.viscosity()
    rho_w = mix.density()
    h_w = mix.mixtureHMass()

    # Velocity gradient
    du2dx = velocity_gradient(p_t2,p_1,rho_t2,reff)

    return 0.763*pr**(-0.6)*((rho_t2 * eta_t2)**0.4)*((rho_w *eta_w)**0.1)*np.sqrt(du2dx)*(h_t2 -h_w)