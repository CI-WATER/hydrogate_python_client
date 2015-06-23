__author__ = 'Pabitra'

""" This is an example usage of the 'subset_project_resample_raster' HydroDS client api where projection can be done
 using UTM or EPSG """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_raster = "nedWesternUS.tif"
try:
    # using UTM based projection
    response_data = hds.subset_project_resample_raster(input_raster=input_raster, left=-111.97, top=42.11,
                                                       right=-111.35, bottom=41.66, cell_size_dx=100, cell_size_dy=100,
                                                       output_raster='subset_project_resample_logan_utm.tif',
                                                       resample='bilinear')
    output_subset_proj_resample_utm_raster_url = response_data['output_raster']

    # print the url path for the generated raster file
    print(output_subset_proj_resample_utm_raster_url)

    # using EPSG based projection
    response_data = hds.subset_project_resample_raster(input_raster=input_raster,left=-111.97, top=42.11, right=-111.35,
                                                       bottom=41.66, cell_size_dx=100, cell_size_dy=100, epsg_code=2152,
                                                       output_raster='subset_project_resample_logan_epsg.tif',
                                                       resample='bilinear')
    output_subset_proj_resample_epsg_raster_url = response_data['output_raster']

    # print the url path for the generated raster file
    print(output_subset_proj_resample_epsg_raster_url)

except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
