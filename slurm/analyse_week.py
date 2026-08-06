# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "netcdf4>=1.7.4",
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
import xarray as xr

#from swarmpal.io._paldata import PalDataItem, create_paldata
from swarmpal import fetch_data

from swarmpal_hvi.spatial_h3_binning import SpatialH3Binning
from swarmpal_hvi.temporal_binning import TemporalBinning

def analyse(args):
    output_filename = f"data/2016_{args.week:03}_analysed.nc"

    if os.path.exists(output_filename):
        print(f"File exists: {output_filename}")
        return

    dataproduct = 'SW_OPER_MAGB_LR_1B'
    print(args)
    config = dict(data_params=[dict(
        provider='file',
        filename=f"data/2016_{args.week:03}.nc",
        filetype='netcdf',
        dataset=dataproduct,
    )])
    #ds = create_paldata(**{
    #    dataproduct: PalDataItem.from_file(f"data/2016_{args.week:02}.nc")
    #})
    ds = fetch_data(config)
    dataproduct = '/' + dataproduct

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

    spatial_binning = SpatialH3Binning(dict(
        dataset=dataproduct + "_time_binned",
        resolution=3,
        output_dataset=dataproduct + "_spatial_binned",
        input_variables=["F", "magnetic_residual"]
    ))
    ds = spatial_binning(ds)

    results = xr.DataTree()
    results[dataproduct + "_spatial_binned"] = ds[dataproduct + "_spatial_binned"]
    results.to_netcdf(output_filename)

def main():
    parser = argparse.ArgumentParser(
            prog="analyse.py",
            description="Perfrom the HVI analysis on a week's data."
    )
    parser.add_argument("-w", "--week", type=int, help="The week to analyse")
    args = parser.parse_args()
    analyse(args)

if __name__ == "__main__":
    main()
