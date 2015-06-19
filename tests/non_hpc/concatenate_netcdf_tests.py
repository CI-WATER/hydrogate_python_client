__author__ = 'Pabitra'

""" This is an example usage of the 'concatenate_netcdf' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
ref_input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
input_netcdf_static_file_1 = 'prcp_2010.nc4'     # this a static dayamet data file on the api server
input_netcdf_static_file_2 = 'prcp_2011.nc4'     # this a static dayamet data file on the api server

try:
    # generate 2 netcdf files that can be concatenated
    response_data = hds.subset_netcdf(input_netcdf=input_netcdf_static_file_1, ref_raster_url_path=ref_input_raster_url,
                                      output_netcdf='prcp_2010_spawn.nc')
    prcp_2010_subset_netcdf_url = response_data['output_netcdf']
    print(prcp_2010_subset_netcdf_url)

    response_data = hds.subset_netcdf(input_netcdf=input_netcdf_static_file_2, ref_raster_url_path=ref_input_raster_url,
                                      output_netcdf='prcp_2011_spawn.nc')
    prcp_2011_subset_netcdf_url = response_data['output_netcdf']
    print(prcp_2011_subset_netcdf_url)

    # concatenate the above 2 output netcdf files
    response_data = hds.concatenate_netcdf(input_netcdf1_url_path=prcp_2010_subset_netcdf_url,
                                           input_netcdf2_url_path=prcp_2011_subset_netcdf_url,
                                           output_netcdf='prcp_2010_2011_spawn.nc')
    output_concatenated_netcdf_url = response_data['output_netcdf']
    print(output_concatenated_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()

