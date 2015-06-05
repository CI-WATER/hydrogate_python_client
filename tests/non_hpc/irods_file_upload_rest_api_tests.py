__author__ = 'Pabitra'

from hydrogate import HydroDS

client = HydroDS()

# login to irods
client.login(username='username for irods rest API', password='password for irods REST API')
client.upload_file_irods(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan_2.tif')

print(">>>>DONE ..")