"""
Read IBM Stock data from Wiki through quandl and push it to the Stock data cube

Run sample setup.py before running this script, to create the required cubes and dimensions!

Prerequisites:
1. Create the required cubes and dimensions
    Run TM1py sample Load Data\setup.py
2. Install quandl
    type 'pip install quandl' into cmd if you don't have quandl installed
"""
import configparser

# type 'pip install quandl' into cmd if you don't have quandl installed
import quandl
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
with TM1Service(**config['tm1srv02']) as tm1:
    financial_instrument_elems = tm1.elements.get_element_names('TM1py Financial Instrument','TM1py Financial Instrument')

for instru in financial_instrument_elems:
    # load Stock data for IBM
    data = quandl.get("WIKI/"+instru, start_date='1991-01-01', end_date='2013-31-12')
    data['Year'] = [str(full_date)[:4] for full_date in list(data.index)]
    data = data.groupby('Year').mean()

    # create cellset from raw data
    cube = 'TM1py Stock Prices'
    measures = ('Open', 'High', 'Low', 'Close', 'Volume', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume')
    cellset = {}
    for tmstp, row in data.iterrows():
        for measure in measures:
            cellset[(instru, str(tmstp), measure)] = row[measure]

    # push data to TM1
    with TM1Service(**config['tm1srv02']) as tm1:
        tm1.cubes.cells.write_values(cube, cellset)
