__author__ = 'Pabitra'

""" This is an example usage of the 'get_static_files_info' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    response_data = hds.get_static_files_info()
    for static_file_item in response_data:
        for variable in static_file_item['variables']:
            print('variable name:' + variable['name'])
            print('variable description:' + variable['description'])
            print('variable unit:' + variable['unit'])

        print('time period:' + str(static_file_item['time_period']))
        print('spatial extent:' + static_file_item['spatial_extent'])
        print('data source:' + static_file_item['data_source'])
        print('data format:' + static_file_item['data_format'])
        print('file name:' + static_file_item['file_name'])
        print('-------------------------------------')
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()