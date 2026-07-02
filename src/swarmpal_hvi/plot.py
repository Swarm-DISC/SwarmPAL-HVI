import h3
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import geopandas as gpd

def plot(dataset: xr.Dataset):
    '''Quick and dirty plotting routine for HVI spatially averaged data.'''

    df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(), crs='EPSG:4326')
    df['h3_bin'] = dataset['h3_bin']
    df['geometry'] = df['h3_bin'].map(lambda cell: h3.cells_to_h3shape([cell]))
    df['B_NEC_std_N'] = dataset['magnetic_residual'][:, 0]
    df['B_NEC_std_E'] = dataset['magnetic_residual'][:, 1]
    df['B_NEC_std_C'] = dataset['magnetic_residual'][:, 2]
    df['B_NEC_std'] = np.sqrt(df['B_NEC_std_N']**2 + df['B_NEC_std_E']**2 + df['B_NEC_std_C']**2 )
    df['F_std'] = dataset['F']
    
    # Cells crossing the antimeridian is removed for visualisation:
    
    #df['can_plot'] = np.array([h3.vertex_to_latlng(
    df['lons_east'] = df['h3_bin'].map(lambda cell: any([h3.vertex_to_latlng(v)[1] >  70 for v in h3.cell_to_vertexes(cell)]))
    df['lons_west'] = df['h3_bin'].map(lambda cell: any([h3.vertex_to_latlng(v)[1] < -70 for v in h3.cell_to_vertexes(cell)]))
    df = df.drop(df[df['lons_east'] & df['lons_west']].index)
    df
    
    
    # +
    def plot_df(df, column=None, ax=None, vmin=None, vmax=None):
        "Plot based on the `geometry` column of a GeoPandas dataframe"
        df = df.copy()
        #df = df.to_crs(epsg=8857)
        df = df.to_crs("ESRI:54009")
    
        if ax is None:
            _, ax = plt.subplots(figsize=(8,8))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    
        df.plot(
            ax=ax,
            #alpha=0.5, #edgecolor='k',
            column=column, 
            #categorical=True,
            legend=True,
            vmin=vmin, vmax=vmax,
            #legend_kwds={'loc': 'upper left'},
        )
    
    
    plot_df(df, column='F_std')
    
    plot_df(df, column='B_NEC_std_C', vmin=0, vmax=0.5)
