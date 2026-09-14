# Hazard Variation Index in SwarmPAL

This is a standalone [SwarmPAL][swarmpal] toolbox that implements the the [Hazard Variation Index][hvi_paper].


## Analysis with Slurm on HPC

Performing the HVI analysis over the 11 year period for which Swarm data is available
is computationaly expensive.
The [`slurm/`](slurm/) directory has scripts to download the data and perform the analysis
on HPC infrastructure hosted by the University of Edinburgh's School of GeoSciences.
The pipeline can be visualised with the following diagram:

```mermaid
---
config:
  theme: redux-color
  look: neo
  layout: elk
---

flowchart LR
    subgraph slurm [GeoSciences Cluster]
        download@{ shape: procs, label: download.py}
        week@{ shape: procs, label: analyse_week.py}
        all[analyse_all.py]
    end

    subgraph github
        cache
    end
    style cache stroke-dasharray: 5 5
    style github stroke-dasharray: 5 5

    subgraph Laptop
        visualise
    end

    download --> week
    week --> all
    cache --> visualise
    all --> cache
```



## Licence

See [LICENCE](LICENCE)



[swarmpal]: https://github.com/Swarm-DISC/SwarmPAL
[hvi_paper]: https://doi.org/10.1051/swsc/2024033
