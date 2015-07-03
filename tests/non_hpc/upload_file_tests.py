__author__ = 'Pabitra'

""" This is an example usage of the 'upload_file' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)
#my_file_to_upload = 'E:\Scratch\param-test-pk.dat'
my_file_to_upload = 'E:\Scratch\LittleBear1000.zip'
try:
    response_data = hds.upload_file(file_to_upload=my_file_to_upload)
    uploaded_file_url = response_data

    # print the url path for the uploaded file
    print(uploaded_file_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE ..."