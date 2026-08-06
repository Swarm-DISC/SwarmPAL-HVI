#!/bin/bash

#SBATCH --job-name HVI-aggregate
#SBATCH --output slurm-out/%A.out

uv run aggregate.py
