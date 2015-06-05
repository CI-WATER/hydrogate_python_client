__author__ = 'Pabitra'

"""
This test needs to be run after running project_dem_tests
"""
from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
try:
    # param: output_raster is optional
    response_data = hds.resample_raster(input_raster_url_path=input_raster_url, cell_size_dx=50, cell_size_dy=50,
                                        output_raster='resample_spawn.tif')
    output_resample_raster_url = response_data['output_raster']
    print(output_resample_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()

