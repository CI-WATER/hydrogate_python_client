__author__ = 'Pabitra'

""" This is an example usage of the 'subset_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
ref_input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
input_netcdf_static_file = 'prcp_2010.nc4'     # this a static dayamet data file on the api server

try:
    # param: save_as: is optional (use this to download the output file to the specified directory)
    response_data = hds.subset_netcdf(input_netcdf=input_netcdf_static_file, ref_raster_url_path=ref_input_raster_url,
                                      output_netcdf='subset_netcdf_to_spawn.nc')

    output_subset_netcdf_url = response_data['output_netcdf']
     # print the url path for the generated netcdf file
    print(output_subset_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()