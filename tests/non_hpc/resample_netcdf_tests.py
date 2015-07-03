__author__ = 'Pabitra'

""" This is an example usage of the 'resample_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: This a long running process
# NOTE: the following url file paths are valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/projected_prcp_spwan.nc'
ref_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnWS_yrev.nc'

try:
    response_data = hds.resample_netcdf(input_netcdf_url_path=input_netcdf_url_path,
                                        ref_netcdf_url_path=ref_netcdf_url_path, variable_name='prcp',
                                        output_netcdf='resample_to_ref_prcp_spwan_3.nc')
    output_resampled_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_resampled_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
