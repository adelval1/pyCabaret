import numpy as np 
import mutationpp as mpp
import rebuilding_setup as setup

def heatflux(mix, pr, L, p_1, p_t2, T_t2, h_t2, reff, T_w):

    mix.equilibrate(T_t2, p_t2)

    rho_t2 = mix.density()
    eta_t2 = mix.viscosity()

    mix.equilibrate(T_w, p_t2)

    eta_w = mix.viscosity()
    rho_w = mix.density()
    h_w = mix.mixtureHMass()

    du2dx=np.sqrt(2*(p_t2 -p_1)/rho_t2)/reff

    return 0.763*pr**(-0.6)*((rho_t2 * eta_t2)**0.4)*((rho_w *eta_w)**0.1)*np.sqrt(du2dx)*(h_t2 -h_w)

# mix = setup.setup_mpp()

# qw = heatflux(mix,0.7,1.,299.2,5000,10000,20000000,0.025,1000)
# print(qw)