__author__ = 'Pabitra'

""" This is an example usage of the 'get_canopy_variables' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
input_NLCD_raster_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/nlcd_proj_spwan.tif'
try:
    # output netcdf parameters are optional
    response_data = hds.get_canopy_variables(input_NLCD_raster_url_path=input_NLCD_raster_url_path,
                                             output_ccNetCDF='nlcd_cc_spwan.nc',
                                             output_hcanNetCDF='nlcd_hcan_spwan.nc',
                                             output_laiNetCDF='nlcd_lai_spwan.nc')
    output_nlcd_cc_url = response_data['out_ccNetCDF']
    print(output_nlcd_cc_url)
    output_nlcd_hcan_url = response_data['out_hcanNetCDF']
    print(output_nlcd_cc_url)
    output_nlcd_lai_url = response_data['out_laiNetCDF']
    print(output_nlcd_lai_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
