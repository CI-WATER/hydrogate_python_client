__author__ = 'Pabitra'

from hydrogate import HydroDS

#>>>>> test iRODS
client = HydroDS()
client.authenticate_user(username='username for irods REST API', password='password for irods REST API')
client.check_irods_server_status()
client.get_irods_collections(listing=True)

#upload_request = client.upload_file_irods(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan_1.tif')

print ">>> DONE..."