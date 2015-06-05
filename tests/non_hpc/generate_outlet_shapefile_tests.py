__author__ = 'Pabitra'

# TODO : check if this test has any dependency on other tests
from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    # param: outlet_raster is optional
    # return: output file will be a zip file with the name same as the value for the param output_raster (eg., outlet-shape.zip)
    response_data = client.create_outlet_shapefile(point_x=-111.787, point_y=41.742, output_shape_file='outlet-shape.shp')
    output_outlet_shapefile_url = response_data['output_shape_file_name']
    print(output_outlet_shapefile_url)
except Exception as ex:
    print(ex.message)

exit()