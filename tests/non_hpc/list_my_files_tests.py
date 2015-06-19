__author__ = 'Pabitra'

""" This is an example usage of the 'list_my_files' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
client = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    response_data = client.list_my_files()
    for file_url in response_data:
        print(file_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()