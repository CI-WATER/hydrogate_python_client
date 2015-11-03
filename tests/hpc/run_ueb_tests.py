__author__ = 'Pabitra'

""" This is an example usage of various hydrogate api for running a UEB model """

from hydrogate import HydroDS
from tests import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# set HydroGate authentication
# here hpc is the USU HPC - where UEB will be executed
hds.hydrogate_authenticate(username=settings.HG_USERNAME, password=settings.HG_PASSWORD, hpc='USU')
HYDROGATE_STATUS_SUCCESS = 'success'

# upload a package (e.g., ueb input data package) to USU hpc
ueb_input_pkg_url_path = hds.hydro_ds_base_url + '/files/data/user_2/LittleBear1000A.zip'

try:
    pkg_upload_request, upload_status = hds.upload_package(package_file_url_path=ueb_input_pkg_url_path,
                                                           wait_until_done=True)
    if upload_status == HYDROGATE_STATUS_SUCCESS:
        # submit job to run ueb
        submit_job_request, submit_job_status = hds.submit_job(package_id=pkg_upload_request.service_id_value,
                                                               program_name='ueb', wait_until_done=True)
        if submit_job_status == HYDROGATE_STATUS_SUCCESS:
            # save locally
            hds.download_file_from_hydrogate(hg_file_url_path=submit_job_request.file_path,
                                             save_as=r'E:\Scratch\HydroGateClientDemo\LittleBear1000F_output.zip')
            # save in HydroDS
            hds.get_hydrogate_result_file(hg_file_url_path=submit_job_request.file_path,
                                          save_as='LittleBear1000F_output.zip')

            # TODO: save in HydroShare

            print('UEB run successful')
        else:
            print('Run job error:' + submit_job_status)
    else:
        print('Package upload error:' + upload_status)

except Exception as ex:
    print(ex.message)

print(">>>Done...")