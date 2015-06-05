__author__ = 'Pabitra'

"""
This test needs to be run after running project_dem_tests
"""
from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

input_raster_url = 'http://129.123.41.184:20199/files/data/user_2/SpawnProj.tif'
try:
    # param: output_raster is optional
    response_data = client.resample_raster(input_raster_url_path=input_raster_url, cell_size_dx=50, cell_size_dy=50,
                                           output_raster='resample_spawn.tif')
    output_resample_raster_url = response_data['output_raster']
    print(output_resample_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()

