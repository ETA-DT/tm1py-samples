"""
Read FX data from FRED (Federal Reserve of St. Louis data) through pandas and push it to the fx cube
Prerequisites:
1. Create the required cubes and dimensions
    Run TM1py sample Load Data\samples setup.py
2. Install pandas
    type 'pip install pandas' into cmd if you don't have pandas installed
3. Add pandas_reader module:
    To install it, run in command line: pip install pandas_datareader
"""
import collections
import configparser

from datetime import datetime

# type 'pip install pandas_datareader' into cmd if you don't have pandas_datareader installed
import pandas_datareader.data as web
from TM1py.Services import TM1Service
import os

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

cube_name = 'External_macro_monthly'
europe_series_codes = [
    "LRHUTTTTEZM156S",  # Harmonized Unemployment Rate: Total: All Persons for the Euro Area
    "XTEXVA01EZM667S",  # Exports of Goods: Total for the Euro Area
    "XTIMVA01EZM667S",  # Imports of Goods: Total for the Euro Area
    "IRLTLT01EZM156N"  # Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the Euro Area
    ]

start = datetime(year=1991,month=1,day=1)
end = datetime(year=2019,month=12,day=31)
external_factors = web.DataReader(europe_series_codes,'fred',start,end)
external_factors_monthly = external_factors.copy()
external_factors_monthly.index = external_factors_monthly.index.map(lambda x : x.strftime("%b-%y"))
external_factors_monthly

for series_code in europe_series_codes:
    # Create cellset and push it to External_measures_yearly Cube
    cellset = collections.OrderedDict()
    for month in list(external_factors_monthly.index):
        coordinates = ("Europe",month, series_code)
        cellset[coordinates] = float(external_factors_monthly.loc[month][series_code])

    with TM1Service(**config['tm1srv03']) as tm1:
        tm1.cubes.cells.write_values(cube_name, cellset)
