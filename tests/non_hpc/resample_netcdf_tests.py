__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

# TODO: When using this input parameters it takes for ever to process this request
input_netcdf_url_path = 'http://129.123.41.184:20199/files/data/user_2/projected_prcp_spwan.nc'
ref_netcdf_url_path = 'http://129.123.41.184:20199/files/data/user_2/SpawnWS_yrev.nc'

try:
    # param: output_netcdf is optional
    response_data = client.resample_netcdf(input_netcdf_url_path=input_netcdf_url_path,
                                           ref_netcdf_url_path=ref_netcdf_url_path, variable_name='prcp',
                                           output_netcdf='resample_to_ref_prcp_spwan.nc')
    output_resampled_netcdf_url = response_data['output_netcdf']
    print(output_resampled_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
