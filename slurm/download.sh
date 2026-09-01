#!/bin/bash

#SBATCH --job-name HVI-download
#SBATCH --output slurm-out/%A.out
#SBATCh --mem 8G

N_WEEKS=$1

uv run ./download.py "$@"
