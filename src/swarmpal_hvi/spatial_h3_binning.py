import xarray as xr

import h3

from swarmpal.io import PalProcess

class SpatialH3Binning(PalProcess):
    """A SwarmPAL PalProcess that calculates HVI statistics in
    H3 spatial binns"""

    @property
    def process_name(self) -> str:
        return "HVIH3SPatialBinning"

    def set_config(
        self,
        dataset: str = "",
        input_variables: list[str] = [],
        resolution: int = 4,
        output_dataset: str = "",
    ) -> None:
        """Set the process configuration.

        Parameters
        ----------
        dataset : str
            The name of the input dataset that this process will operate on
        resolution : int
            The H3 resulution @see
        input_variables : list[str]
            A list of variables in input_dataset that spatial statistics are calculated over
        output_dataset : str
            The name of the DataSet in the DataTree where this process will save results to.
        """
        super().set_config(
            dataset=dataset,
            resolution=resolution,
            input_variables=input_variables,
            output_dataset=output_dataset,
        )

    def _call(self, datatree: xr.DataTree) -> xr.DataTree:
        dataset = self.config["dataset"]
        output_dataset = self.config["output_dataset"]
        input_variables = self.config["input_variables"]
        resolution = self.config["resolution"]

        def latlng_to_cell_3(lat, long):
            try:
                return h3.latlng_to_cell(long, lat, resolution)
            except:
                return ''
        
        # Calculate the h3 bin for each time average sample
        datatree[dataset]["h3_bin"] = xr.apply_ufunc(
            latlng_to_cell_3,
            datatree[dataset]["Longitude"],
            datatree[dataset]["Latitude"],
            vectorize=True,
        )
        
        # Remove samples that fall outside h3 coverage
        idx = datatree[dataset]["h3_bin"] == ''
        datatree[dataset] = datatree[dataset].to_dataset().drop_isel(Timestamp=idx)

        datatree[output_dataset] = xr.Dataset()
        
        for variable in input_variables:
            print(dataset, variable)
            binned = datatree[dataset][variable].groupby(datatree[dataset]['h3_bin'])
            datatree[output_dataset][variable] = binned.mean()

        return datatree
