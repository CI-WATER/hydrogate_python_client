__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

# generate the shape file that can then be projected
response_data = client.create_outlet_shapefile(point_x=-111.787, point_y=41.742, output_shape_file='outlet-shape.shp')
output_outlet_shapefile_url = response_data['output_shape_file_name']

try:
    # param: output_shape_file is optional
    # return: output file will be a zip file with the name same as the value for the param output_shape_file (eg., outlet-proj.zip)
    response_data = client.project_shapefile_to_UTM_NAD83(input_shapefile_url_path=output_outlet_shapefile_url,
                                                          utm_zone=12, output_shape_file='outlet-proj.shp')
    output_proj_shapefile_url = response_data['output_shape_file']
    print(output_proj_shapefile_url)
except Exception as ex:
    print(ex.message)

exit()