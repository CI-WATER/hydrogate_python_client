from hydrogate import Client
#import watershedFunctions

"""
THIS CODE IS OBSOLETE AS IT IS USING THE OLD JAVA BASED WEB SERVICES
"""

client = Client()

workingDir = "E:/Scratch/HydroGateClientDemo/"
#get approximate watereshed boundary in geographic coordinates left, top, right, bottom
#-112.04 41.73 -111.5 41.36
#get approximate lat lon coordinates for the watershed outlets
# 41.726 -111. 953
subsetDEM_request = client.subset_dem(-112.04, 41.73, -111.5, 41.36)
projectDEM_request = client.project_raster_to_UTM_NAD83(input_raster_url_path=subsetDEM_request.file_path, utm=12)
outlet_shapefile_request = client.create_outlet_shapefile(point_x=-111.953, point_y=41.726)
projectShp_request = client.project_shapefile_to_UTM_NAD83(outlet_shapefile_request.file_path, 12)
#not implemented local function used instead
#resamleDEM_request = client.resample_raster(projectDEM_request.file_path,120,120)
uploadWSfile = workingDir + "LBres120.tif"
#watershedFunctions.resample_Raster(wsFileLocal,uploadWSfile,120,120,'bilinear')
resampleDEM_request = client.upload_file(uploadWSfile)
watershedFile = workingDir + 'LittleBearWS.nc'
delineation_request = client.delineate_watershed(resampleDEM_request.file_path,
                                                 projectShp_request.file_path, 12,8000)
watershed_file_path = delineation_request.file_path
rastertoNC_request = client.raster_to_netcdf(delineation_request.file_path, save_as=watershedFile)
aspectFile = workingDir+'LBApspect.nc'
computeAspect_request = client.raster_aspect(resampleDEM_request.file_path)
rastertoNC_request = client.raster_to_netcdf(computeAspect_request.file_path, save_as=aspectFile)
slopeFile = workingDir+'LBApspect.nc'
computeSlope_request = client.raster_slope(resampleDEM_request.file_path)
rastertoNC_request = client.raster_to_netcdf(computeSlope_request.file_path, save_as=slopeFile)
subsetNLCD_request = client.subset_NLCD_to_reference_raster(delineation_request.file_path)
canopy_var_file = workingDir + 'canopy.zip'
getCanopyVars_reqest = client.get_canopy_variables(subsetNLCD_request.file_path, save_as=canopy_var_file)

#model start and end datetime
startYear = 2010
endYear = 2011
simStartTimeindex = 270
simEndTimeindex = 545
#iterate through climate variables
climate_Vars = ['vp', 'tmin', 'tmax', 'srad', 'prcp']
for var in climate_Vars:
    climateFile1 = var+"_"+str(startYear)+".nc4"
    climateFile2 = var+"_"+str(endYear)+".nc4"
    #ni
    Year1sub_request = client.subset_netcdf_to_referenceRaster(climateFile1,watershed_file_path)
    Year2sub_request = client.subset_netcdf_to_referenceRaster(climateFile2,watershed_file_path)

    concateNC_request = client.concatenate_netcdf(Year1sub_request.file_path,Year2sub_request.file_path)
    #ni
    timesubNc_request = client.get_netcdf_subset_timeDim(concateNC_request.file_path,'time',
                                                         simStartTimeindex,simEndTimeindex)
    climatefileComp = workingDir+var+"_wy"+str(endYear)+".nc"
    ncProj_request = client.project_netcdf_UTM_NAD83(timesubNc_request.file_path,var,12,save_as=climatefileComp)

#prepare model setup files for UEB to run

#upload ueb model package to hydrogate, first put them all in a zip file
ueb_package_file = workingDir + "uebLittleBear.zip"
upload_request = client.upload_file(ueb_package_file)
uploadtoHPC_request = client.upload_package(upload_request.file_path)

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

