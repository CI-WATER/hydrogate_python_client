__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_NLCD_raster_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/nlcd_proj_spwan.tif'
try:
    # output netcdf parameters are optional
    response_data = hds.get_canopy_variable(input_NLCD_raster_url_path=input_NLCD_raster_url_path, variable_name='cc',
                                            output_netcdf='nlcd_cc-2_spwan.nc')

    output_nlcd_cc_url = response_data['output_netcdf']
    print(output_nlcd_cc_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()