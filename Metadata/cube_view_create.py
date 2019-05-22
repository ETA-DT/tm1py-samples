""" 
Create a classic TM1 cube view

Assumptions: all referenced subsets exist in TM1 Server. 
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Objects import NativeView
from TM1py.Services import TM1Service

# establish connection to TM1 Server
with TM1Service(**config['tm1srv01']) as tm1:

    native_view = NativeView(cube_name='Plan_BudgetPlan',
                             view_name='TM1py View3')

    # set up native view - put subsets on Rows, Columns and Titles
    subset = tm1.dimensions.subsets.get(dimension_name='plan_version',
                                        subset_name='FY 2004 Budget',
                                        private=False)
    native_view.add_row(dimension_name='plan_version', subset=subset)

    subset = tm1.dimensions.subsets.get(dimension_name='plan_business_unit',
                                        subset_name='n level business unit',
                                        private=False)
    native_view.add_row(dimension_name='plan_business_unit', subset=subset)

    subset = tm1.dimensions.subsets.get(dimension_name='plan_department',
                                        subset_name='n level departments',
                                        private=False)
    native_view.add_row(dimension_name='plan_department', subset=subset)

    subset = tm1.dimensions.subsets.get(dimension_name='plan_chart_of_accounts',
                                        subset_name='Consolidations',
                                        private=False)
    native_view.add_row(dimension_name='plan_chart_of_accounts', subset=subset)

    subset = tm1.dimensions.subsets.get(dimension_name='plan_exchange_rates',
                                        subset_name='local',
                                        private=False)
    native_view.add_title(dimension_name='plan_exchange_rates', subset=subset, selection='local')

    subset = tm1.dimensions.subsets.get(dimension_name='plan_time',
                                        subset_name='2004 Total Year',
                                        private=False)
    native_view.add_column(dimension_name='plan_time', subset=subset)

    subset = tm1.dimensions.subsets.get(dimension_name='plan_source',
                                        subset_name='budget',
                                        private=False)
    native_view.add_column(dimension_name='plan_source', subset=subset)

    # create native view on Server
    tm1.cubes.views.create(view=native_view, private=False)
