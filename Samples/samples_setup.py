"""
Create all cubes and dimensions thar are required for the Load Data Samples:
- fx rates to cube
- gdp to cube
- stock prices to cube


"""
import configparser
from datetime import timedelta, date, datetime
import os
import pandas as pd
from TM1py.Services import TM1Service

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
from TM1py.Objects import Cube, Dimension, Hierarchy, Element
from TM1py.Services import TM1Service

config = configparser.ConfigParser()
# storing the credentials in a file is not recommended for purposes other than testing.
# it's better to setup CAM with SSO or use keyring to store credentials in the windows credential manager. Sample:
# Samples/credentials_best_practice.py
config.read(r'..\config.ini')


# Time magic with python generator
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# push data to TM1
with TM1Service(**config['tm1srv02']) as tm1:
    # ============================
    # create TM1 objects for fx rates sample
    currencies = ('RMB', 'EUR', 'JPY', 'CHF', 'USD', 'AUD', 'TWD', 'HKD', 'GBP', 'SGD', 'INR')
    elements = [Element(cur, 'Numeric') for cur in currencies]

    # create dimension TM1py Currency From
    hierarchy = Hierarchy('TM1py Currency From', 'TM1py Currency From', elements)
    dimension = Dimension('TM1py Currency From', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Currency To
    hierarchy = Hierarchy('TM1py Currency To', 'TM1py Currency To', elements)
    dimension = Dimension('TM1py Currency To', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Date
    start_date = date(1990, 1, 1)
    end_date = date(2041, 1, 1)
    elements = [Element(str(single_date), 'Numeric') for single_date in daterange(start_date, end_date)]
    hierarchy = Hierarchy('TM1py Date', 'TM1py Date', elements)
    dimension = Dimension('TM1py Date', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Month
    elements = [Element(str(month), 'Numeric') for month in range(1, 13)]
    hierarchy = Hierarchy('TM1py Month', 'TM1py Month', elements)
    dimension = Dimension('TM1py Month', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Year
    elements = [Element(str(year), 'Numeric') for year in range(1990, 2041, 1)]
    hierarchy = Hierarchy('TM1py Year', 'TM1py Year', elements)
    dimension = Dimension('TM1py Year', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py FX Rates Measure
    elements = [Element('Spot', 'Numeric'), Element('EOP', 'Numeric'),
                Element('AVG', 'Numeric'), Element('Month Close', 'Numeric')]
    hierarchy = Hierarchy('TM1py FX Rates Measure', 'TM1py FX Rates Measure', elements)
    dimension = Dimension('TM1py FX Rates Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create cube TM1py FX Rates
    cube = Cube('TM1py FX Rates', ['TM1py Currency From', 'TM1py Currency To', 'TM1py Date', 'TM1py FX Rates Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)

    # create cube TM1py FX Rates Monthly
    cube = Cube('TM1py FX Rates Monthly', ['TM1py Currency From', 'TM1py Currency To', 'TM1py Year', 'TM1py Month',
                                           'TM1py FX Rates Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)

    # ============================
    # create TM1 objects for gdp sample

    # create dimension TM1py Country
    countries = ('USA', 'AUS', 'DEU')
    elements = [Element(country, 'Numeric') for country in countries]
    hierarchy = Hierarchy('TM1py Country', 'TM1py Country', elements)
    dimension = Dimension('TM1py Country', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Quarter
    elements = [Element('Q' + str(q), 'Numeric') for q in range(1, 5, 1)]
    hierarchy = Hierarchy('TM1py Quarter', 'TM1py Quarter', elements)
    dimension = Dimension('TM1py Quarter', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Econ Measure
    elements = [Element('GDP', 'Numeric')]
    hierarchy = Hierarchy('TM1py Econ Measure', 'TM1py Econ Measure', elements)
    dimension = Dimension('TM1py Econ Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create cube TM1py Econ
    cube = Cube('TM1py Econ', ['TM1py Country', 'Years_et', 'TM1py Quarter', 'TM1py Econ Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)

    # ============================
    # create TM1 objects for stock sample

    # create dimension TM1py Financial Instrument
    instruments = ('IBM', 'AAPL', 'GOOG')
    elements = [Element(instrument, 'Numeric') for instrument in instruments]
    hierarchy = Hierarchy('TM1py Financial Instrument', 'TM1py Financial Instrument', elements)
    dimension = Dimension('TM1py Financial Instrument', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create dimension TM1py Stock Prices Measure
    measures = ('Open', 'High', 'Low', 'Close', 'Volume', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close',
                'Adj. Volume')
    elements = [Element(measure, 'Numeric') for measure in measures]
    hierarchy = Hierarchy('TM1py Stock Prices Measure', 'TM1py Stock Prices Measure', elements)
    dimension = Dimension('TM1py Stock Prices Measure', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)

    # create cube TM1py Stock Prices
    cube = Cube('TM1py Stock Prices', ['TM1py Financial Instrument', 'Years_et', 'TM1py Stock Prices Measure'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)

    # ============================
    # create TM1 objects for External_macro

    # create dimension External_measures
    elements = []
    europe_series_codes = [
    "LRHUTTTTEZM156S",  # Harmonized Unemployment Rate: Total: All Persons for the Euro Area
    "XTEXVA01EZM667S",  # Exports of Goods: Total for the Euro Area
    "XTIMVA01EZM667S",  # Imports of Goods: Total for the Euro Area
    "IRLTLT01EZM156N"  # Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the Euro Area
    ]
    for code in europe_series_codes:
        elements.append(Element(code, 'Numeric'))
    
    hierarchy = Hierarchy('External_measures', 'External_measures', elements)
    dimension = Dimension('External_measures', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)
    
    # create cube External_macro
    cube = Cube('External_macro', ['Region_et', 'Years_et', 'External_measures'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)


    # ============================
    # create TM1 objects for External_macro_monthly

    # create dimension Mon-Ye
    elements = []
    start = datetime(year=1991,month=1,day=1)
    end = datetime(year=2019,month=12,day=31)
    datelist = pd.date_range(start,end,freq='ME').tolist()
    datelist = list(map(lambda x : x.strftime("%b-%y"),datelist))
    datelist

    for month in datelist:
        elements.append(Element(month, 'Numeric'))
    
    hierarchy = Hierarchy('Month_year', 'Month_year', elements)
    dimension = Dimension('Month_year', [hierarchy])
    if not tm1.dimensions.exists(dimension.name):
        tm1.dimensions.create(dimension)
    
    # create cube External_macro_monthly
    cube = Cube('External_macro_monthly', ['Region_et', 'Month_year', 'External_measures'])
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)
    