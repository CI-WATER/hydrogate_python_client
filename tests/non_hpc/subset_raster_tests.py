__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

ref_input_raster_url = 'http://129.123.41.184:20199/files/data/user_2/SpawnProj.tif'
input_raster_url = 'http://129.123.41.184:20199/files/data/user_2/projected_raster.tif'

try:
    # param: output_raster is optional
    response_data = client.subset_raster(input_raster_url_path=input_raster_url, ref_raster_url_path=ref_input_raster_url,
                                         output_raster='subset_to_spawn.tif')
    output_subset_raster_url = response_data['output_raster']
    print(output_subset_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()