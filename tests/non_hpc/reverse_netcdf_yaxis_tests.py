__author__ = 'Pabitra'

""" This is an example usage of the 'reverse_netcdf_yaxis' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_netcdf_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/resample.nc'

try:
    # param: save_as: is optional (use this to download the output file to the specified directory)
    response_data = hds.reverse_netcdf_yaxis(input_netcdf_url_path=input_netcdf_url,
                                             output_netcdf='resample_reverse_yaxis.nc')
    output_reverse_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_reverse_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()