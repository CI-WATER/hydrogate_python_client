__author__ = 'Pabitra'

"""
Run this test after running generate_outlet_shapefile tests
"""
from hydrogate import Client
import settings

# login to irods
#client.login(username='rods', password='ciwater80')

# account for django api server
client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset dem to get the output raster to be used as an input for delineation
response_data = client.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66)
output_subset_dem_url = response_data['output_raster']

try:
    response_data = client.delineate_watershed(utm_zone=12, threshold=60000, outlet_point_x=111.787,
                                               outlet_point_y=41.742, input_raster_url_path=output_subset_dem_url)
    output_delineated_raster_url = response_data['output_WS_raster']
    print(output_delineated_raster_url)
except Exception as ex:
    print(ex.message)


print ">>>> DONE..."
exit()