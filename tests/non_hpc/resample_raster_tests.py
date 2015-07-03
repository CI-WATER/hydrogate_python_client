__author__ = 'Pabitra'

""" This is an example usage of the 'project_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
try:

    response_data = hds.resample_raster(input_raster_url_path=input_raster_url, cell_size_dx=50, cell_size_dy=50,
                                        resample='near', output_raster='resample_spawn2.tif')
    output_resample_raster_url = response_data['output_raster']

    # print the url path for the generated raster file
    print(output_resample_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()

