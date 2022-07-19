import numpy as np
import inverse as inv
import forward as forw
import rebuilding_setup as setup
 
## function that populates a dictionary with the inputs ##

def reading_input():
    with open('../input.in', 'r') as f:
        lines = f.readlines()

    input_parameters = {"freestream":{"Temperature": float(lines[27].strip()), "Pressure": float(lines[31].strip()), "Mach": float(lines[35].strip())},
                        "simulated_measurements": {"Heat_flux": float(lines[72].strip()),"Stagnation_pressure": float(lines[76].strip()), "Reservoir_pressure": float(lines[80].strip()), "Reservoir_temperature": float(lines[84].strip()), "Total_enthalpy": float(lines[88].strip()), "Stagnation_density": float(lines[92].strip()), "Free_stream_density": float(lines[96].strip()), "Mass_flow": float(lines[100].strip()), "Free_stream_velocity": float(lines[104].strip())},
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
                        "print_info": lines[120].strip()

    }

    return input_parameters

input_dict = reading_input()
mix = setup.setup_mpp()

if input_dict["inverse"] == 'True':
    output = inv.inverse(input_dict["measurements"],input_dict,mix)
    print('...in inverse mode')
    print('------------------'+'\n')
    print('For these measurements...'+'\n')
    print(input_dict["measurements"][0]+'                  '+ str(input_dict["simulated_measurements"][input_dict["measurements"][0]]))
    print(input_dict["measurements"][1]+'                  '+ str(input_dict["simulated_measurements"][input_dict["measurements"][1]]))
    print(input_dict["measurements"][2]+'                  '+ str(input_dict["simulated_measurements"][input_dict["measurements"][2]]))
    print('------------------'+'\n')
    print('these free stream conditions...'+'\n')
    print('T1 [K]'+'   '+ str(output[0]))
    print('P1 [Pa]'+'   '+str(output[1]))
    print('M1 [-]'+'       '+str(output[2]))
    print('------------------')

else:
    preshock_state = [input_dict["freestream"]["Temperature"],input_dict["freestream"]["Pressure"],input_dict["freestream"]["Mach"]]
    output = forw.forward(preshock_state,input_dict["residual"],input_dict["throat_area"],input_dict["effective_radius"],input_dict["surface_temperature"],input_dict["Prandtl"],input_dict["Lewis"],mix,input_dict["print_info"])
    print('...in forward mode')
    print('------------------'+'\n')
    print('For these free stream conditions...'+'\n')
    print('T1 [K]'+'   '+ str(preshock_state[0]))
    print('P1 [Pa]'+'   '+str(preshock_state[1]))
    print('M1 [-]'+'       '+str(preshock_state[2]))
    print('------------------')
    print('Measurements obtained...'+'\n')
    print('Heat flux [W/m^2]'+'                  '+ str(output["Heat_flux"]))
    print('Stagnation pressure [Pa]'+'          '+ str(output["Stagnation_pressure"]))
    print('Reservoir pressure [Pa]'+'           '+ str(output["Reservoir_pressure"]))
    print('Reservoir temperature [K]'+'           '+ str(output["Reservoir_temperature"]))
    print('Total enthalpy [J/kg]'+'              '+ str(output["Total_enthalpy"]))
    print('Stagnation density [kg/m^3]'+'     '+ str(output["Stagnation_density"]))
    print('Free stream density [kg/m^3]'+'   '+ str(output["Free_stream_density"]))
    print('Mass flow [kg/s]'+'                   '+ str(output["Mass_flow"]))
    print('Free stream velocity [m/s]'+'        '+ str(output["Free_stream_velocity"]))
    print('------------------')