"""
Query data through MDX

"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service


with TM1Service(**config['tm1srv01']) as tm1:
    # Define mdx query
    mdx = "SELECT " \
          "NON EMPTY {TM1SUBSETALL( [}Clients] )} on ROWS, " \
          "NON EMPTY {TM1SUBSETALL( [}Groups] )} ON COLUMNS " \
          "FROM [}ClientGroups]"

    # Get view content
    content = tm1.cubes.cells.execute_mdx(mdx)

    # Print content
    print(dict(content))



