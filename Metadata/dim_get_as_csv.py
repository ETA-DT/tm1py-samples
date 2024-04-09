"""
Get a random dimension from the TM1 model and print out its details
"""
import configparser
import random
import os
import csv
from TM1py.Services import TM1Service

def set_current_directory():
    abspath = os.path.abspath(__file__)         # file absolute path
    directory = os.path.dirname(abspath)        # current file parent directory
    os.chdir(directory)
    return directory

CURRENT_DIRECTORY = set_current_directory()

config = configparser.ConfigParser()
config.read(r'..\config.ini')

dimension_name = input('Enter dimension name: ')

# Connection to TM1. Needs Address, Port, Credentials, and SSL
with TM1Service(**config['tm1srv01']) as tm1:
    try:
        dimension = tm1.dimensions.get(dimension_name)
    except:
        raise SystemExit(f'No dimension named {dimension_name}')

    with open(f'../Outputs/{dimension_name}_info.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # iterate through hierarchies
        for hierarchy in dimension:
            writer.writerow(['Hierarchy Name: {}'.format(hierarchy.name)])
            print('Hierarchy Name: {}'.format(hierarchy.name))
            for parent, child in hierarchy.edges:
                writer.writerow([child, parent])
            print(hierarchy.edges)
            list_edges = [(val2,val1) for (val1,val2) in hierarchy.edges]
            par = [val[0] for val in hierarchy.edges]
            chi = [val[1] for val in hierarchy.edges]
            writer.writerow(list_edges)
            for couple in list_edges:
                if couple[0] in par:
                    print(couple[1])
            mdx = "SELECT " \
                "NON EMPTY {TM1SUBSETALL( ["+dimension_name+"] )} on ROWS, " \
                "NON EMPTY {TM1SUBSETALL( [}ElementAttributes_"+dimension_name+"] )} ON COLUMNS " \
                "FROM [}ClientGroups]"
            cube_content = tm1.cubes.cells.execute_mdx(mdx, ['Value'])
            print(cube_content)


            break
            

            # # iterate through Elements in hierarchy
            # for element in hierarchy:
            #     writer.writerow(['Element Name: {} Index: {} Type: {}'.format(element.name, str(element.index), element.element_type)])
            #     print(['Element Name: {} Index: {} Type: {}'.format(element.name, str(element.index), element.element_type)])

            # # iterate through Subsets
            # for subset in hierarchy.subsets:
            #     writer.writerow(['Subset Name: {}'.format(subset)])
            #     print('Subset Name: {}'.format(subset))

            # # iterate through Edges
            # for parent, child in hierarchy.edges:
            #     writer.writerow(["Parent Name: {}, Component Name: {}".format(parent, child)])
            #     parent_child = {}
            #     print("Parent Name: {}, Component Name: {}".format(parent, child))
            
            # # print the default member
            # writer.writerow(['Default Member: {}'.format(hierarchy.default_member)])
            # print('Default Member: {}'.format(hierarchy.default_member))

        #     start = 0
        #     current_level = start
        #     current_type = 'Consolidated'
        #     previous_type = current_type[:]
        #     # iterate through Elements in hierarchy
        #     for element in hierarchy:
        #         current_type = element.element_type
        #         if str(previous_type) == 'Consolidated':
        #             current_level += 1
        #         else:
        #             if str(current_type) == 'Consolidated':
        #                 current_level -= 1
        #         level_string = '--'*current_level
        #         previous_type = current_type
        #         writer.writerow([level_string + element.name])

        # all_cubes = tm1.cubes.get_all()
        # cube_with_dimension = []
        # for cube in all_cubes:
        #     if dimension_name in cube.dimensions:
        #         print(cube.name)
        #         cube_with_dimension.append(cube.name)
        
        # writer.writerow([])
        # writer.writerow([f'Cubes containing {dimension_name} dimension'])
        # for cube_name in cube_with_dimension:
        #     writer.writerow([cube_name])
        # writer.writerow([f'Cubes containing {dimension_name} dimension: {tm1.cubes.search_for_dimension(dimension_name)}'])
