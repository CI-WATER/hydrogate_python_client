__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

file_to_delete = 'aspect.tif'
try:
    response_data = client.delete_my_file(file_name=file_to_delete)
    # this should print the name of the file that got deleted
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()