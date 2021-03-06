__author__ = 'Pabitra'

""" This is an example usage of the 'zip_files' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: these files are expected to be on the server for user with id 2
files_to_zip = ['subset.nc', 'projected.tif']
try:
    # param: save_as: optional for downloading the output zip file to specified directory
    response_data = hds.zip_files(files_to_zip=files_to_zip, zip_file_name='test_zip_pk.zip')
    output_zip_file_url = response_data['zip_file_name']

    # print the url path for the generated zip file
    print(output_zip_file_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()