""" 
Get a Process from TM1. Update it. Push it back to TM1.
"""
import configparser
import os
from TM1py.Services import TM1Service
from operator import itemgetter

def set_current_directory():
    abspath = os.path.abspath(__file__)         # file absolute path
    directory = os.path.dirname(abspath)        # current file parent directory
    os.chdir(directory)
    return directory

CURRENT_DIRECTORY = set_current_directory()
config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')

# connection to TM1 Server
tm1_master = TM1Service(**config['tm1srv01'])
tm1_other = TM1Service(**config['tm1srv02'])

# read process
p_master = tm1_master.processes.get('TM1py process')
p_other = tm1_other.processes.get('TM1py process')


# get the sections to update

sections_to_update = []
sections = ['Prolog', 'Metadata', 'Data', 'Epilog']
for section in sections:
    new_input = input(f'Do you want to synchronize the "{section}" section ? (Y/N)').lower()
    if new_input == 'y':
        sections_to_update.append(section)
change_param = input('Do you want to synchronize parameters ? (Y/N) ')
change_var = input('Do you want to synchronize variables ? (Y/N) ')


if 'Prolog' in sections_to_update:
    p_other.prolog_procedure = p_master.prolog_procedure
if 'Metadata' in sections_to_update:
    p_other.metadata_procedure = p_master.metadata_procedure
if 'Data' in sections_to_update:
    p_other.data_procedure = p_master.data_procedure
if 'Epilog' in sections_to_update:
    p_other.epilog_procedure = p_master.epilog_procedure

if change_param.lower() == 'y':
    p_master_parameters_names = [p_master.parameters[k]['Name'] for k in range(len(p_master.parameters))]
    p_other_parameters_names =  [p_other.parameters[k]['Name'] for k in range(len(p_other.parameters))]


    if set(p_other_parameters_names) != set(p_master_parameters_names):                                     # si p_other possède des paramètres en trop, les retirer
        parameter_names_to_remove = set(p_other_parameters_names) - set(p_master_parameters_names)
        for parameter_name_to_remove in parameter_names_to_remove:
            p_other.remove_parameter(parameter_name_to_remove)
    
    p_other_parameters_names =  [p_other.parameters[k]['Name'] for k in range(len(p_other.parameters))]

    name_intersection = set(p_master_parameters_names).intersection(set(p_other_parameters_names))      # si un paramètre existe dans p_other mais valeurs différentes, le retirer (pour l'ajouter après)
    for name in name_intersection:
        p_master_param = p_master.parameters[p_master_parameters_names.index(name)]
        p_other_param = p_other.parameters[p_other_parameters_names.index(name)]
        print(p_master_param)
        print(p_other_param)
        if p_master_param != p_other_param:
            p_other.remove_parameter(name)
    p_other_parameters_names =  [p_other.parameters[k]['Name'] for k in range(len(p_other.parameters))]
    
    tm1_other.processes.update(p_other)

    parameter_names_to_add = set(p_master_parameters_names) - set(p_other_parameters_names)
    for parameter_name_to_add in parameter_names_to_add:
        parameter_to_add = p_master.parameters[p_master_parameters_names.index(parameter_name_to_add)]
        p_other.add_parameter(name=parameter_to_add['Name'],
                                prompt=parameter_to_add['Prompt'],
                                value=parameter_to_add['Value'],
                                parameter_type=parameter_to_add['Type'])
        
if change_var.lower() == 'y':
    p_master_variables_names = [p_master.variables[k]['Name'] for k in range(len(p_master.variables))]
    p_other_variables_names =  [p_other.variables[k]['Name'] for k in range(len(p_other.variables))]


    if set(p_other_variables_names) != set(p_master_variables_names):                                     # si p_other possède des varètres en trop, les retirer
        variable_names_to_remove = set(p_other_variables_names) - set(p_master_variables_names)
        for variable_name_to_remove in variable_names_to_remove:
            p_other.remove_variable(variable_name_to_remove)
        p_other_variables_names =  [p_other.variables[k]['Name'] for k in range(len(p_other.variables))]

    name_intersection = set(p_master_variables_names).intersection(set(p_other_variables_names))      # si un varètre existe dans p_other mais valeurs différentes, le retirer (pour l'ajouter après)
    for name in name_intersection:
        p_master_var = p_master.variables[p_master_variables_names.index(name)]
        p_other_var = p_other.variables[p_other_variables_names.index(name)]
        if p_master_var != p_other_var:
            p_other.remove_variable(name)

    p_other_variables_names =  [p_other.variables[k]['Name'] for k in range(len(p_other.variables))]
    tm1_other.processes.update(p_other)

    variable_names_to_add = set(p_master_variables_names) - set(p_other_variables_names)
    for variable_name_to_add in variable_names_to_add:
        variable_to_add = p_master.variables[p_master_variables_names.index(variable_name_to_add)]
        p_other.add_variable(name=variable_to_add['Name'],
                            variable_type=variable_to_add['Type'])

tm1_other.processes.update(p_other)
