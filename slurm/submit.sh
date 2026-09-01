#!/bin/bash

#
# 
#
if [[ -z $1 ]]; then
    echo "Provide the number of weeks to analyse as the first argument"
    exit 1
fi
#N_WEEKS=$1
mkdir -p {data,slurm-out}

DOWNLOAD_JOB_ID=$(sbatch --parsable download.sh "$@")
echo "Submitted download job with JobID: ${DOWNLOAD_JOB_ID}"

ANALYSE_JOB_ID=$(sbatch --parsable --dependency=afterok:${DOWNLOAD_JOB_ID} analyse_all.sh "$@")
echo "Submitted analysis job with JobID: ${ANALYSE_JOB_ID}"

#ANALYSE_JOB_ID=$(sbatch --parsable --dependency=${DOWNLOAD_JOB_ID} --array=1-${N_WEEKS} analyse_week.sh)
#echo "Submitted ${N_WEEKS} analyse jobs with JobID: ${ANALYSE_JOB_ID}"

#AGGREGATE_JOB_ID=$(sbatch --parsable --dependency=${ANALYSE_JOB_ID} aggregate.sh)
#AGGREGATE_JOB_ID=$(sbatch --parsable aggregate.sh)
#echo "Submitted aggregate job over ${N_WEEKS} weeks with JobID: ${AGGREGATE_JOB_ID}"
