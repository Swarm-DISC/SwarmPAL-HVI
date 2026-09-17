import datetime
import math

import pooch

swarm_start_year = 2014
swarm_start_time = datetime.datetime(swarm_start_year, 1, 1)
a_week = datetime.timedelta(days=7)

SWARMPAL_HVI_DATA_VERSION = "v0.0.1+dev"

POOCH = pooch.create(
    # Download location. Defaults to ~/.cache/swarmpal_hvi_data on Linux.
    path=pooch.os_cache("swarmpal_hvi_data"),
    base_url="https://raw.githubusercontent.com/Swarm-DISC/SwarmPal-HVI-data/{version}",
    version=SWARMPAL_HVI_DATA_VERSION,
    version_dev="main",
    registry={
        "registry.txt": "md5:3bd63ac6938801d4a1e1ae3ff2c08b7f",
    },
)

# git-lfs files are not 'in' the git repository, but can be downloaded from slightly different URL.
# See: https://stackoverflow.com/questions/45117476/access-download-on-git-lfs-file-via-raw-githubusercontent-com
POOCH_LFS = pooch.create(
    path=pooch.os_cache("swarmpal_hvi_data"),
    base_url="https://media.githubusercontent.com/media/Swarm-DISC/SwarmPal-HVI-data/{version}",
    version=SWARMPAL_HVI_DATA_VERSION,
    version_dev="main",
    registry=None,
)
POOCH_LFS.load_registry(POOCH.fetch("registry.txt"))


def get_local_filename(filename):
    """Returns the absolute path to a filename in the test set."""
    return POOCH_LFS.fetch(filename)

def get_file_list():
    return sorted(list(POOCH_LFS.registry.keys()))

def make_dataset_filename(collection, week_no, *args, **kwargs):
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


