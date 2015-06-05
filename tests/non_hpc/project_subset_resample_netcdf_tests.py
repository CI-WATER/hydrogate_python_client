__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

# TODO: When using this input parameters it takes does not take much time compared to runing the resample_netcdf()
input_netcdf_url_path = 'http://129.123.41.184:20199/files/data/user_2/projected_prcp_spwan.nc'
ref_netcdf_url_path = 'http://129.123.41.184:20199/files/data/user_2/SpawnWS_yrev.nc'

try:
    # param: output_netcdf is optional
    response_data = client.project_subset_resample_netcdf(input_netcdf_url_path=input_netcdf_url_path,
                                                          ref_netcdf_url_path=ref_netcdf_url_path, variable_name='prcp',
                                                          output_netcdf='proj_subset_resample_prcp_spwan.nc')
    output_netcdf_url = response_data['output_netcdf']
    print(output_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
