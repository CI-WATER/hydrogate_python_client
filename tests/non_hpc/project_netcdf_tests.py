__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/subset_netcdf_to_spawn.nc'
try:
    # param: output_netcdf is optional
    response_data = hds.project_netcdf(input_netcdf_url_path=input_netcdf_url_path, variable_name='prcp',
                                       utm_zone=12, output_netcdf='projected_prcp_spwan.nc')
    output_proj_netcdf_url = response_data['output_netcdf']
    print(output_proj_netcdf_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
