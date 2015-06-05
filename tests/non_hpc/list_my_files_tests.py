__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

client = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    response_data = client.list_my_files()
    for file_url in response_data:
        print(file_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()