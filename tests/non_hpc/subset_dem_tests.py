__author__ = 'Pabitra'

"""
This is the 1st test that you need to run that are hydrological in nature
This is the only function/service that works with the iRODS. All other dataservices need rework
to make it work with iRDOS.

NOTE: The subset boundary is limited to Western USA only
"""
from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    # param: output_raster is optional
    response_data = hds.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66,
                                   output_raster='subset_dem_logan.tif',
                                   save_as=r'E:\Scratch\HydroGateClientDemo\nedLogan_1B.tif')
    output_subset_dem_url = response_data['output_raster']
    print(output_subset_dem_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE ..."