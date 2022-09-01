## Importing local mutationpp python module ##
import argparse
import os
import sys
from .time_it import timing

mppPyDir = os.environ.get("MPP_LOCALPY")
sys.path.append(mppPyDir)


from pycabaret.inverse import inverse
from pycabaret.forward import forward
import pycabaret.rebuilding_setup as setup
import pycabaret.reading_input as input_data
import time


mix = setup.setup_mpp()


@timing
def main():
    parser = argparse.ArgumentParser(description="Enter filename")
    parser.add_argument("-f", "--filename", default="input.in", help="Filename of input parameters", type=str)
    args = parser.parse_args()

    filename = args.filename

    input_dict = input_data.reading_input(input_filename=filename)

    if input_dict["inverse"]:
        output = inverse(input_dict["measurements"], input_dict, mix)

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

        print("...in inverse mode")
        print("------------------" + "\n")
        print("For these measurements..." + "\n")
        print(
            f'{input_dict["measurements"][0]} \t {input_dict["simulated_measurements"][input_dict["measurements"][0]]}'.expandtabs(
                28
            )
        )
        print(
            f'{input_dict["measurements"][1]} \t {input_dict["simulated_measurements"][input_dict["measurements"][1]]}'.expandtabs(
                28
            )
        )
        print(
            f'{input_dict["measurements"][2]} \t {input_dict["simulated_measurements"][input_dict["measurements"][2]]}'.expandtabs(
                28
            )
        )
        print("------------------" + "\n")
        print("these free stream conditions..." + "\n")

        print(f"T1 [K]  \t {output[0]:.4f}".expandtabs(28))
        print(f"P1 [Pa]  \t {output[1]:.4f}".expandtabs(28))
        print(f"M1 [-]  \t {output[2]:.4f}".expandtabs(28))

        print("------------------" + "\n")
        print("...reproduce these observations..." + "\n")
        print(f'{input_dict["measurements"][0]} \t  {check_forward[input_dict["measurements"][0]]}'.expandtabs(28))
        print(f'{input_dict["measurements"][1]} \t {check_forward[input_dict["measurements"][1]]}'.expandtabs(28))
        print(f'{input_dict["measurements"][2]} \t {check_forward[input_dict["measurements"][2]]}'.expandtabs(28))
        print("------------------" + "\n")

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

        print("...in forward mode")
        print("------------------" + "\n")
        print("For these free stream conditions..." + "\n")
        print(f"T1 [K] \t {preshock_state[0]:.4f}".expandtabs(28))
        print(f"P1 [Pa] \t {preshock_state[1]:.4f}".expandtabs(28))
        print(f"M1 [-] \t {preshock_state[2]:.4f}".expandtabs(28))

        print("------------------")
        print("Measurements obtained..." + "\n")
        print(f"Heat flux [W/m^2] \t {output['Heat_flux']:.4f}".expandtabs(28))
        print(f"Stagnation pressure [Pa] \t {output['Stagnation_pressure']:.4f}".expandtabs(28))
        print(f"Reservoir pressure [Pa] \t {output['Reservoir_pressure']:.4f}".expandtabs(28))
        print(f"Reservoir temperature [K] \t {output['Reservoir_temperature']:.4f}".expandtabs(28))
        print(f"Total enthalpy [J/kg] \t {output['Total_enthalpy']:.4f}".expandtabs(28))
        print(f"Stagnation density [kg/m^3] \t {output['Stagnation_density']:.4f}".expandtabs(28))
        print(f"Free stream density [kg/m^3] \t {output['Free_stream_density']:.4f}".expandtabs(28))
        print(f"Mass flow [kg/s] \t {output['Mass_flow']:.4f}".expandtabs(28))
        print(f"Free stream velocity [m/s] \t {output['Free_stream_velocity']:.4f}".expandtabs(28))
        print("------------------")
