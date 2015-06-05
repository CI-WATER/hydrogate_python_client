__author__ = 'Pabitra'

from hydrogate import Client
import settings

client = Client(username=settings.USER_NAME, password=settings.PASSWORD)

# run the subset dem to get the output raster to be used as an input for creating the slope raster
response_data = client.subset_dem(left=-111.97, top=42.11, right=-111.35, bottom=41.66)
output_subset_dem_url = response_data['output_raster']

try:
    # param: output_raster is optional
    response_data = client.create_raster_slope(input_raster_url_path=output_subset_dem_url,
                                               output_raster='slope_logan.tif')
    output_slope_raster_url = response_data['output_raster']
    print(output_slope_raster_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE..."
exit()
