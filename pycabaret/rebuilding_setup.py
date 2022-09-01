import os

import mutationpp as mpp
import yaml


def setup_mpp():
    """
    Function that sets up the mixture.

    Output
    ----------
    mix: object
        Mixture object from the mpp module.
    """

    path_to_this_file = os.path.dirname(os.path.realpath(__file__))

    with open("input.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    mixture = data["MIXTURE"]["Type"]
    thermo = data["MIXTURE"]["Thermodynamics"]
    state = data["MIXTURE"]["State model"]

    ## Setting up Mutation++ options and mixture
    opts = mpp.MixtureOptions(mixture)
    opts.setThermodynamicDatabase(thermo)
    opts.setStateModel(state)

    mix = mpp.Mixture(mixture)
    mix = mpp.Mixture(opts)

    return mix


def mixture_states(mix):
    """
    Function that assigns the mixture to the different flow states: reservoir, free stream, post shock, total and nozzle throat.

    Parameters
    ----------
    mix: object
        Mixture object from the mpp module.

    Output
    ----------
    states: dictionary
        Dictionary containing different mixtures for each flow state so they do not change each other's when invoking the "equilibrate" mutation function.
    """
    mix_freeStream = mix
    mix_ps = mix
    mix_total = mix
    mix_res = mix
    mix_thr = mix
    states = {
        "free_stream": mix_freeStream,
        "post_shock": mix_ps,
        "total": mix_total,
        "reservoir": mix_res,
        "throat": mix_thr,
    }
    return states
