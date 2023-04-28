import numpy as np
import sys
import time
import os

# To run locally and find the modules in /src
cabaret_src_folder = '/Users/anabel/Documents/PhD/Code/pyCabaret/src' # Change to your folder path
sys.path.insert(0, cabaret_src_folder)

mutation_folder = "/Users/anabel/Documents/PhD/Code/Mpp_test/Mutationpp/" # Your folder
my_distribution = "macosx-10.15-x86_64-3.9" # Your particular distribution
sys.path.append(mutation_folder + "_skbuild/" + my_distribution +"/cmake-install/interface/python/mutationpp")

import _mutationpp as mpp
from reservoir import reservoir
from massflow import massflow
from shock import shock
from total import total
from heatflux import heatflux
import rebuilding_setup as setup
import reading_input as input_data

# Free stream conditions
T_1 = 3500.0
p_1 = 5000.0
M_1 = 2.0

# Mutation++ mixture setup
mix = setup.setup_mpp()

# Specify module options
options = {"ratio": 0.2, 
           "robust": "No"}

preshock_state = [T_1,p_1,M_1]

start_time = time.time()
T2,p2,v2 = shock(preshock_state,mix,options)
end_time = time.time()
exec_time = end_time - start_time

print('T2 = '+ "{:.2f}".format(T2)+' K;', 'p2 = '+ "{:.2f}".format(p2)+' Pa;', 'v2 = '+ "{:.2f}".format(v2)+' m/s')
print('Execution time = '+"{:.4f}".format(exec_time), ' seconds = '+"{:.4f}".format(exec_time/60), ' minutes')