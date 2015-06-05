__author__ = 'Pabitra'

from hydrogate import HydroDS
import settings

hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

# NOTE: this file path is valid for user with id 2
ref_input_raster_url = 'http://hydro-ds-uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
input_raster = 'nlcd2011CONUS.tif'  # this a static data file on the api server

try:
    # param: output_raster is optional
    response_data = hds.project_clip_raster(input_raster=input_raster, ref_raster_url_path=ref_input_raster_url,
                                            output_raster='nlcd_proj_spwan.tif')
    output_raster_url = response_data['output_raster']
    print(output_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()