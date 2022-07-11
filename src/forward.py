import mutationpp as mpp
import rebuilding_setup as setup
import reservoir as res
import massflow as msfl
import shock as sck
import heatflux as htfl
import enthalpy_entropy_solver as solver
import total as ttl

def forward(preshock_state,resmin,A_t,reff,T_w,pr,L,mix):
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

    T0,p0,v0 = res.reservoir(T_1,p_1,h_1,s_1,resmin,mix,"reservoir")

    mf = msfl.massflow(T_1,p_1,h_1,s_1,A_t,resmin,mix,"throat")

    T_2,p_2,v_2 = sck.shock(preshock_state,mix)
    Tt2,pt2,vt2 = ttl.total(T_2,p_2,v_2,resmin,mix,"total")

    setup.mixture_states(mix)["total"].equilibrate(Tt2,pt2)
    ht2 = setup.mixture_states(mix)["total"].mixtureHMass()
    rhot2 = setup.mixture_states(mix)["total"].density()

    qw = htfl.heatflux(mix, pr, L, p_1, pt2, Tt2, ht2, reff, T_w)

    measurements = {"Reservoir_temperature": T0, 
                    "Reservoir_pressure": p0, 
                    "Mass_flow": mf, 
                    "Total_enthalpy": ht2, 
                    "Heat_flux": qw, 
                    "Stagnation_density": rhot2,
                    "Stagnation_pressure": pt2,
                    "Free_stream_density": rho_1,
                    "Free_stream_velocity": v_1

    }

    return measurements 