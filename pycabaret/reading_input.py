## function that populates a dictionary with the inputs ##
def reading_input(input_filename):
    """
    Function that reads the input file and produces a dictionary with all the information.

    Output
    ----------
    input_parameters: dictionary
        Dictionary describing the information contained in the input file.
    """

    with open(f"{input_filename}", "r") as f:
        lines = f.readlines()

    input_parameters = {
        "freestream": {
            "Temperature": float(lines[27].strip()),
            "Pressure": float(lines[31].strip()),
            "Mach": float(lines[35].strip()),
        },
        "simulated_measurements": {
            "Heat_flux": float(lines[72].strip()),
            "Stagnation_pressure": float(lines[76].strip()),
            "Reservoir_pressure": float(lines[80].strip()),
            "Reservoir_temperature": float(lines[84].strip()),
            "Total_enthalpy": float(lines[88].strip()),
            "Stagnation_density": float(lines[92].strip()),
            "Free_stream_density": float(lines[96].strip()),
            "Mass_flow": float(lines[100].strip()),
            "Free_stream_velocity": float(lines[104].strip()),
            "Free_stream_pressure": float(lines[31].strip()),
        },
        "residual": float(lines[62].strip()),
        "throat_area": float(lines[39].strip()),
        "surface_temperature": float(lines[55].strip()),
        "Prandtl": float(lines[43].strip()),
        "Lewis": float(lines[47].strip()),
        "effective_radius": float(lines[51].strip()),
        "inverse": lines[5].strip(),
        "measurements": [lines[66].strip(), lines[67].strip(), lines[68].strip()],
        "method": lines[108].strip(),
        "maxiter": int(lines[112].strip()),
        "start_points": int(lines[116].strip()),
        "print_info": lines[120].strip(),
        "options": {
            "reservoir": {
                "pressure": float(lines[133].strip()),
                "temperature": float(lines[129].strip()),
                "robust": lines[137].strip(),
            },
            "massflow": {
                "pressure": float(lines[147].strip()),
                "temperature": float(lines[143].strip()),
                "robust": lines[151].strip(),
            },
            "shocking": {"ratio": float(lines[157].strip()), "robust": lines[161].strip()},
            "total": {
                "pressure": float(lines[171].strip()),
                "temperature": float(lines[167].strip()),
                "robust": lines[175].strip(),
            },
        },
    }

    return input_parameters
