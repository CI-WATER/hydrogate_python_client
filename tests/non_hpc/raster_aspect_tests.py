__author__ = 'Pabitra'

""" This is an example usage of the 'create_raster_aspect' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset dem to get the output raster to be used as an input for creating the aspect raster
response_data = hds.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66)
output_subset_dem_url = response_data['output_raster']

try:
    # param: output_raster is optional
    response_data = hds.create_raster_aspect(input_raster_url_path=output_subset_dem_url,
                                             output_raster='aspect_logan.tif')
    output_aspect_raster_url = response_data['output_raster']

     # print the url path for the generated raster file
    print(output_aspect_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()