import numpy as np 
import rebuilding_setup as setup
import enthalpy_entropy_solver as solver

def total(T,p,v,resmin,mix,state,options):
    setup.mixture_states(mix)["post_shock"].equilibrate(T,p)
    h = setup.mixture_states(mix)["post_shock"].mixtureHMass() + (0.5*v**2)
    s = setup.mixture_states(mix)["post_shock"].mixtureSMass()

    total_state = solver.enthalpy_entropy_solver(resmin,h,s,mix,state,"total",options)

    return total_state.solution(T,p,"lower",[T,p])