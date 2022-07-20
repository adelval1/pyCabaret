import numpy as np
import inverse as inv
import forward as forw
import rebuilding_setup as setup
import time

start_time = time.time()
 
## function that populates a dictionary with the inputs ##
def reading_input():
    with open('../input.in', 'r') as f:
        lines = f.readlines()

    input_parameters = {"freestream":{"Temperature": float(lines[27].strip()), "Pressure": float(lines[31].strip()), "Mach": float(lines[35].strip())},
                        "simulated_measurements": {"Heat_flux": float(lines[72].strip()),"Stagnation_pressure": float(lines[76].strip()), "Reservoir_pressure": float(lines[80].strip()), "Reservoir_temperature": float(lines[84].strip()), "Total_enthalpy": float(lines[88].strip()), "Stagnation_density": float(lines[92].strip()), "Free_stream_density": float(lines[96].strip()), "Mass_flow": float(lines[100].strip()), "Free_stream_velocity": float(lines[104].strip()), "Free_stream_pressure": float(lines[31].strip())},
                        "residual": float(lines[62].strip()),
                        "throat_area": float(lines[39].strip()),
                        "surface_temperature": float(lines[55].strip()),
                        "Prandtl": float(lines[43].strip()),
                        "Lewis": float(lines[47].strip()),
                        "effective_radius": float(lines[51].strip()),
                        "inverse": lines[5].strip(),
                        "measurements": [lines[66].strip(),lines[67].strip(),lines[68].strip()],
                        "method": lines[108].strip(),
                        "maxiter": int(lines[112].strip()),
                        "start_points": int(lines[116].strip()),
                        "print_info": lines[120].strip(),
                        "options": {"reservoir": {"pressure": float(lines[133].strip()), 
                                                 "temperature": float(lines[129].strip()),
                                                 "robust": lines[137].strip()},
                                    "massflow": {"pressure": float(lines[147].strip()), 
                                                 "temperature": float(lines[143].strip()),
                                                 "robust": lines[151].strip()},
                                    "shocking": {"pressure": float(lines[161].strip()), 
                                                 "ratio": float(lines[157].strip()),
                                                 "robust": lines[165].strip()},
                                    "total":    {"pressure": float(lines[175].strip()), 
                                                 "temperature": float(lines[171].strip()),
                                                 "robust": lines[179].strip()}
                        }

    }

    return input_parameters

input_dict = reading_input()
mix = setup.setup_mpp()

if input_dict["inverse"] == 'True':
    output = inv.inverse(input_dict["measurements"],input_dict,mix)
    end_time=time.time()
    total_time = end_time-start_time

    check_forward = forw.forward(output,input_dict["residual"],input_dict["throat_area"],input_dict["effective_radius"],input_dict["surface_temperature"],input_dict["Prandtl"],input_dict["Lewis"],mix,input_dict["print_info"],input_dict["options"])

    width = [(40-len(input_dict["measurements"][i])) for i in range(3)]
    string_width = ["{"+":>"+str(width[i])+".4f}" for i in range(3)]

    print('...in inverse mode')
    print('------------------'+'\n')
    print('For these measurements...'+'\n')
    print(input_dict["measurements"][0]+string_width[0].format(input_dict["simulated_measurements"][input_dict["measurements"][0]]))
    print(input_dict["measurements"][1]+string_width[1].format(input_dict["simulated_measurements"][input_dict["measurements"][1]]))
    print(input_dict["measurements"][2]+string_width[2].format(input_dict["simulated_measurements"][input_dict["measurements"][2]]))
    print('------------------'+'\n')
    print('these free stream conditions...'+'\n')
    print('T1 [K]'+"{:>16.4f}".format(output[0]))
    print('P1 [Pa]'+"{:>15.4f}".format(output[1]))
    print('M1 [-]'+"{:>16.4f}".format(output[2]))
    print('------------------'+'\n')
    print('...reproduce these observations...'+'\n')
    print(input_dict["measurements"][0]+string_width[0].format(check_forward[input_dict['measurements'][0]]))
    print(input_dict["measurements"][1]+string_width[1].format(check_forward[input_dict['measurements'][1]]))
    print(input_dict["measurements"][2]+string_width[2].format(check_forward[input_dict['measurements'][2]]))
    print('------------------'+'\n')

    print('Execution time = '+"{:.4f}".format(total_time), ' seconds = '+"{:.4f}".format(total_time/60), ' minutes')

else:
    preshock_state = [input_dict["freestream"]["Temperature"],input_dict["freestream"]["Pressure"],input_dict["freestream"]["Mach"]]
    output = forw.forward(preshock_state,input_dict["residual"],input_dict["throat_area"],input_dict["effective_radius"],input_dict["surface_temperature"],input_dict["Prandtl"],input_dict["Lewis"],mix,input_dict["print_info"],input_dict["options"])
    end_time=time.time()
    total_time = end_time-start_time

    print('...in forward mode')
    print('------------------'+'\n')
    print('For these free stream conditions...'+'\n')
    print('T1 [K]'+"{:>16.4f}".format(preshock_state[0]))
    print('P1 [Pa]'+"{:>15.4f}".format(preshock_state[1]))
    print('M1 [-]'+"{:>16.4f}".format(preshock_state[2]))
    print('------------------')
    print('Measurements obtained...'+'\n')
    print('Heat flux [W/m^2]'+"{:>30.4f}".format(output["Heat_flux"]))
    print('Stagnation pressure [Pa]'+"{:>23.4f}".format(output["Stagnation_pressure"]))
    print('Reservoir pressure [Pa]'+"{:>24.4f}".format(output["Reservoir_pressure"]))
    print('Reservoir temperature [K]'+"{:>22.4f}".format(output["Reservoir_temperature"]))
    print('Total enthalpy [J/kg]'+"{:>26.4f}".format(output["Total_enthalpy"]))
    print('Stagnation density [kg/m^3]'+"{:>20.4f}".format(output["Stagnation_density"]))
    print('Free stream density [kg/m^3]'+"{:>19.4f}".format(output["Free_stream_density"]))
    print('Mass flow [kg/s]'+"{:>31.4f}".format(output["Mass_flow"]))
    print('Free stream velocity [m/s]'+"{:>21.4f}".format(output["Free_stream_velocity"]))
    print('------------------')

    print('Execution time = '+"{:.4f}".format(total_time), ' seconds = '+"{:.4f}".format(total_time/60), ' minutes')