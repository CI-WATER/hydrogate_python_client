__author__ = 'Pabitra'

""" This is an example usage of the 'download_file' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# set hydroshare user account
hds.set_hydroshare_account(username=settings.HS_USERNAME, password=settings.HS_PASSWORD)
# NOTE: this file path is valid for user with id 2
file_to_upload_to_hydroshare_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/canopy_cc.nc'

try:
    # param: title: is optional
    # param: abstract: is optional
    # param: keywords: is optional
    response_data = hds.create_hydroshare_resource(file_url_path=file_to_upload_to_hydroshare_url_path,
                                             local_download_directory='E:\Scratch\HydroGateClientDemo',
                                             resource_type='GenericResource', title='Resource created from HydroDS')
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
