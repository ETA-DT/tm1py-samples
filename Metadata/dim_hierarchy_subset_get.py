"""
Get private and public Subsets from TM1
"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

dimension_name='Region'
hierarchy_name='Region'

with TM1Service(**config['tm1srv01']) as tm1:

    private_subsets = tm1.dimensions.subsets.get_all_names(dimension_name=dimension_name,
                                                           hierarchy_name=hierarchy_name,
                                                           private=True)
    print('private subsets: ')
    for subset_name in private_subsets:
        subset = tm1.dimensions.subsets.get(dimension_name=dimension_name,
                                            subset_name=subset_name,
                                            private=True)
        print(subset.name)

    public_subsets = tm1.dimensions.subsets.get_all_names(dimension_name=dimension_name,
                                                          hierarchy_name=hierarchy_name,
                                                          private=False)
    print('public subsets: ')
    for subset_name in public_subsets:
        subset = tm1.dimensions.subsets.get(dimension_name=dimension_name,
                                            subset_name=subset_name,
                                            private=False)
        print(subset.name)
