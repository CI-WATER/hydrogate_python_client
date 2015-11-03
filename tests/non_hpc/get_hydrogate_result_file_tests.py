__author__ = 'Pabitra'

""" This is an example usage of retrieving the output data zip file from hydrogate after successful completion
of a job submission and saving it at user data workspace on HydroDS"""

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# this is the output zip file on hydrogate that we want to save on HydroDs
hydrogate_result_file_path = '/data/result_job101.zip'

try:
    response_data = hds.get_hydrogate_result_file(hg_file_url_path=hydrogate_result_file_path,
                                                  save_as='ueb_result_job101.zip')
    result_file_url = response_data
    print(result_file_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
