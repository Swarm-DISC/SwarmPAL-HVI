#!/bin/bash

#SBATCH --job-name HVI-download
#SBATCH --output slurm-out/%A.out

N_WEEKS=$1

uv run ./download.py --weeks ${N_WEEKS}
