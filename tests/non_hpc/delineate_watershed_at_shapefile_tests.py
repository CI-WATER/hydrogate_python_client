__author__ = 'Pabitra'

""" This is an example usage of the 'delineate_watershed' HydroDS client api using outlet shapefile """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset raster get the output raster to be used as an input for delineation
response_data = hds.subset_raster(left=-111.97, top=42.11, right=-111.35, bottom=41.66, input_raster='nedWesternUS.tif',
                                  output_raster='subset_dem_logan.tif')

output_subset_dem_url = response_data['output_raster']

# project the subset raster - delineation requires a projected raster
response_data = hds.project_raster_to_UTM_NAD83(input_raster_url_path=output_subset_dem_url, utm_zone=12,
                                                output_raster='projected_raster_logan.tif')
output_proj_raster_url = response_data['output_raster']

# create an outlet shapefile that can be used for delineation
response_data = hds.create_outlet_shapefile(point_x=-111.787, point_y=41.742, output_shape_file_name='outlet_logan.shp')
output_outlet_shapefile_url = response_data['output_shape_file_name']

# project the outlet shapefile
response_data = hds.project_shapefile(input_shapefile_url_path=output_outlet_shapefile_url, utm_zone=12,
                                      output_shape_file='outlet_logan_proj.shp')
output_proj_outlet_shapefile_url = response_data['output_shape_file']

try:
    response_data = hds.delineate_watershed(input_raster_url_path=output_proj_raster_url, threshold=60000,
                                            input_outlet_shapefile_url_path=output_proj_outlet_shapefile_url,
                                            output_raster='logan_ws_shape.tif',
                                            output_outlet_shapefile='logan_outlet_at.shp')

    output_delineated_raster_url = response_data['output_raster']
    print(output_delineated_raster_url)

    output_outlet_shapefile_url = response_data['output_outlet_shapefile']
    print(output_outlet_shapefile_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()