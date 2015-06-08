__author__ = 'Pabitra'
from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    # param: output_raster is optional
    response_data = hds.upload_file(file_to_upload='E:\Scratch\param-test-pk.dat')
    uploaded_file_url = response_data
    print(uploaded_file_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE ..."