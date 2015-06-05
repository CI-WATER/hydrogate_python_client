__author__ = 'Pabitra'
from hydrogate import HydroDS

# >>>>>> tests data services
client = HydroDS()

#client.get_token()
#client.get_upload_status()
# test function doc string print
#help(client.subset_dem)

#exit()
# test printing service log history all, first in first print
client.show_service_request_history()

# print only the first 2 items
client.show_service_request_history(count=2)

# print all items (last in print first)
client.show_service_request_history(order='last')

# print only the last 3 items
client.show_service_request_history(order='last', count=3)
#exit()

# test getting a token
# first need to login to hydrogate passing username and password.
#client.login()
#print(client.get_token())

#print(client.get_token_expire_time())
#exit()
#test subsetting a dem
#client.subset_dem(left_top_x=170000, left_top_y=4700000, right_bottom_x=570000, right_bottom_y=4100000)
#subset_dem_request = client.subset_dem(left=432760.510, top=4662453.522, right=461700.887, bottom=4612686.409)
#subset_dem_request = client.subset_dem(-112.04, 41.73, -111.5, 41.36)

#exit()

# test downloading the subset dem
# subset_dem_request = client.get_most_recent_request(service_name='subset_dem')
# if subset_dem_request:
#     # remove the '.zip' part of the url path
#     input_raster_url = subset_dem_request.file_path
#     # login to irods
#     client.login(username='username for irods REST API', password='password for irods REST API')
#     client.download_file(subset_dem_request.file_path, save_as=r'E:\Scratch\HydroGateClientDemo\nedLogan_2.tif')

#exit()

#     file_url_path = subset_dem_request.file_path[:len(subset_dem_request.file_path)-4]
#client.download_file(file_url_path, save_as=r'E:\Scratch\HydroGateClientDemo\nedLogan.tif')

