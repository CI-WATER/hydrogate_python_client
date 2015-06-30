__author__ = 'Pabitra'

""" This is an example usage of the 'delete_my_file' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

file_to_delete = 'subset_dem_logan_test.tif'
try:
    response_data = hds.delete_my_file(file_name=file_to_delete)
    # this should print the name of the file that got deleted
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()