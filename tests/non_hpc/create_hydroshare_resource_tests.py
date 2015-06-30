__author__ = 'Pabitra'

""" This is an example usage of the 'create_hydroshare_resource' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# set hydroshare user account
hds.set_hydroshare_account(username=settings.HS_USERNAME, password=settings.HS_PASSWORD)

file_to_use_for_hydroshare_resource = 'canopy_cc.nc'
try:
    # param: title: is optional
    # param: abstract: is optional
    # param: keywords: is optional
    response_data = hds.create_hydroshare_resource(file_name=file_to_use_for_hydroshare_resource,
                                                   resource_type='GenericResource',
                                                   title='Resource created from HydroDS netcdf by pk',
                                                   abstract="Testing creation resource from HydroDS",
                                                   keywords=['HydroShare', 'HydroDS'])
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()