import mutationpp as mpp
import numpy as np

def setup_mpp():

    with open('../input.in', 'r') as f:
        lines = f.readlines()

    mixture = lines[5].strip()
    thermo = lines[9].strip()
    state = lines[13].strip()

    ## Setting up Mutation++ options and mixture
    opts = mpp.MixtureOptions(mixture)
    opts.setThermodynamicDatabase(thermo)
    opts.setStateModel(state)

    mix = mpp.Mixture(mixture)
    mix = mpp.Mixture(opts)
    
    return mix