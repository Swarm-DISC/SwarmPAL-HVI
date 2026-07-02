import datetime
import os
from glob import glob
import swarmpal
import swarmpal_hvi
import geopandas as gpd
import xarray as xr


# +
a_week = datetime.timedelta(days=7)
year = 2016

def make_config(start_time):
    '''Makes a SwarmPAL config object for downloading VirES data'''
    return dict(data_params=[dict(
        provider='vires',
        collection='SW_OPER_MAGB_LR_1B',
        measurements=['F', 'B_NEC', 'Flags_F', 'Flags_B', 'Flags_q', 'Flags_Platform'],
        models=["Model = 'CHAOS'"],
        start_time=start_time.isoformat(),
        end_time=(start_time + a_week).isoformat(),
        server_url='https://vires.services/ows',
    )])

# Download 4 weeks of data if the files are not present already
start_time = datetime.datetime(year, 1, 1)
for week in range(1, 2):
    filename = f'data_{year}_{week:02}.nc'
    if os.path.exists(filename):
        continue
        
    config = make_config(start_time)
    data = swarmpal.fetch_data(config)
    data.to_netcdf(filename)
    start_time += a_week

# +
# Collate the downloaded data into a single xarray DataTree object
data_files = glob('data*.nc')
data_files.sort(reverse=True) # Sort in reverse, because list.pop takes items from the back.
print(data_files)

dataproduct = '/SW_OPER_MAGB_LR_1B'

ds = xr.load_datatree(data_files.pop())
while len(data_files) > 0:
    ds2 = xr.load_datatree(data_files.pop())
    ds[dataproduct] = xr.concat([ds[dataproduct].to_dataset(), ds2[dataproduct].to_dataset()], dim='Timestamp')
ds[dataproduct]

# +
from swarmpal_hvi.temporal_binning import TemporalBinning

ds[dataproduct]["magnetic_residual"] = ds[dataproduct].swarmpal.magnetic_residual()

temporal_binning = TemporalBinning(config=dict(
    dataset=dataproduct,
    input_variables=[
        "F",
        "magnetic_residual"
    ],
    N_readings=20,
    output_dataset=dataproduct + "_time_binned"
))
print(temporal_binning.config)
ds = temporal_binning(ds)
ds

# +
from swarmpal_hvi.spatial_h3_binning import SpatialH3Binning

spatial_binning = SpatialH3Binning(dict(
    dataset=dataproduct + "_time_binned",
    resolution=3,
    output_dataset=dataproduct + "_spatial_binned",
    input_variables=["F", "magnetic_residual"]
))
ds = spatial_binning(ds)
ds

# +
from swarmpal_hvi.plot import plot

plot(ds[dataproduct + '_spatial_binned'])
# -


