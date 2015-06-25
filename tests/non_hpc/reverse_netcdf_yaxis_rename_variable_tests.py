__author__ = 'Pabitra'

""" This is an example usage of the 'reverse_netcdf_yaxis_rename_variable' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_netcdf_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/canopy_cc.nc'

try:
    # param: input_variable_name: is optional
    # param: output_variable_name: is optional
    # param: save_as: is optional (use this to download the output file to the specified directory)
    response_data = hds.reverse_netcdf_yaxis_rename_variable(input_netcdf_url_path=input_netcdf_url,
                                                             input_variable_name='Band1', output_variable_name='Band1',
                                                             output_netcdf='resample_reverse_yaxis_rename_var_1.nc')
    output_reverse_rename_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_reverse_rename_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()