__author__ = 'Pabitra'

""" This is an example usage of the 'create_outlet_shape_file' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    # param: output_shape_file is optional
    # return: output file will be a zip file with the name same as the value for the param output_raster
    # (eg., outlet-shape.zip)
    response_data = hds.create_outlet_shapefile(point_x=-111.787, point_y=41.742, output_shape_file='outlet-shape.shp')
    output_outlet_shapefile_url = response_data['output_shape_file_name']
    print(output_outlet_shapefile_url)
except Exception as ex:
    print(ex.message)

exit()