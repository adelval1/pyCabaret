import numpy as np
from .module_forward import module_forward
import scipy
from scipy.optimize import minimize
from .metric_minimization import metric


def normalization(x, ub, lb):
    """
    Function that normalizes a quantity x for given upper and lower bounds.

    Parameters
    ----------
    x : float or 1D array
        Quantity to normalize.
    ub : float or 1D array
        Upper bounds of each component of x.
    lb: float
        Lower bounds of each component of x.

    Output
    ----------
    x_norm: float or 1D array
        Normalized quantity
    """
    x_norm = [0.0] * len(x)
    for i in range(len(x)):
        x_norm[i] = (x[i] - lb[i]) / (ub[i] - lb[i])
    return x_norm


def denormalization(x, ub, lb):
    """
    Function that de-normalizes a quantity x for given upper and lower bounds.

    Parameters
    ----------
    x : float or 1D array
        Quantity to de-normalize.
    ub : float or 1D array
        Upper bounds of each component of x.
    lb: float
        Lower bounds of each component of x.

    Output
    ----------
    x_dnorm: float or 1D array
        De-normalized quantity
    """
    x_dnorm = [0.0] * len(x)
    for i in range(len(x)):
        x_dnorm[i] = (x[i] * (ub[i] - lb[i])) + lb[i]
    return x_dnorm


def inverse_minimize(preshock_state_var, meas, dict, mix, method):
    """
    Function to minimize.

    Parameters
    ----------
    preshock_state_var : 1D array of shape 3
        Normalized free stream state variables.
    meas : list
        List of names of the different modules.
    dict : Dictionary
        Dictionary with the input file variables.
    mix: object
        Mixture object from the mpp module.

    Output
    ----------
    res_norm: float
        Error metric to be minimized.
    """
    if method == "Root":
        for i in range(len(preshock_state_var)):
            if preshock_state_var[i] > 1.0 or preshock_state_var[i] < 0.0:
                return [1.0e16] * len(preshock_state_var)
    else:
        for i in range(len(preshock_state_var)):
            if preshock_state_var[i] > 1.0 or preshock_state_var[i] < 0.0:
                return 1.0e16

    preshock_state = denormalization(preshock_state_var, [20000.0, 50000.0, 20.0], [300.0, 50.0, 1.01])

    measurements_dict = module_forward(
        preshock_state,
        dict["residual"],
        dict["throat_area"],
        dict["effective_radius"],
        dict["surface_temperature"],
        dict["Prandtl"],
        dict["Lewis"],
        mix,
        dict["measurements"],
        dict["print_info"],
        dict["options"],
    )

    res = [
        (dict["simulated_measurements"][meas[i]] - measurements_dict[meas[i]])
        / dict["simulated_measurements"][meas[i]]
        for i in range(len(meas))
    ]

    if method == "Root":
        res_norm = [np.linalg.norm(res[i]) for i in range(3)]
    else:
        res_norm = np.linalg.norm(res)

    return res_norm


def jacobian(preshock_state_var, meas, dict, mix):
    """
    Function that computes the Jacobian matrix.

    Parameters
    ----------
    preshock_state_var : 1D array of shape 3.
        Normalized free stream state variables.
    meas : list
        List of names of the different modules.
    dict : Dictionary
        Dictionary with the input file variables.
    mix: object
        Mixture object from the mpp module.

    Output
    ----------
    jacob: ndarray or matrix of shape (3,3)
        Jacobian matrix.
    """
    jacob = scipy.optimize.approx_fprime(
        preshock_state_var, inverse_minimize, 1.4901161193847656e-08, meas, dict, mix
    )
    return jacob


def inverse(meas, dict, mix):
    """
    Function that parses the input file for the optimization method and computes the free stream variables.

    Parameters
    ----------
    meas : list
        List of names of the different modules.
    dict : Dictionary
        Dictionary with the input file variables.
    mix: object
        Mixture object from the mpp module.

    Output
    ----------
    1D array of shape 3
        Vector with the free stream state variables
    """

    preshock_state_var = normalization(
        [dict["freestream"]["Temperature"], dict["freestream"]["Pressure"], dict["freestream"]["Mach"]],
        [20000.0, 50000.0, 20.0],
        [300.0, 50.0, 1.01],
    )

    options = {"maxiter": dict["maxiter"]}
    bnds = ((0.0, 1.0), (0.0, 1.0), (0.0, 1.0))  # 0.1, 1.01

    if dict["start_points"] > 1:
        evals = [0.0] * dict["start_points"]
        xevals = np.array((dict["start_points"], 3))
        for i in range(dict["start_points"]):
            preshock_state_var = [np.random.random(), np.random.random(), np.random.random()]
            if dict["method"] == "Root":
                result = scipy.optimize.root(
                    inverse_minimize,
                    preshock_state_var,
                    args=(meas, dict, mix, dict["method"]),
                    tol=dict["residual"],
                )
            elif dict["method"] == "Hybrid":
                result = scipy.optimize.minimize(
                    inverse_minimize,
                    preshock_state_var,
                    args=(meas, dict, mix, dict["method"]),
                    method="L-BFGS-B",
                    tol=1.0e-03,
                    options=options,
                )
                preshock_state_var = result.x
                result = scipy.optimize.root(
                    inverse_minimize,
                    preshock_state_var,
                    args=(meas, dict, mix, dict["method"]),
                    tol=dict["residual"],
                )
            else:
                result = scipy.optimize.minimize(
                    inverse_minimize,
                    preshock_state_var,
                    args=(meas, dict, mix, dict["method"]),
                    method=dict["method"],
                    tol=dict["residual"],
                    bounds=bnds,
                    options=options,
                )
            evals[i] = result.fun
            print(result.message)

        position = np.argmin(evals)
        x = xevals[position]
    else:
        if dict["method"] == "Root":
            result = scipy.optimize.root(
                inverse_minimize, preshock_state_var, args=(meas, dict, mix, dict["method"]), tol=dict["residual"]
            )
        elif dict["method"] == "Hybrid":
            result = scipy.optimize.minimize(
                inverse_minimize,
                preshock_state_var,
                args=(meas, dict, mix, dict["method"]),
                method="L-BFGS-B",
                tol=1.0e-03,
                options=options,
            )
            preshock_state_var = result.x
            result = scipy.optimize.root(
                inverse_minimize, preshock_state_var, args=(meas, dict, mix, dict["method"]), tol=dict["residual"]
            )
        else:
            result = scipy.optimize.minimize(
                inverse_minimize,
                preshock_state_var,
                args=(meas, dict, mix, dict["method"]),
                method=dict["method"],
                tol=dict["residual"],
                options=options,
            )
        print(result.message)
        print("Residual value = ", result.fun)
        x = result.x

    return denormalization(x, [20000.0, 50000.0, 20.0], [300.0, 50.0, 1.01])
