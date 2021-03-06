__author__ = 'Pabitra'

""" This is an example usage of the 'subset_dem' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# first create 2 rasters then can be joined
response_data = hds.subset_dem(left=-111.97, top=42.16, right=-111.32, bottom=41.85,
                               output_raster='raster_1_to_join.tif')
raster_one_url = response_data['output_raster']

response_data = hds.subset_dem(left=-111.97, top=41.85, right=-111.32, bottom=41.66,
                               output_raster='raster_2_to_join.tif')
raster_two_url = response_data['output_raster']

try:
    # param: output_raster is optional
    response_data = hds.combine_rasters(input_one_raster_url_path=raster_one_url,
                                        input_two_raster_url_path=raster_two_url, output_raster='combined_rasters.tif')
    output_combined_raster_url = response_data['output_raster']
    print(output_combined_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()