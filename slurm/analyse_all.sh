#!/bin/bash

#SBATCH --mem=16G
#SBATCH --job-name HVIAnalyseAll
#SBATCH --account geos_research
#SBATCH --output slurm-out/%A.out

uv run ./analyse_all.py "$@"
