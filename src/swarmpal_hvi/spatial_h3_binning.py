import xarray as xr

from swarmpal.io import PalProcess

class SpatialH3Binning(PalProcess):
    """A SwarmPAL PalProcess that calculates HVI statistics in
    H3 spatial binns"""

    def set_config(
        self,
        resolution: int = 4,
        output_dataset: str = "",
    ) -> None:
        """Set the process configuration.

        Parameters
        ----------
        resolution : int
            The H3 resulution @see
        input_variables : list[str]
            A list of variables in input_dataset that spatial statistics are calculated over
        output_dataset : str
            The name of the DataSet in the DataTree where this process will save results to.
        """
        super().set_config(
            resolution=resolution,
            output_dataset=output_dataset,
        )

    def _call(self, datatree: DataTree) -> DataTree:
        output_dataset = self.config["output_dataset"]
        resolution = self.config["resolution"]

        def latlng_to_cell_3(lat, long):
            try:
                return h3.latlng_to_cell(long, lat, resolution)
            except:
                return ''
        
        # Calculate the h3 bin for each time average sample
        ds[self.active_variable]["h3_bin"] = xr.apply_ufunc(
            latlng_to_cell_3,
            ds[self.active_variable]["Longitude"],
            ds[self.active_variable]["Latitude"],
            vectorize=True,
        )
        
        # Remove samples that fall outside h3 coverage
        idx = ds[self.active_variable]["h3_bin"] == ''
        ds[self.active_variable] = ds[self.active_variable].to_dataset().drop_isel(Timestamp=idx)

        ds[output_dataset] = xr.Dataset()
        
        for variable in input_variables:
            binned = ds[self.active_variable][variable].groupby(ds[self.active_variable]['h3_bin'])
            ds[output_dataset][variable] = binned.mean()
