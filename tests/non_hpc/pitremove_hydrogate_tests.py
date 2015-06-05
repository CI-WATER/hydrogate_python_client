__author__ = 'Pabitra'

""""
Run this test after successfully running subset_dem test
"""
import time
from hydrogate import HydroDS

client = HydroDS()


# user needs to be authenticated to USU hpc system in order to transfer file
# to HPC system and then to run 'pitremove' on HPC
client.authenticate_user(username="hydrogate username",  password="hydrogate password", hpc='USU')

subset_dem_request = client.get_most_recent_request(service_name='subset_dem')
if subset_dem_request:
    client.upload_package(subset_dem_request.file_path)
else:
    print("Error: Did not find a subset dem file to upload for pitremove.")
    exit()

# give some time to finish package upload
time.sleep(10)

# now check upload status
upload_status_request = client.get_upload_status()
if upload_status_request.service_status == "PackageTransferDone":
    # get the file name excluding the '.zip' part
    input_raster_file_name = subset_dem_request.file_path.split('/')[-1][:-4]
    client.submit_job(package_id=upload_status_request.service_id_value, program_name='pitremove',
                      input_raster_file_name=input_raster_file_name)
else:
    print("Package upload is in progress.")
    exit()

# give some time to finish pitremove program to finish
time.sleep(10)

# check submit_job status
submit_job_request = client.get_most_recent_request(service_name='submit_job')
if submit_job_request:
    job_status = client.get_job_status(job_id=submit_job_request.service_id_value)
else:
    print "Error: Failed to check job submit status."
    exit()

if job_status:
    if job_status == 'JobOutputFileTransferDone':
        # user needs to authenticate to iRODS to be able to download the pitremove output file
        client.authenticate_user(username='rods', password='ciwater80')
        client.download_file(file_url_path=submit_job_request.file_path, save_as=r'E:\Scratch\HydroGateClientDemo\pitremove_5.zip')
    else:
        print "Output file is not yet available for download."


print ">>>> DONE ..."