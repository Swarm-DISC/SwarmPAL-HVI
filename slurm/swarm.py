# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "swarmpal>=0.3.0",
#     "swarmpal-hvi",
#     "xarray>=2026.4.0",
# ]
#
# [tool.uv.sources]
# swarmpal-hvi = { path = "../" }
# ///

import datetime
import math


swarm_start_year = 2014
swarm_start_time = datetime.datetime(swarm_start_year, 1, 1)
a_week = datetime.timedelta(days=7)

def make_filename(collection, week_no, *args, **kwargs):
    args_part = ("__" + "__".join(map(str,args))
        if len(args) > 0
        else ""
    )

    kwargs_part = ("__" + "__".join([f'{k}={v}' for k, v in kwargs.items()])
        if len(kwargs) > 0
        else ""
    )

    return f"data/{collection}__{week_no:03}{args_part}{kwargs_part}.nc"

def get_swarm_week(date):
    '''Returns the number of weeks after the start of Swarm data capture'''
    return math.floor((date - swarm_start_time ).days / 7)

def get_swarm_week_start_date(week_no):
    return swarm_start_time + week_no * a_week

def make_filename_containing(collection, date, *args, **kwargs):
    week_no = get_swarm_week(date)
    return make_filename(collection, week_no, *args, **kwargs)

def add_common_args(parser):
    '''Add arguments to argpars.ArgumentParser objects that
    should be consistent between scripts.'''

    parser.add_argument("-c", "--collection", default="SW_OPER_MAGB_LR_1B", help="The Swarm data product to download")
    parser.add_argument(
        "-S", "--start-date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        help="Start date of the period to aggrate [YYYY-MM-DD]",
    )
    parser.add_argument(
        "-E", "--end-date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        help="End date of the period to aggrate [YYYY-MM-DD]",
    )


### TESTS

import unittest

class TestGetSwarmWeek(unittest.TestCase):

    #def test_test(self):
    #    self.assertTrue(True)

    def test_no_overlaps(self):
        pass



if __name__ == "__main__":
    unittest.main()
