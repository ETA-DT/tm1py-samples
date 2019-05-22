"""
Reschedule all chores by -1 Hour.
Chores get deactivated implicitly before update (and activate after transaction is done)

"""
import configparser
config = configparser.ConfigParser()
config.read('..\config.ini')

from TM1py.Services import TM1Service

with TM1Service(**config['tm1srv01']) as tm1:
    # Get all chores. Loop through them and update them
    for chore in tm1.chores.get_all():
        chore.reschedule(hours=-1)
        tm1.chores.update(chore)





