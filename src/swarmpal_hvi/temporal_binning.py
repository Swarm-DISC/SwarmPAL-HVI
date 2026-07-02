import datetime

import xarray as xr

from swarmpal.io import PalProcess

class TemporalBinning(PalProcess):
    """A SwarmPAL PalProcess that calculates HVI statistics over a given
    number of sequential measurements in a DataSet"""

    @property
    def process_name(self) -> str:
        return "HVITemporalBinning"

    def set_config(
        self, 
        dataset: str = "",
        N_readings: int = 20,
        input_variables : list[str] = [],
        output_dataset: str = "",
    ) -> None:
        """Set the process configuration.

        Parameters
        ----------
        dataset : str
            The name of the input dataset that this process will operate on
        N_readings : int
            The number of sequential readings used to calculate statistics with.
        input_variables : list[str]
            A list of variables in input_dataset that statistics are calculated over. Logitude and Latitude are
            are always included.
        output_dataset : str
            The name of the DataSet in the DataTree where this process will save results to.
        """
        super().set_config(
            dataset=dataset,
            N_readings=N_readings,
            input_variables=input_variables,
            output_dataset=output_dataset,
        )

    def _call(self, datatree: xr.DataTree) -> xr.DataTree:

        N = self.config["N_readings"]
        dataset = self.config['dataset']
        output_dataset = self.config["output_dataset"]
        input_variables = self.config["input_variables"]
        input_coordinates = ["Longitude", "Latitude"]
        dt = datetime.timedelta(seconds=N)

        datatree[output_dataset] = xr.Dataset()
        # Calculate standard deviations of the variables
        for variable in input_variables:
            variable_resampled = datatree[dataset][variable].resample(Timestamp=dt)
            datatree[output_dataset][variable] = variable_resampled.std(ddof=1, skipna=True)

        # Calculate mean of the coordinates
        for coordinate in input_coordinates:
            coordinate_resampled = datatree[dataset][coordinate].resample(Timestamp=dt)
            datatree[output_dataset][coordinate] = coordinate_resampled.mean()

        return datatree

        #b_nec_groups = ds[dataproduct].swarmpal.magnetic_residual().resample(Timestamp=dt)
        #f_groups = ds[dataproduct]["F"].resample(Timestamp=dt)

        #lon_groups = ds[dataproduct]["Longitude"].resample(Timestamp=dt)
        #lat_groups = ds[dataproduct]["Latitude"].resample(Timestamp=dt)

        ## A new DataSet is created and populated with the mean of spatial coordinates and the standard deviations of the variables.

        #ds[output_dataset] = xr.Dataset()
        #ds[output_dataset]["Longitude"] = lon_groups.mean()
        #ds[output_dataset]["Latitude"] = lat_groups.mean()
        #ds[output_dataset]["B_NEC_std"] = b_nec_groups.std(ddof=1, skipna=True)
        #ds[output_dataset]["F_std"] = f_groups.std(ddof=1, skipna=True)
