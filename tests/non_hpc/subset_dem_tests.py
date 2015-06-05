__author__ = 'Pabitra'

"""
This is the 1st test that you need to run that are hydrological in nature
This is the only function/service that works with the iRODS. All other dataservices need rework
to make it work with iRDOS.

NOTE: The subset boundary is limited to Western USA only
"""
from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)
#client.authenticate_user(username='rods', password='ciwater80')

#get approximate watereshed boundary in geographic coordinates left, top, right, bottom
#-112.04 41.73 -111.5 41.36
# try:
#     # param: output_raster is optional
#     response_data = client.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66,
#                                       output_raster='subset_dem_logan.tif')
#     output_subset_dem_url = response_data['output_raster']
#     print(output_subset_dem_url)
# except Exception as ex:
#     print(ex.message)
#
# # download the subset dem
# if output_subset_dem_url:
#     try:
#         client.download_file(output_subset_dem_url, save_as=r'E:\Scratch\HydroGateClientDemo\nedLogan_1A.tif')
#         print ("Subset dem download was successful.")
#     except Exception as ex:
#         print(ex.message)
#
# print ">>>> DONE ..."
# exit()

# run and download the output
try:
    # param: output_raster is optional
    response_data = client.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66,
                                      output_raster='subset_dem_logan.tif',
                                      save_as=r'E:\Scratch\HydroGateClientDemo\nedLogan_1B.tif')
    output_subset_dem_url = response_data['output_raster']
    print(output_subset_dem_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE ..."