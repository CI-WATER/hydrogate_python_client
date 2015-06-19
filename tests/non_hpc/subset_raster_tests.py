__author__ = 'Pabitra'

""" This is an example usage of the 'subset_raster_to_reference' HydroDS client api """
from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
ref_input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
input_raster_url = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/projected_raster.tif'

try:
    # param: output_raster is optional
    # param: save_as: is optional (use this to download the output file to the specified directory)
    response_data = hds.subset_raster_to_reference(input_raster_url_path=input_raster_url,
                                                   ref_raster_url_path=ref_input_raster_url,
                                                   output_raster='subset_to_spawn.tif')
    output_subset_raster_url = response_data['output_raster']

    # print the url path for the generated netcdf file
    print(output_subset_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()