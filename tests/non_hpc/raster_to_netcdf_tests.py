__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
try:
    # param: output_netcdf is optional
    response_data = hds.raster_to_netcdf(input_raster_url_path=input_raster_url, output_netcdf='raster_to_netcdf.nc')
    output_aspecte_raster_url = response_data['output_netcdf']
    print(output_aspecte_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()