__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

file_to_delete = 'aspect.tif'
try:
    response_data = hds.delete_my_file(file_name=file_to_delete)
    # this should print the name of the file that got deleted
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()