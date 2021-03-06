__author__ = 'Pabitra'

""" This is an example usage of the 'create_raster_slope' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset dem to get the output raster to be used as an input for creating the slope raster
response_data = hds.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66)
output_subset_dem_url = response_data['output_raster']

try:
    response_data = hds.create_raster_slope(input_raster_url_path=output_subset_dem_url,
                                            utput_raster='slope_logan.tif')
    output_slope_raster_url = response_data['output_raster']

    # print the url path for the generated raster file
    print(output_slope_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
