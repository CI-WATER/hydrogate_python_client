__author__ = 'Pabitra'

""" This is an example usage of the 'project_shapefile_to_UTM_NAD83' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# generate the shape file that can then be projected
response_data = hds.create_outlet_shapefile(point_x=-111.787, point_y=41.742, output_shape_file='outlet-shape.shp')
output_outlet_shapefile_url = response_data['output_shape_file_name']

try:
    # param: output_shape_file is optional
    # return: output file will be a zip file with the name same as the value for the param
    # output_shape_file (eg., outlet-proj.zip)
    response_data = hds.project_shapefile_to_UTM_NAD83(input_shapefile_url_path=output_outlet_shapefile_url,
                                                       utm_zone=12, output_shape_file='outlet-proj.shp')
    output_proj_shapefile_url = response_data['output_shape_file']

    # print the url path for the generated shapefile
    print(output_proj_shapefile_url)
except Exception as ex:
    print(ex.message)

exit()