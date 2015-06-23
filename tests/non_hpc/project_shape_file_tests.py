__author__ = 'Pabitra'

""" This is an example usage of the 'project_shapefile' HydroDS client api to project a shapefile using either UTM zone
or EPSG code"""

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# generate the shape file that can then be projected
response_data = hds.create_outlet_shapefile(point_x=-111.787, point_y=41.742, output_shape_file_name='outlet-shape.shp')
output_outlet_shapefile_url = response_data['output_shape_file_name']

try:
    # return: output file will be a zip file with the name same as the value for the param
    # output_shape_file (eg., outlet-proj.zip)

    # projection using UTM zone
    response_data = hds.project_shapefile(input_shapefile_url_path=output_outlet_shapefile_url, utm_zone=12,
                                          output_shape_file='outlet-proj_utm.shp')
    output_proj_utm_shapefile_url = response_data['output_shape_file']

    # print the url path for the generated shapefile
    print(output_proj_utm_shapefile_url)

    # projection using EPSG code
    response_data = hds.project_shapefile(input_shapefile_url_path=output_outlet_shapefile_url, epsg_code=2152,
                                          output_shape_file='outlet-proj_epsg.shp')
    output_proj_epsg_shapefile_url = response_data['output_shape_file']

    # print the url path for the generated shapefile
    print(output_proj_epsg_shapefile_url)
except Exception as ex:
    print(ex.message)

exit()