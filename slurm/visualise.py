import datetime
import os
from glob import glob
import swarmpal
import swarmpal_hvi
import geopandas as gpd
import xarray as xr
import numpy as np

from swarmpal_hvi.plot import plot

dataproduct = '/SW_OPER_MAGB_LR_1B_spatial_binned'

# +
#ds = xr.load_datatree('data/aggregated.nc')

files = glob('data/*__analysed.nc')

for file in files:
    ds = xr.load_datatree(file)
    print(file)
    for name, child_node in ds.children.items():
        print(name)
        plot(child_node, columns=['B_NEC_std_C'], vmax=dict(B_NEC_std_C=1.0))
# +
from swarm import get_swarm_week
import datetime

resolution=3

def make_start_week(year):
    return get_swarm_week(datetime.datetime(year, 1, 1))
def make_end_week(year):
    return get_swarm_week(datetime.datetime(year, 12, 31))
                          
long_average_fname = f"data/SW_OPER_MAGB_LR_1B__000__626__analysed__h3r={resolution}.nc"
year_average_fname = {
    year: f"data/SW_OPER_MAGB_LR_1B__{make_start_week(year):03}__{make_end_week(year):03}__analysed__h3r={resolution}.nc"
    for year in range(2014, 2026)
}

long_average = xr.load_datatree(long_average_fname)
long_average = long_average[dataproduct].dataset

for year, input_fname in year_average_fname.items():
    print(year, input_fname)

    year_data = xr.load_datatree(input_fname)

    plot(year_data[dataproduct], columns=['B_NEC_std_C'],
         vmax=dict(B_NEC_std_C=1.0),
    )
    
    long_average, year_data = xr.align(
        long_average,
        year_data[dataproduct].dataset,
        join='outer',
        fill_value = 0.0,
    )

    for variable in long_average.variables:
        #print(variable)
        if variable in {'h3_bin', 'NEC'}:
            continue
        year_data[variable] = year_data[variable] / long_average[variable]

    
    plot(year_data, columns=['B_NEC_std_C'],
         vmax=dict(B_NEC_std_C=1.7),
         vmin=dict(B_NEC_std_C=0.3),
         cmap='PiYG',
    )


# -

year_data


