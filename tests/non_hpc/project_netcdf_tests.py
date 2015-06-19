__author__ = 'Pabitra'

""" This is an example usage of the 'project_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/subset_netcdf_to_spawn.nc'
try:
    # param: output_netcdf is optional
    # param: save_as: is optional (use this to download the output file to the specified directory)
    response_data = hds.project_netcdf(input_netcdf_url_path=input_netcdf_url_path, variable_name='prcp',
                                       utm_zone=12, output_netcdf='projected_prcp_spwan.nc')
    output_proj_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_proj_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
