## function that populates a dictionary with the inputs ##

import yaml


def reading_input(input_filename):
    """
    Function that reads the input file and produces a dictionary with all the information.

    Output
    ----------
    input_parameters: dictionary
        Dictionary describing the information contained in the input file.
    """

    with open("input.yaml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    input_parameters = {
        "freestream": {
            "Temperature": data["FORWARD INPUT"]["Free stream temperature"],
            "Pressure": data["FORWARD INPUT"]["Free stream pressure"],
            "Mach": data["FORWARD INPUT"]["Free stream Mach number"],
        },
        "simulated_measurements": {
            "Heat_flux": data["INVERSE INPUT"]["Heat flux"],
            "Stagnation_pressure": data["INVERSE INPUT"]["Stagnation pressure"],
            "Reservoir_pressure": data["INVERSE INPUT"]["Reservoir pressure"],
            "Reservoir_temperature": data["INVERSE INPUT"]["Reservoir temperature"],
            "Total_enthalpy": data["INVERSE INPUT"]["Total enthalpy"],
            "Stagnation_density": data["INVERSE INPUT"]["Stagnation density"],
            "Free_stream_density": data["INVERSE INPUT"]["Free stream density"],
            "Mass_flow": data["INVERSE INPUT"]["Mass flow"],
            "Free_stream_velocity": data["INVERSE INPUT"]["Free stream velocity"],
            "Free_stream_pressure": data["FORWARD INPUT"]["Free stream pressure"],
        },
        "residual": data["INVERSE INPUT"]["Residual"],
        "throat_area": data["FORWARD INPUT"]["Throat area"],
        "surface_temperature": data["FORWARD INPUT"]["Surface temperature"],
        "Prandtl": data["FORWARD INPUT"]["Prandtl number"],
        "Lewis": data["FORWARD INPUT"]["Lewis number"],
        "effective_radius": data["FORWARD INPUT"]["Effective radius"],
        "inverse": data["Inverse Rebuilding"],
        "measurements": data["INVERSE INPUT"]["Measurements to rebuild from"],
        "method": data["INVERSE INPUT"]["Optimization method"],
        "maxiter": data["INVERSE INPUT"]["Maximum number of iterations"],
        "start_points": data["INVERSE INPUT"]["Number of starting points"],
        "print_info": data["INVERSE INPUT"]["Print steps"],
        "options": {
            "reservoir": {
                "pressure": data["Reservoir Parameters"]["Initial pressure"],
                "temperature": data["Reservoir Parameters"]["Initial temperature"],
                "robust": data["Reservoir Parameters"]["Robust"],
            },
            "massflow": {
                "pressure": data["Mass flow parameters"]["Initial pressure"],
                "temperature": data["Mass flow parameters"]["Initial temperature"],
                "robust": data["Mass flow parameters"]["Robust"],
            },
            "shocking": {
                "ratio": data["Shock parameters"]["Initial ratio"],
                "robust": data["Shock parameters"]["Robust"],
            },
            "total": {
                "pressure": data["Total quantities"]["Initial pressure"],
                "temperature": data["Total quantities"]["Initial temperature"],
                "robust": data["Total quantities"]["Robust"],
            },
        },
    }

    return input_parameters
