__author__ = 'Pabitra'

""" This is an example usage of the 'subset_netcdf_by_time' HydroDS client api """
from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/subset_netcdf_to_spawn.nc'
try:
    # param: save_as is set to None by default. To save the output file to local disk set this parameter to a local file
    # path (eg., c:/scratch/subset_prcp_spwan_1_to_10_days.nc
    response_data = hds.subset_netcdf_by_time(input_netcdf_url_path=input_netcdf_url_path,
                                              time_dimension_name='time', start_date='01/01/2010', end_date='01/11/2010',
                                              output_netcdf='subset_prcp_spwan_1_to_10_days.nc')
    output_subset_netcdf_url = response_data['output_netcdf']

    # print the url path for the generated netcdf file
    print(output_subset_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()