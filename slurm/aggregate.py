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

import os
import argparse 
from glob import glob

import xarray as xr

def make_config(dataproduct, filename):
    return dict(data_params=[dict(
        provider='file',
        filename=filename,
        filetype='netcdf',
        dataset=dataproduct,
    )])

def main(args):
    print(args)
    files = glob(f"data/*analysed.nc")
    print(files)
    if len(files) == 0:
        print("No data files to aggregate")
        return

    dataproduct = 'SW_OPER_MAGB_LR_1B_spatial_binned'
    n_datafiles = len(files)

    result = xr.load_datatree(files.pop()) #fetch_data(make_config(dataproduct, files.pop()))
    while len(files) > 0:
        ds = xr.load_datatree(files.pop()) #fetch_data(make_config(dataproduct, files.pop()))
        result += ds

    for variable in result.variables:
        result[variable] /= n_datafiles

    result.to_netcdf("data/aggregated.nc")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="aggregrate.py",
            description="Merge the HVI results from several time periods"
    )
    #parser.add_argument("-n", "--num-weeks", type=int, help="The number weeks to aggergate")
    args = parser.parse_args()
    main(args)
