__author__ = 'Pabitra'

""" This is an example usage of the 'create_hydroshare_resource' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# set hydroshare user account
hds.set_hydroshare_account(username=settings.HS_USERNAME, password=settings.HS_PASSWORD)

file_to_use_for_hydroshare_resource = 'streamflow_calibration.dat'
#file_to_use_for_hydroshare_resource = 'PBProj.tif'
try:
    # param: title: is optional
    # param: abstract: is optional
    # param: keywords: is optional
    # param: metadata: is optional
    metadata = []
    metadata.append({'creator': {'name': 'Pabitra Dash', 'email': 'pabitra.dash@usu.edu'}})
    metadata.append({'contributor': {'name': 'John Smith', 'email': 'jsmith@gmail.com'}})
    metadata.append({'contributor': {'name': 'Lisa Anderson', 'email': 'landerson@gmail.com'}})
    metadata.append({'coverage': {'type': 'box',
                                  'value': {'northlimit': '30',
                                            'southlimit': '20',
                                            'eastlimit': '100',
                                            'westlimit': '40',
                                            'units': 'Decimal degrees',
                                            'projection': 'WGS 84 EPSG:4326'
                                            }
                                  }
                     })
    response_data = hds.create_hydroshare_resource(file_name=file_to_use_for_hydroshare_resource,
                                                   resource_type='GenericResource',
                                                   title='Topnet streamflow data from HydroDS',
                                                   abstract="Testing creation resource from HydroDS",
                                                   keywords=['HydroShare', 'HydroDS', 'TOPNET'],
                                                   metadata=metadata)
    print(response_data)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()