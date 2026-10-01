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

from datetime import datetime
from pathlib import Path

from swarmpal import fetch_data

from swarmpal_hvi.spatial_h3_binning import SpatialH3Binning
from swarmpal_hvi.temporal_binning import TemporalBinning
import swarmpal_hvi.data as hvi_data

import swarm

def analyse(args):

    data_dir = Path('data')
    results_dir = Path('SwarmPAL-HVI-data/results')

    start_week = hvi_data.get_swarm_week(args.start_date)
    end_week = hvi_data.get_swarm_week(args.end_date)

    output_filename = results_dir / hvi_data.make_dataset_filename(args.collection, start_week, f"{end_week:03}", 'analysed', f'h3r={args.resolution}')
    
    if os.path.exists(output_filename):
        print(f"File exists: {output_filename}")
        return

    input_dataproduct = '/' + args.collection + '_time_binned'
    output_dataproduct = '/' + args.collection + '_spatial_binned'
    input_filename = data_dir / hvi_data.make_dataset_filename(args.collection, start_week, 'time_binned')
    ds = xr.load_datatree(str(input_filename))
    for week in range(start_week+1, end_week+1):
        input_filename = data_dir / hvi_data.make_dataset_filename(args.collection, week, 'time_binned')
        if not os.path.exists(input_filename):
            print(f"File {input_filename} does not exists")
            continue
        tmp = xr.load_datatree(str(input_filename))
        if ds[input_dataproduct]["Timestamp"].size == 0:
            print('No data')
            continue
        print(input_filename, ':', tmp[input_dataproduct]["Timestamp"][0].dt.strftime("%Y-%m-%d").item(), '-', tmp[input_dataproduct]["Timestamp"][-1].dt.strftime("%Y-%m-%d").item(), '\n')
        ds[input_dataproduct] = xr.concat([ds[input_dataproduct].to_dataset(), tmp[input_dataproduct].to_dataset()], dim='Timestamp')

    '''
    ds[dataproduct]["sigma_B_NEC"] = ds[dataproduct].swarmpal.magnetic_residual()

    temporal_binning = TemporalBinning(config=dict(
        dataset=dataproduct,
        input_variables=[
            "F",
            "sigma_B_NEC"
        ],
        N_readings=20,
        output_dataset=dataproduct + "_time_binned"
    ))
    print(temporal_binning.config)
    ds = temporal_binning(ds)
    '''

    spatial_binning = SpatialH3Binning(dict(
        dataset=input_dataproduct, # + "_time_binned",
        resolution=args.resolution,
        output_dataset=output_dataproduct, # + "_spatial_binned",
        input_variables=["F", "sigma_B_NEC"]
    ))
    ds = spatial_binning(ds)

    results = xr.DataTree()
    results[output_dataproduct] = ds[output_dataproduct]
    results.to_netcdf(str(output_filename))

def main():
    parser = argparse.ArgumentParser(
            prog="analyse.py",
            description="Perfrom the HVI analysis on a week's data."
    )
    swarm.add_common_args(parser)
    args = parser.parse_args()
    analyse(args)

if  __name__ == "__main__":
    main()
