"""
Get all TM1 transactions for all cubes starting to a specific date.
"""

import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from datetime import datetime

from TM1py.Services import TM1Service


with TM1Service(**config['tm1srv01']) as tm1:

    # Timestamp for Message-Log parsing
    timestamp = datetime(year=2018, month=2, day=15, hour=16, minute=2, second=0)

    # Get all entries since timestamp
    entries = tm1.server.get_transaction_log_entries(since=timestamp)

    # loop through entries
    for entry in entries:
        # Do stuff
        print(entry['TimeStamp'], entry)
