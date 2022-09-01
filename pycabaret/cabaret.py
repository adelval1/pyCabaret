## Importing local mutationpp python module ##
import argparse
import sys
import os

mppPyDir = os.environ.get("MPP_LOCALPY")
sys.path.append(mppPyDir)
##

import numpy as np
from pycabaret.inverse import inverse
from pycabaret.forward import forward
import pycabaret.rebuilding_setup as setup
import pycabaret.reading_input as input_data
import time

start_time = time.time()

mix = setup.setup_mpp()


def main():
    parser = argparse.ArgumentParser(description='Enter filename')
    parser.add_argument('-f', '--filename', default='input.in', help='Filename of input parameters', type=str)
    args = parser.parse_args()

    filename = args.filename

    input_dict = input_data.reading_input(input_filename=filename)

    if input_dict["inverse"] == "True":
        output = inverse(input_dict["measurements"], input_dict, mix)
        end_time = time.time()
        total_time = end_time - start_time

        check_forward = forward(
            output,
            input_dict["residual"],
            input_dict["throat_area"],
            input_dict["effective_radius"],
            input_dict["surface_temperature"],
            input_dict["Prandtl"],
            input_dict["Lewis"],
            mix,
            input_dict["print_info"],
            input_dict["options"],
        )

        width = [(40 - len(input_dict["measurements"][i])) for i in range(3)]
        string_width = ["{" + ":>" + str(width[i]) + ".4f}" for i in range(3)]

        print("...in inverse mode")
        print("------------------" + "\n")
        print("For these measurements..." + "\n")
        print(
            input_dict["measurements"][0]
            + string_width[0].format(input_dict["simulated_measurements"][input_dict["measurements"][0]])
        )
        print(
            input_dict["measurements"][1]
            + string_width[1].format(input_dict["simulated_measurements"][input_dict["measurements"][1]])
        )
        print(
            input_dict["measurements"][2]
            + string_width[2].format(input_dict["simulated_measurements"][input_dict["measurements"][2]])
        )
        print("------------------" + "\n")
        print("these free stream conditions..." + "\n")
        print("T1 [K]" + "{:>16.4f}".format(output[0]))
        print("P1 [Pa]" + "{:>15.4f}".format(output[1]))
        print("M1 [-]" + "{:>16.4f}".format(output[2]))
        print("------------------" + "\n")
        print("...reproduce these observations..." + "\n")
        print(input_dict["measurements"][0] + string_width[0].format(check_forward[input_dict["measurements"][0]]))
        print(input_dict["measurements"][1] + string_width[1].format(check_forward[input_dict["measurements"][1]]))
        print(input_dict["measurements"][2] + string_width[2].format(check_forward[input_dict["measurements"][2]]))
        print("------------------" + "\n")

        print(
            "Execution time = " + "{:.4f}".format(total_time),
            " seconds = " + "{:.4f}".format(total_time / 60),
            " minutes",
        )

    else:
        preshock_state = [
            input_dict["freestream"]["Temperature"],
            input_dict["freestream"]["Pressure"],
            input_dict["freestream"]["Mach"],
        ]
        output = forward(
            preshock_state,
            input_dict["residual"],
            input_dict["throat_area"],
            input_dict["effective_radius"],
            input_dict["surface_temperature"],
            input_dict["Prandtl"],
            input_dict["Lewis"],
            mix,
            input_dict["print_info"],
            input_dict["options"],
        )
        end_time = time.time()
        total_time = end_time - start_time

        print("...in forward mode")
        print("------------------" + "\n")
        print("For these free stream conditions..." + "\n")
        print("T1 [K]" + "{:>16.4f}".format(preshock_state[0]))
        print("P1 [Pa]" + "{:>15.4f}".format(preshock_state[1]))
        print("M1 [-]" + "{:>16.4f}".format(preshock_state[2]))
        print("------------------")
        print("Measurements obtained..." + "\n")
        print("Heat flux [W/m^2]" + "{:>30.4f}".format(output["Heat_flux"]))
        print("Stagnation pressure [Pa]" + "{:>23.4f}".format(output["Stagnation_pressure"]))
        print("Reservoir pressure [Pa]" + "{:>24.4f}".format(output["Reservoir_pressure"]))
        print("Reservoir temperature [K]" + "{:>22.4f}".format(output["Reservoir_temperature"]))
        print("Total enthalpy [J/kg]" + "{:>26.4f}".format(output["Total_enthalpy"]))
        print("Stagnation density [kg/m^3]" + "{:>20.4f}".format(output["Stagnation_density"]))
        print("Free stream density [kg/m^3]" + "{:>19.4f}".format(output["Free_stream_density"]))
        print("Mass flow [kg/s]" + "{:>31.4f}".format(output["Mass_flow"]))
        print("Free stream velocity [m/s]" + "{:>21.4f}".format(output["Free_stream_velocity"]))
        print("------------------")

        print(
            "Execution time = " + "{:.4f}".format(total_time),
            " seconds = " + "{:.4f}".format(total_time / 60),
            " minutes",
        )
