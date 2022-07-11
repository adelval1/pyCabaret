import mutationpp as mpp
import numpy as np

def setup_mpp():

    with open('../input.in', 'r') as f:
        lines = f.readlines()

    mixture = lines[12].strip()
    thermo = lines[16].strip()
    state = lines[20].strip()

    ## Setting up Mutation++ options and mixture
    opts = mpp.MixtureOptions(mixture)
    opts.setThermodynamicDatabase(thermo)
    opts.setStateModel(state)

    mix = mpp.Mixture(mixture)
    mix  = mpp.Mixture(opts)

    return mix

def mixture_states(mix):
    mix_freeStream = mix
    mix_ps = mix
    mix_total = mix
    mix_res = mix   
    mix_thr = mix 
    states = {"free_stream": mix_freeStream,
              "post_shock": mix_ps,
              "total": mix_total,
              "reservoir": mix_res,
              "throat": mix_thr

    }
    return states