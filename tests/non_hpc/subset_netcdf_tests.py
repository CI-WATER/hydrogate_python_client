__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

ref_input_raster_url = 'http://129.123.41.184:20199/files/data/user_2/SpawnProj.tif'
input_netcdf_static_file = 'prcp_2010.nc4'     # this a static dayamet data file on the api server

try:
    # param: output_netcdf is optional
    response_data = client.subset_netcdf(input_netcdf=input_netcdf_static_file, ref_raster_url_path=ref_input_raster_url,
                                         output_netcdf='subset_netcdf_to_spawn.nc')
    output_subset_netcdf_url = response_data['output_netcdf']
    print(output_subset_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()