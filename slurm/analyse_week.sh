#!/bin/bash


#SBATCH --job-name HVI-analise-week
#SBATCH --account geos_extra
#SBATCH --output slurm-out/%A_%a.out
#SBATCH --array=1-12

uv run ./analyse_week.py --week ${SLURM_ARRAY_TASK_ID}
