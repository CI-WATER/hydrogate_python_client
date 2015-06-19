__author__ = 'Pabitra'

""" This is an example usage of the 'project_raster_to_UTM_NAD83' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset dem to get the output raster to be used as an input for creating the projected raster
response_data = hds.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66)
output_subset_dem_url = response_data['output_raster']

try:
    # param: output_raster is optional
    response_data = hds.project_raster_to_UTM_NAD83(input_raster_url_path=output_subset_dem_url, utm_zone=12,
                                                    output_raster='projected_raster.tif')
    output_proj_raster_url = response_data['output_raster']

    # print the url path for the generated raster file
    print(output_proj_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
