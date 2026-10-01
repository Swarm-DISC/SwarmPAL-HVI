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
from pathlib import Path

#from swarmpal.io._paldata import PalDataItem, create_paldata
from swarmpal import fetch_data

from swarmpal_hvi.spatial_h3_binning import SpatialH3Binning
from swarmpal_hvi.temporal_binning import TemporalBinning
import swarmpal_hvi.data as hvi_data

import swarm

def analyse(args):

    start_week = hvi_data.get_swarm_week(args.start_date)
    end_week = hvi_data.get_swarm_week(args.end_date)
    n_weeks = end_week - start_week
    print(f"Performing temporal binning on weeks {start_week} to {end_week}")
    data_dir = Path('data')
    for week in range(start_week, end_week+1):
        input_filename = data_dir / hvi_data.make_dataset_filename(args.collection, week)
        output_filename = data_dir / hvi_data.make_dataset_filename(args.collection, week, 'time_binned')

        if os.path.exists(output_filename):
            print(f"File exists: {output_filename}")
            continue

        config = dict(data_params=[dict(
            provider='file',
            filename=str(input_filename),
            filetype='netcdf',
            dataset=args.collection,
        )])

        #ds = create_paldata(**{
        #    dataproduct: PalDataItem.from_file(f"data/2016_{args.week:02}.nc")
        #})
        ds = fetch_data(config)
        dataproduct = '/' + args.collection

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

        #spatial_binning = SpatialH3Binning(dict(
        #    dataset=dataproduct + "_time_binned",
        #    resolution=2,
        #    output_dataset=dataproduct + "_spatial_binned",
        #    input_variables=["F", "magnetic_residual"]
        #))
        #ds = spatial_binning(ds)

        results = xr.DataTree()
        #results[dataproduct + "_spatial_binned"] = ds[dataproduct + "_spatial_binned"]
        results[dataproduct + "_time_binned"] = ds[dataproduct + "_time_binned"]
        results.to_netcdf(str(output_filename))

def main():
    parser = argparse.ArgumentParser(
            prog="analyse.py",
            description="Perfrom the HVI analysis on a week's data."
    )
    swarm.add_common_args(parser)
    args = parser.parse_args()
    analyse(args)

if __name__ == "__main__":
    main()
