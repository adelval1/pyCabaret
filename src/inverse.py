import numpy as np
from module_forward import module_forward
import scipy
from scipy.optimize import minimize

def normalization(x,ub,lb):
    x_norm = [0.]*len(x)
    for i in range(len(x)):
        x_norm[i] = (x[i] - lb[i])/(ub[i]-lb[i])
    return x_norm

def denormalization(x,ub,lb):
    x_dnorm = [0.]*len(x)
    for i in range(len(x)):
        x_dnorm[i] = (x[i]*(ub[i]-lb[i])) + lb[i]
    return x_dnorm

def inverse_minimize(preshock_state_var,meas,dict,mix): # meas is list of names
    for i in range(len(preshock_state_var)):
        if preshock_state_var[i]>1.0 or preshock_state_var[i]<0.:
            return 1.0e+16

    preshock_state = denormalization(preshock_state_var,[20000.,50000.,20.],[300.,50.,1.01])

    measurements_dict = module_forward(preshock_state,dict["residual"],dict["throat_area"],dict["effective_radius"],dict["surface_temperature"],dict["Prandtl"],dict["Lewis"],mix,dict["measurements"],dict["print_info"],dict["options"])

    res = [(dict["simulated_measurements"][meas[i]] - measurements_dict[meas[i]])/dict["simulated_measurements"][meas[i]] for i in range(len(meas))]
    res_norm = np.linalg.norm(res)

    return res_norm

def vect_inverse_minimize(preshock_state_var,meas,dict,mix): # meas is list of names
    for i in range(len(preshock_state_var)):
        if preshock_state_var[i]>1.0 or preshock_state_var[i]<0.:
            return [1.0e+16]*len(preshock_state_var)

    preshock_state = denormalization(preshock_state_var,[20000.,50000.,20.],[300.,50.,1.01])

    measurements_dict = module_forward(preshock_state,dict["residual"],dict["throat_area"],dict["effective_radius"],dict["surface_temperature"],dict["Prandtl"],dict["Lewis"],mix,dict["measurements"],dict["print_info"],dict["options"])

    res = [(dict["simulated_measurements"][meas[i]] - measurements_dict[meas[i]])/dict["simulated_measurements"][meas[i]] for i in range(len(meas))]
    res_norm = [np.linalg.norm(res[i]) for i in range(3)]

    return res_norm

def jacobian(preshock_state_var,meas,dict,mix):
    jacob = scipy.optimize.approx_fprime(preshock_state_var,inverse_minimize,1.4901161193847656e-08,meas,dict,mix)
    return jacob

def inverse(meas,dict,mix):

    preshock_state_var = normalization([dict["freestream"]["Temperature"],dict["freestream"]["Pressure"],dict["freestream"]["Mach"]],[20000.,50000.,20.],[300.,50.,1.01])
    
    options={'maxiter': dict["maxiter"]}
    bnds = ((0.,1.), (0.,1.), (0.,1.)) #0.1, 1.01

    if dict["start_points"]>1:
        evals = [0.]*dict["start_points"]
        xevals = np.array((dict["start_points"],3))
        for i in range(dict["start_points"]):
            preshock_state_var = [np.random.random(),np.random.random(),np.random.random()]
            if dict["method"] == "Root":
                result = scipy.optimize.root(vect_inverse_minimize,preshock_state_var,args=(meas,dict,mix),tol=dict["residual"])
            elif dict["method"] == "Hybrid":
                result = scipy.optimize.minimize(inverse_minimize,preshock_state_var,args=(meas,dict,mix),method="L-BFGS-B",tol=1.0e-03,options=options)
                preshock_state_var = result.x
                result = scipy.optimize.root(vect_inverse_minimize,preshock_state_var,args=(meas,dict,mix),tol=dict["residual"])
            else:
                result = scipy.optimize.minimize(inverse_minimize,preshock_state_var,args=(meas,dict,mix),method=dict["method"],tol=dict["residual"],bounds=bnds,options=options)
            evals[i] = result.fun
            print(result.message)

        position = np.argmin(evals)
        x = xevals[position]
    else:
        if dict["method"] == "Root":
            result = scipy.optimize.root(vect_inverse_minimize,preshock_state_var,args=(meas,dict,mix),tol=dict["residual"])
        elif dict["method"] == "Hybrid":
            result = scipy.optimize.minimize(inverse_minimize,preshock_state_var,args=(meas,dict,mix),method="L-BFGS-B",tol=1.0e-03,options=options)
            preshock_state_var = result.x
            result = scipy.optimize.root(vect_inverse_minimize,preshock_state_var,args=(meas,dict,mix),tol=dict["residual"])
        else:
            result = scipy.optimize.minimize(inverse_minimize,preshock_state_var,args=(meas,dict,mix),method=dict["method"],tol=dict["residual"],options=options)
        print(result.message)
        print("Residual value = ", result.fun)
        x = result.x

    return denormalization(x,[20000.,50000.,20.],[300.,50.,1.01])