# first upload the files necessary for generating watershed raster
# login to irods
client.login(username='username for irods REST API', password='password for irods REST API')
client.upload_file_irods(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan.tif')
#client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan.tif')
exit()
# file_upload_request = client.get_most_recent_request()
# if file_upload_request:
#     input_raster_url = file_upload_request.file_path
#
#client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\LoganOutlet.zip')

# file_upload_request = client.get_most_recent_request(service_name='upload_file')
# if file_upload_request:
#    outlet_shapefile_url = file_upload_request.file_path

# test generate watershed raster
# since the shapefile name needs to be always be 'LoganOutlet.shp" due error in service implementation
# I need to make this adjustment
#outlet_shapefile_url = "http://129.123.41.158:8080/dem/LoganOutlet.shp.zip"
# outlet_shapefile_url = "http://129.123.41.158:8080/dem/user8386917276039430266.shp.zip"
# client.generate_watershed_raster(input_raster_url_path=input_raster_url,
#                                   outlet_shapefile_url_path=outlet_shapefile_url,
#                                   save_as=r'E:\Scratch\HydroGateClientDemo\WS_Logan-1.tif')
#
#
# generate_watershed_raster_request = client.get_most_recent_request(service_name='generate_watershed_raster')
# if generate_watershed_raster_request:
#     ref_raster_url = generate_watershed_raster_request.file_path
#exit()

### >>>>> NEW SERVICES TESTS

##>>> Test project and clip - works
# ref_raster_url = "http://129.123.41.158:8080/dem/dem2bfecaf10e2446ac84351dcde2a01cfaWS.tif.zip"
# proj_clip_request = client.subset_NLCD_to_reference_raster(input_raster_url_path=ref_raster_url)


## >>> test get canopy variables - works
#canopy_request = client.get_canopy_variables(input_raster_url_path=proj_clip_request.file_path)

##>>> test combine rasters - works
# first upload 2 raster (nedLogan1.tif, nedLogan2.tif) to the file server
# upload_request_combine_one = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan1.tif')
# upload_request_combine_two = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan2.tif')
# combine_raster_request = client.combine_rasters(input_one_raster_url_path=upload_request_combine_one.file_path,
#                                                 input_two_raster_url_path=upload_request_combine_two.file_path)


##>>> test uncompress raster- works
#uncompress_raster_request = client.uncompress_raster(input_raster_url_path=upload_request_combine_one.file_path)

##>>> test concatenate NetCDF files - works
# first upload 2 netcd file to be concatenated
# upload_request_concatenate_one = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\prcpLog_2010.nc')
# upload_request_concatenate_two = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\prcpLog_2011.nc')

# concatenate_request = client.concatenate_netcdf(input_one_netcdf_url_path=upload_request_concatenate_one.file_path,
#                                                 input_two_netcdf_url_path=upload_request_concatenate_two.file_path)


##>>> test combine netcdf spatially - works
# first upload 2 netcdf files
# upload_request_combine_netcdf_one = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\prcp_11915.nc')
# upload_request_combine_netcdf_two = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\prcp_11735.nc')
#
# combine_netcdf_request = client.combine_netcdf(input_one_netcdf_url_path=upload_request_combine_netcdf_one.file_path,
#                                                input_two_netcdf_url_path=upload_request_combine_netcdf_two.file_path)

##>>> test subset netcdf spatially - not working yet due to file upload of large file (prcp_2010.nc)
# upload 2 netcdf files
#upload_request_subset_netcdf_reference = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogProj.tif')

# TODO: THIS ONE FAILS - may be the parameters are not right - check with Ahmet
upload_request_subset_netcdf_inputnc = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\prcp_2010.nc')
upload_request_subset_netcdf_refraster = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLog_lcc.tif')
subset_netcdf_request = client.subset_netcdf(input_netcdf_url_path=upload_request_subset_netcdf_inputnc.file_path,
                                             ref_raster_url_path=upload_request_subset_netcdf_refraster.file_path)

exit()
##>>> test create outlet shapefile - this one works
outlet_shapefile_request = client.create_outlet_shapefile(point_x=-111.576, point_y=41.829)

##>>> test project raster to NAD83 - this one seems to work
upload_request_for_project_raster = client.upload_file(file_to_upload=r'E:\Scratch\HydroGateClientDemo\nedLogan1.tif')
project_raster_request = client.project_raster_to_UTM_NAD83(input_raster_url_path=upload_request_for_project_raster.file_path, utm=12)


##>>> test project shapefile to NAD83
project_shapefile_request = client.project_shapefile_to_UTM_NAD83(input_shapefile_url_path=outlet_shapefile_request.file_path, utm=12)

##>>> Test watershed delineation
delineation_request = client.delineate_watershed(input_raster_url_path=project_raster_request.file_path,
                                                 input_shapefile_url_path=outlet_shapefile_request.file_path, utm=12,
                                                 threshold=6000)

exit()


## >>>> END OF NEW SERVICES TESTS

# test raster subsetting
input_raster_url = "http://129.123.41.158:8080/dem/nedLogan.tif.zip"
#ref_raster_url = "http://129.123.41.158:8080/dem/dem5d9cbf03f1ef4061bbaa6cae1b568656WS.tif.zip"
client.subset_raster(input_raster_url_path=input_raster_url, ref_raster_url_path=ref_raster_url, save_as=r'E:\Scratch\HydroGateClientDemo\subset_raster.tif')
raster_subset_request = client.get_most_recent_request()

# test raster to netcdf conversion
client.raster_to_netcdf(input_raster_url_path=ref_raster_url, save_as=r'E:\Scratch\HydroGateClientDemo\Ws_logan.nc')

raster_to_netcdf_request = client.get_most_recent_request(service_name='raster_to_netcdf')
if raster_to_netcdf_request:
    netcdf_file_url = raster_to_netcdf_request.file_path


# test generating a raster slope file
raster_subset_request = client.get_most_recent_request(service_name='subset_raster')
subset_raster_url = raster_subset_request.file_path

client.raster_slope(input_raster_url_path=subset_raster_url, save_as=r'E:\Scratch\HydroGateClientDemo\slope_logan.tif')

raster_slope_request = client.get_most_recent_request(service_name='raster_slope')
if raster_slope_request:
    raster_slope_url = raster_slope_request.file_path

# test generating a raster aspect file
client.raster_aspect(input_raster_url_path=subset_raster_url, save_as=r'E:\Scratch\HydroGateClientDemo\aspect_logan.tif')

raster_aspect_request = client.get_most_recent_request(service_name='raster_aspect')
if raster_aspect_request:
    raster_aspect_url = raster_aspect_request.file_path

exit()

# test uploading file to HPC for pitremove processing
# if subset_dem_request:
#     client.upload_package(subset_dem_request.file_path)
#     client.get_upload_status()
# else:
#     print("Error")
# test downloading the subset dem
#client.download_file('http://129.123.41.158:8080/dem/dem8667489440153154896.tif', save_as='C:\Users\Pabitra\Downloads\sub_dem_1.tif')

# save_to = r'C:\Users\Pabitra\Downloads\sub_dem_2.tif'
# client.subset_dem(left_top_x=170000, left_top_y=4700000, right_bottom_x=570000, right_bottom_y=4100000, save_as=save_to)

client.get_upload_status()

upload_status_request = client.get_most_recent_request()
if upload_status_request:
    if upload_status_request.service_status == "PackageTransferDone":
        client.submit_job(package_id=upload_status_request.service_id_value, program_name='pitremove')
else:
    print("Error")
    
submit_job_request = client.get_most_recent_request(service_name='submit_job')
if submit_job_request:
    client.get_job_status(job_id=submit_job_request.service_id_value)

job_status_request = client.get_most_recent_request(service_name='retrieve_job_status')
if job_status_request:
    if job_status_request.service_status == 'JobOutputFileTransferDone':
        client.download_file(file_url_path=submit_job_request.file_path, save_as=r'C:\Users\Pabitra\Downloads\pitremove_1.zip')
    else:
        print "Output file is not yet available for download."

client.save_service_call_history()

print 'done'

