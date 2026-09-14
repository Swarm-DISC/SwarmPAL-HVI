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

import swarm

a_week = datetime.timedelta(days=7)

def make_config(collection, start_time):
    '''Makes a SwarmPAL config object for downloading VirES data'''
    return dict(data_params=[dict(
        provider='vires',
        collection=collection, 
        measurements=['F', 'B_NEC', 'Flags_F', 'Flags_B', 'Flags_q', 'Flags_Platform'],
        models=["Model = 'CHAOS'"],
        start_time=start_time.isoformat(),
        end_time=(start_time + a_week).isoformat(),
        server_url='https://vires.services/ows',
    )])

def main(args) -> None:

    start_week = swarm.get_swarm_week(args.start_date)
    end_week = swarm.get_swarm_week(args.end_date)
    n_weeks = end_week - start_week
    print(f"Downloading weeks {start_week} to {end_week}")
    for week in range(start_week, end_week+1):
        start_date = swarm.get_swarm_week_start_date(week)
        filename = swarm.make_filename(args.collection, week)

        if os.path.exists(filename):
            print(f"Skipping because file exists: {filename}")
            continue
            
        config = make_config(args.collection, args.start_date)
        data = swarmpal.fetch_data(config)
        data.to_netcdf(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="download.py",
            description="Downloads Swarm data from VIRes"
    )
    swarm.add_common_args(parser)
    args = parser.parse_args()
    main(args)
