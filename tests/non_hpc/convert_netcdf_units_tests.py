__author__ = 'Pabitra'

""" This is an example usage of the 'resample_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: This a long running process
# NOTE: the following url file paths are valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/resample_to_ref_prcp_2_spwan.nc'

try:
    response_data = hds.convert_netcdf_units(input_netcdf_url_path=input_netcdf_url_path,
                                             output_netcdf='converted_units_spwan.nc',
                                             variable_name='prcp', variable_new_units="m/hr",
                                             multiplier_factor=0.00004167, offset=0)
    output_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()