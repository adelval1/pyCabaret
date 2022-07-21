import mutationpp as mpp
import rebuilding_setup as setup
from reservoir import reservoir
from massflow import massflow
from shock import shock
from heatflux import heatflux
from total import total
import time

def forward(preshock_state,resmin,A_t,reff,T_w,pr,L,mix,print_info,options):
    """
    Function that computes all quantities of interest from the free stream state.

    Parameters
    ----------
    preshock_state : 1D array of size 3
        Free stream temperature, pressure and Mach number.
    resmin : float
        Residual for convergence of all modules except shocking.
    A_t: float
        Throat area needed for mass flow computations in m^2.
    reff: float
        Effective radius in m.
    T_w: float
        Wall temperature in K.
    pr: float
        Prandtl number.
    L: float
        Lewis number
    mix: object
        Mixture object from the mpp module.
    print_info: string
        String that specifies if step information will be printed out.
    options: dictionary
        Dictionary of options for the different modules

    Output
    ----------   
    measurements: dictionary
        Dictionary containing the results of all modules.     
    """

    if print_info == "Yes":
        print(preshock_state)

    T_1 = preshock_state[0]
    p_1 = preshock_state[1]
    M_1 = preshock_state[2]

    # Setting up the free stream quantities
    mix = setup.setup_mpp()
    setup.mixture_states(mix)["free_stream"].equilibrate(T_1,p_1)
    rho_1 = setup.mixture_states(mix)["free_stream"].density()
    v_1 = M_1*setup.mixture_states(mix)["free_stream"].equilibriumSoundSpeed()
    h_1 = setup.mixture_states(mix)["free_stream"].mixtureHMass() + (0.5*v_1**2)
    s_1 = setup.mixture_states(mix)["free_stream"].mixtureSMass()

    # Reservoir computation
    T0,p0,v0 = reservoir(T_1,p_1,h_1,s_1,resmin,mix,"reservoir",options["reservoir"])

    # Mass flow computation
    mf = massflow(T_1,p_1,h_1,s_1,A_t,resmin,mix,"throat",options["massflow"])

    # Shocking computation
    T_2,p_2,v_2 = shock(preshock_state,mix,options["shocking"])

    # Stagnation quantities
    Tt2,pt2,vt2 = total(T_2,p_2,v_2,resmin,mix,"total",options["total"])

    start_time = time.time()
    setup.mixture_states(mix)["total"].equilibrate(Tt2,pt2)
    ht2 = setup.mixture_states(mix)["total"].mixtureHMass()
    rhot2 = setup.mixture_states(mix)["total"].density()

    # Heat flux computation
    qw = heatflux(mix, pr, L, p_1, pt2, Tt2, ht2, reff, T_w)

    measurements = {"Reservoir_temperature": T0, 
                    "Reservoir_pressure": p0, 
                    "Mass_flow": mf, 
                    "Total_enthalpy": ht2, 
                    "Heat_flux": qw, 
                    "Stagnation_density": rhot2,
                    "Stagnation_pressure": pt2,
                    "Free_stream_density": rho_1,
                    "Free_stream_velocity": v_1,
                    "Free_stream_pressure": p_1

    }

    return measurements 