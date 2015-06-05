__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# TODO: When using this input parameters it takes does not take much time compared to runing the resample_netcdf()
# NOTE: this file path is valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/projected_prcp_spwan.nc'
ref_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnWS_yrev.nc'

try:
    # param: output_netcdf is optional
    response_data = hds.project_subset_resample_netcdf(input_netcdf_url_path=input_netcdf_url_path,
                                                       ref_netcdf_url_path=ref_netcdf_url_path, variable_name='prcp',
                                                       output_netcdf='proj_subset_resample_prcp_spwan.nc')
    output_netcdf_url = response_data['output_netcdf']
    print(output_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
