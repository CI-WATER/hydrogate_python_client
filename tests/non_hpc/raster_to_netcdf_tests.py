__author__ = 'Pabitra'

""" This is an example usage of the 'raster_to_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/projected_raster.tif'
try:
    response_data = hds.raster_to_netcdf(input_raster_url_path=input_raster_url, increasing_y=True,
                                         output_netcdf='raster_to_netcdf_slope_logan.nc')

    output_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()