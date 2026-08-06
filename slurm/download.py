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
import swarmpal
import datetime

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

def main(args) -> None:
    start_time = datetime.datetime(year, 1, 1)
    for week in range(1, args.weeks+1):
        filename = f'data/{year}_{week:03}.nc'
        if os.path.exists(filename):
            print(f"Skipping because file exists: {filename}")
            continue
            
        config = make_config(start_time)
        data = swarmpal.fetch_data(config)
        data.to_netcdf(filename)
        start_time += a_week


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="download.py",
            description="Downloads Swarm data from VIRes"
    )
    parser.add_argument("-w", "--weeks", default=12, type=int, help="The number of weeks worth of data to download")
    args = parser.parse_args()
    main(args)
