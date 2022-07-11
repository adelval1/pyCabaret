import numpy as np
import forward as frwd
import scipy
from scipy.optimize import minimize

def inverse_minimize(preshock_state_var,meas,dict,mix,resini): # meas is list of names

    preshock_state = [preshock_state_var[0]*dict["freestream"]["Temperature"],preshock_state_var[1]*dict["freestream"]["Pressure"],preshock_state_var[2]*dict["freestream"]["Mach"]]

    measurements_dict = frwd.forward(preshock_state,dict["residual"],dict["throat_area"],dict["effective_radius"],dict["surface_temperature"],dict["Prandtl"],dict["Lewis"],mix)

    res = [(dict["simulated_measurements"][meas[i]] - measurements_dict[meas[i]])/dict["simulated_measurements"][meas[i]] for i in range(len(meas))]
    res_norm = np.linalg.norm(res)#/resini

    return res_norm


def inverse(meas,dict,mix):
    ## Initial condition ##
    preshock_state_var = [1.0,1.0,1.0]
    resini = 1.0
    resini = inverse_minimize(preshock_state_var,meas,dict,mix,resini)

    options={'maxiter': dict["maxiter"]}
    bnds = ((0.1, None), (0.1, None), (1.01/dict["freestream"]["Mach"], None))

    result = scipy.optimize.minimize(inverse_minimize,preshock_state_var,args=(meas,dict,mix,resini),method=dict["method"],tol=dict["residual"],bounds=bnds,options=options)
    print(result)

    return result.x
