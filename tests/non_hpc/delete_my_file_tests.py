__author__ = 'Pabitra'

""" This is an example usage of the 'delete_my_file' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# # delete a specific file
file_to_delete = 'subset_dem_logan_test_2.tif'
try:
    response_data = hds.delete_my_file(file_name=file_to_delete)
    # this should print the name of the file that got deleted
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()

# delete all my files
try:
    response_data = hds.list_my_files()
    for file_url in response_data:
        file_to_delete = file_url.split('/')[-1]
        hds.delete_my_file(file_name=file_to_delete)
        print("deleted file:" + file_to_delete)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()