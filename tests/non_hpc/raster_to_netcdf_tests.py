__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

input_raster_url = 'http://129.123.41.184:20199/files/data/user_2/SpawnProj.tif'
try:
    # param: output_netcdf is optional
    response_data = client.raster_to_netcdf(input_raster_url_path=input_raster_url, output_netcdf='raster_to_netcdf.nc')
    output_aspecte_raster_url = response_data['output_netcdf']
    print(output_aspecte_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()