__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

input_NLCD_raster_url_path = 'http://129.123.41.184:20199/files/data/user_2/nlcd_proj_spwan.tif'
try:
    # output netcdf parameters are optional
    response_data = client.get_canopy_variables(input_NLCD_raster_url_path=input_NLCD_raster_url_path,
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
