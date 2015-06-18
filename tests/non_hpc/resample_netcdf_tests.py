__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# TODO: When using this input parameters it takes for ever to process this request
# NOTE: this file path is valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/projected_prcp_spwan.nc'
ref_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/SpawnWS_yrev.nc'

# input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_3/LB_prcp_outnc.nc'
# ref_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_3/LittleBearWS.nc'

try:
    # param: output_netcdf is optional
    response_data = hds.resample_netcdf(input_netcdf_url_path=input_netcdf_url_path,
                                        ref_netcdf_url_path=ref_netcdf_url_path, variable_name='prcp',
                                        output_netcdf='resample_to_ref_prcp_spwan_3.nc')
    output_resampled_netcdf_url = response_data['output_netcdf']
    print(output_resampled_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
