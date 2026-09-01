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
import math
from glob import glob
import datetime

import xarray as xr

#from download import swarm_start_time, make_filename
import swarm

#def make_config(dataproduct, filename):
#    return dict(data_params=[dict(
#        provider='file',
#        filename=filename,
#        filetype='netcdf',
#        dataset=dataproduct,
#    )])

def main(args):
    print(args)

    start_dt = swarm.get_swarm_week(args.start_date)
    print(start_dt)

    end_dt = swarm.get_swarm_week(args.end_date)
    print(end_dt)
    return

    files = glob(f"data/*analysed.nc")
    print(files)
    if len(files) == 0:
        print("No data files to aggregate")
        return

    dataproduct = 'SW_OPER_MAGB_LR_1B_spatial_binned'
    n_datafiles = len(files)

    result = xr.load_datatree(files.pop())
    #for variable in result.variables:
    #    result[dataproduct][variable] = result[dataproduct][variable]**2
    while len(files) > 0:
        dt = xr.load_datatree(files.pop())
        r, dataset = xr.align(
            result[dataproduct].dataset, 
            dt[dataproduct].dataset,
            join = 'outer',
            fill_value=0.0,
        )

        for variable in result.variables:
            result[dataproduct][variable] = r[variable] + dataset[variable] #**2

    for variable in result.variables:
        result[variable] /= n_datafiles
        #result[variable] = np.sqrt(result[variable])

    result.to_netcdf("data/aggregated.nc")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="aggregrate.py",
            description="Merge the HVI results from several time periods"
    )
    swarm.add_common_args(parser)
    args = parser.parse_args()
    main(args)
