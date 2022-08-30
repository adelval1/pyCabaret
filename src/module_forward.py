import _mutationpp as mpp
import rebuilding_setup as setup
from reservoir import reservoir
from massflow import massflow
from shock import shock
from heatflux import heatflux
from total import total
import time

def module_forward(preshock_state,resmin,A_t,reff,T_w,pr,L,mix,meas,print_info,options):
    """
    Function that computes the quantities of interest from which to rebuild as specified by the input file from the free stream state.

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
        Dictionary containing the results of the invoked modules.     
    """
    if print_info == "Yes":
        print(preshock_state)

    T_1 = preshock_state[0]
    p_1 = preshock_state[1]
    M_1 = preshock_state[2]

    mix = setup.setup_mpp()
    setup.mixture_states(mix)["free_stream"].equilibrate(T_1,p_1)
    rho_1 = setup.mixture_states(mix)["free_stream"].density()
    v_1 = M_1*setup.mixture_states(mix)["free_stream"].equilibriumSoundSpeed()
    h_1 = setup.mixture_states(mix)["free_stream"].mixtureHMass() + (0.5*v_1**2)
    s_1 = setup.mixture_states(mix)["free_stream"].mixtureSMass()

    measurements = {}
    result = [0.]*len(meas)

    if "Reservoir_temperature" in meas or "Reservoir_pressure" in meas:
        T0,p0,v0 = reservoir(T_1,p_1,h_1,s_1,resmin,mix,"reservoir",options["reservoir"])

        if "Reservoir_temperature" in meas:
            result[meas.index("Reservoir_temperature")] = T0

        if "Reservoir_pressure" in meas:
            result[meas.index("Reservoir_pressure")] = p0

    if "Mass_flow" in meas:
        mf = massflow(T_1,p_1,h_1,s_1,A_t,resmin,mix,"throat",options["massflow"])
        result[meas.index("Mass_flow")] = mf

    if "Stagnation_pressure" in meas or "Heat_flux" in meas or "Total_enthalpy" in meas or "Stagnation_density" in meas:
        T_2,p_2,v_2 = shock(preshock_state,mix,options["shocking"])
        Tt2,pt2,vt2 = total(T_2,p_2,v_2,resmin,mix,"total",options["total"])

        setup.mixture_states(mix)["total"].equilibrate(Tt2,pt2)
        ht2 = setup.mixture_states(mix)["total"].mixtureHMass()
        rhot2 = setup.mixture_states(mix)["total"].density()

        qw = heatflux(mix, pr, L, p_1, pt2, Tt2, ht2, reff, T_w)

        if "Stagnation_pressure" in meas:
            result[meas.index("Stagnation_pressure")] = pt2

        if "Heat_flux" in meas:
            result[meas.index("Heat_flux")] = qw

        if "Total_enthalpy" in meas:
            result[meas.index("Total_enthalpy")] = ht2

        if "Stagnation_density" in meas:
            result[meas.index("Stagnation_density")] = rhot2

    if "Free_stream_pressure" in meas:
        result[meas.index("Free_stream_pressure")] = p_1

    for i in range(len(meas)):
        measurements[meas[i]] = result[i]

    return measurements 