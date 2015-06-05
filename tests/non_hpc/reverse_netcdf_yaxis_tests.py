__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_netcdf_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/resample.nc'

try:
    # param: output_netcdf is optional
    response_data = hds.reverse_netcdf_yaxis(input_netcdf_url_path=input_netcdf_url,
                                             output_netcdf='resample_reverse_yaxis.nc')
    output_reverse_netcdf_url = response_data['output_netcdf']
    print(output_reverse_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()