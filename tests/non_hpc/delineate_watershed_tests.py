__author__ = 'Pabitra'

""" This is an example usage of the 'delineate_watershed' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset dem to get the output raster to be used as an input for delineation
response_data = hds.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66)
output_subset_dem_url = response_data['output_raster']

try:
    response_data = hds.delineate_watershed(input_raster_url_path=output_subset_dem_url, outlet_point_x=111.787,
                                            outlet_point_y=41.742, utm_zone=12, threshold=60000,
                                            output_raster='logan_ws.tif', output_outlet_shapefile='logan_outlet.shp')
    output_delineated_raster_url = response_data['output_raster']
    print(output_delineated_raster_url)
    output_outlet_shapefile_url = response_data['output_outlet_shapefile']
    print(output_outlet_shapefile_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()