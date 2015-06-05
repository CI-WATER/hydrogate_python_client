__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

input_netcdf_url = 'http://129.123.41.184:20199/files/data/user_2/resample.nc'

try:
    # param: output_netcdf is optional
    response_data = client.reverse_netcdf_yaxis(input_netcdf_url_path=input_netcdf_url,
                                                output_netcdf='resample_reverse_yaxis.nc')
    output_reverse_netcdf_url = response_data['output_netcdf']
    print(output_reverse_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()