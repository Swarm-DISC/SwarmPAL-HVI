#!/bin/bash


#SBATCH --job-name HVI-analise-week
#SBATCH --account geos_extra
#SBATCH --mem 4Gb
#SBATCH --output slurm-out/%A.out
# SBATCH --array=1-12

uv run ./analyse_week.py "$@"
