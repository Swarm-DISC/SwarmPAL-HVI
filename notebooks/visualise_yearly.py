import datetime
import os
from glob import glob
import swarmpal
import swarmpal_hvi
import geopandas as gpd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from swarmpal_hvi.plot import plot
import swarmpal_hvi.data as hvi_data #import get_local_filename, get_file_list

dataproduct = '/SW_OPER_MAGB_LR_1B_spatial_binned'

# +
import datetime

resolution=2

def make_start_week(year):
    return hvi_data.get_swarm_week(datetime.datetime(year, 1, 1))
def make_end_week(year):
    return hvi_data.get_swarm_week(datetime.datetime(year, 12, 31))
                          
long_average_fname = hvi_data.get_local_filename(f"results/SW_OPER_MAGB_LR_1B__000__626__analysed__h3r={resolution}.nc")
year_average_fname = {
    year: hvi_data.get_local_filename(f"results/SW_OPER_MAGB_LR_1B__{make_start_week(year):03}__{make_end_week(year):03}__analysed__h3r={resolution}.nc")
    for year in range(2014, 2026)
}

long_average = xr.load_datatree(long_average_fname)
long_average = long_average[dataproduct].dataset


reference_average = xr.load_datatree(year_average_fname[2020])
reference_average = reference_average[dataproduct].dataset


for year, input_fname in year_average_fname.items():

    year_data = xr.load_datatree(input_fname)

    '''
    plot(year_data[dataproduct], columns=['B_NEC_std_C'],
         vmax=dict(B_NEC_std_C=1.0),
    )
    plt.title('$\\bar{\\sigma}_B$' + f'({year})')
    '''
    
    long_average, year_data = xr.align(
        long_average,
        year_data[dataproduct].dataset,
        join='outer',
        fill_value = 0.0,
    )

    ratio_data = year_data.copy()
    for variable in long_average.variables:
        #print(variable)
        if variable in {'h3_bin', 'NEC'}:
            continue
        ratio_data[variable] = year_data[variable] / long_average[variable]

    '''
    plot(ratio_data, columns=['B_NEC_std_C'],
         vmax=dict(B_NEC_std_C=1.7),
         vmin=dict(B_NEC_std_C=0.3),
         cmap='PiYG',
    )
    plt.title('$\\bar{\\sigma}_B$' + f'({year})/' + '$\\bar{\\sigma}_B$(2014-2025)')
    '''
    
    for variable in long_average.variables:
        #print(variable)
        if variable in {'h3_bin', 'NEC'}:
            continue
        ratio_data[variable] = year_data[variable] / reference_average[variable]

    plot(ratio_data, columns=['B_NEC_std'],
         vmax=dict(B_NEC_std=3.0),
         vmin=dict(B_NEC_std=-1.0),
         cmap='PiYG',
    )
    plt.title('$\\bar{\\sigma}_B$' + f'({year})/' + '$\\bar{\\sigma}_B$(2020)')
    
    


# -


