__author__ = 'Pabitra'

""" This is an example usage of the 'download_file' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_NLCD_raster_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/nlcd_proj_spwan.tif'
try:
    hds.download_file(file_url_path=input_NLCD_raster_url_path, save_as=r'E:\Scratch\HydroGateClientDemo\nlcd_proj_spwan.tif')
    print("Download successful")
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()