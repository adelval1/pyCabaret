import pycabaret.enthalpy_entropy_solver as solver
import pycabaret.rebuilding_setup as setup


def total(T, p, v, resmin, mix, state, options):
    """
    Function that solves the conservation equations for the computation of the total quantities.

    Parameters
    ----------
    T : float
        Temperature.
    p: float
        Pressure.
    resmin: float
        Residual.
    mix: object
        Mixture object.
    state: string
        Name of the state being computed, in this case "total".
    options: dictionary
        Options for the computation of the shocking module. Comes from the input file.

    Output
    ----------
    1D array of size 3
        T,p and v.
    """
    setup.mixture_states(mix)["post_shock"].equilibrate(T, p)
    h = setup.mixture_states(mix)["post_shock"].mixtureHMass() + (0.5 * v**2)
    s = setup.mixture_states(mix)["post_shock"].mixtureSMass()

    total_state = solver.enthalpy_entropy_solver(resmin, h, s, mix, state, "total", options)

    return total_state.solution(T, p)
