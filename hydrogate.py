__author__ = 'Pabitra'

""""
HydroGate Python Client (hpc) for accessing CI-WATER Data and Computational Web Services
"""
import requests
import os
import json
import pickle
import datetime

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Client(object):
    def __init__(self, base_url='https://hydrogate.uwrl.usu.edu/hydrogate', username=None, password=None, hpc=None):
        self.base_url = base_url
        if self.base_url.endswith('/'):
            self.base_url = self.base_url.strip('/')

        self.dataserver_base_url = 'http://129.123.41.158:8080' #http://ckan-fileserver.uwrl.usu.edu
        self.token_url = self.base_url + '/request_token/'
        self.upload_pkg_url = self.base_url + '/upload_package/'
        self.upload_pkg_status_url = self.base_url + '/retrieve_package_status'
        self.submit_job_url = self.base_url + '/submit_job/'
        self.job_status_url = self.base_url + '/retrieve_job_status'
        self.token_expire_time_url = self.base_url + '/retrieve_token_expire_time'
        self.hpc_program_names_url = self.base_url + '/return_hpc_program_names/'
        self.program_info_url = self.base_url + '/retrieve_program_info'
        self.username = username
        self.password = password
        self.requests = requests
        if self.username and self.password:
            self.requests.auth.HTTPBasicAuth(self.username, self.password)
            self.user_authenticated = True
        else:
            self.user_authenticated = False

        self.token = None
        if not hpc:
            self.default_hpc = 'HydrogateHPC' #'MountMoran'
        else:
            self.default_hpc = hpc

        _ServiceLog.load()

    def login(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.user_authenticated = False
        try:
            self.get_token()
            self.requests.auth.HTTPBasicAuth(self.username, self.password)
            self.user_authenticated = True
            print("Login successful.")
        except:
            print("Login failed.")

    def get_available_hpc(self):
        # returns a list of hpc resource names
        pass

    def set_default_hpc(self, hpc):
        available_hpc = self.get_available_hpc()
        if hpc in available_hpc:
            self.default_hpc = hpc
        else:
            raise Exception("Invalid hpc resource.")

    def get_available_programs(self, hpc=None):
        # returns a list of installed program names that are installed on a specified hpc resource
        if not self.token:
            self.get_token()
        else:
            if self.get_token_expire_time() == 0:
                self.get_token()

        if not hpc:
            hpc = self.default_hpc

        request_data = {'token': self.token, 'hpc': hpc}
        response = self.requests.post(self.hpc_program_names_url, data=request_data, verify=False)

        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)

        if response_dict['status'] == 'success':
            return response_dict['programnames']
        else:
            raise Exception('Error %s' % response_dict['description'])

    def get_program_info(self, program_name):
        # returns information about specific program/application
        if not self.token:
            self.get_token()
        else:
            if self.get_token_expire_time() == 0:
                self.get_token()

        request_data = {'token': self.token, 'program': program_name}
        response = self.requests.get(self.program_info_url, params=request_data, verify=False)

        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['status'] == 'success':
            return response_dict
        else:
            raise Exception('Error %s' % response_dict['description'])

    def get_token(self):
        if self.token:
            return self.token

        if not self.user_authenticated:
            print("You need login first.")
            return

        user_data = {'username': self.username, 'password': self.password}
        response = self.requests.post(self.token_url, data=user_data, verify=False)
        if response.status_code != requests.codes.ok:
            raise Exception("HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['status'] == 'success':
            self.token = response_dict['token']
            return self.token
        else:
            raise Exception('Error:%s' % response_dict['description'])

    def get_token_expire_time(self):
        # returns token expire time in seconds (0 means token has expired)
        if not self.token:
            return 0

        request_data = {'token': self.token}
        response = self.requests.get(self.token_expire_time_url, params=request_data, verify=False)

        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['status'] == 'success':
            return response_dict['remainingexpiretime']
        else:
            raise Exception('Error %s' % response_dict['description'])

    def show_service_request_history(self, order='first', count=None):
        _ServiceLog.print_log(order=order, count=count)

    def get_most_recent_request(self, service_name=None, service_id_name=None, service_id_value=None):
        last_request = _ServiceLog.get_most_recent_request(service_name, service_id_name, service_id_value)
        if last_request:
            print last_request.to_json()
        else:
            print ("No matching request was found.")

        return last_request

    def upload_package(self, package_file_url_path):
        if not self.token:
            self.get_token()
        else:
            if self.get_token_expire_time() == 0:
                self.get_token()

        # location of the file to be uploaded (must be a url file path).
        request_data = {'token': self.token, 'package': package_file_url_path, 'hpc': self.default_hpc}
        response = self.requests.post(self.upload_pkg_url, data=request_data, verify=False)

        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)

        if response_dict['status'] == 'success':
            package_id = response_dict['packageid']
            service_req = ServiceRequest(service_name='upload_package', service_id_name='packageID',
                                         service_id_value=package_id, service_status='success')
            _ServiceLog.add(service_req)
            self.save_service_call_history()
            print("Package upload request successful. Package ID:%s" % package_id)
            #print json.dumps(response.content, indent=4)
            print(service_req.to_json())
            return service_req
        else:
            raise Exception('Error:%s' % response_dict['description'])

    def get_upload_status(self, package_id=None):
        if not package_id:
            # TODO: get the most recent service request object that has a package id
            last_request = _ServiceLog.get_most_recent_request(service_id_name='packageID')
            if not last_request:
                print("No package upload request has been made yet to check status.")
                return None
            else:
                package_id = last_request.service_id_value

        if not self.token:
            self.get_token()
        else:
            if self.get_token_expire_time() == 0:
                self.get_token()

        request_data = {'token': self.token, 'packageid': int(package_id)}
        response = self.requests.get(self.upload_pkg_status_url, params=request_data, verify=False)
        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['status'] == 'success':
            upload_status = response_dict['state']
            service_req = ServiceRequest(service_name='retrieve_package_upload_status', service_id_name='packageID',
                                         service_id_value=package_id, service_status=upload_status)
            _ServiceLog.add(service_req)
            self.save_service_call_history()
            print(service_req.to_json())
            return upload_status
        else:
            raise Exception('Error:' + response_dict['description'])

    def submit_job(self, package_id, program_name, **kwargs):
        # TODO: check that the user provided program_name is one of the supported programs using the get_available_programs()

        if self.get_token_expire_time() == 0:
            self.get_token()

        job_def = {}
        if len(kwargs) > 0:
            job_def = kwargs
        else:
            if program_name == 'pitremove':
                job_def['program'] = 'pitremove'
                job_def['walltime'] = '00:00:50'
                job_def['outputlist'] = ['fel*.tif']
            else:
                raise Exception("Program parameters are missing for '%s'." % program_name)

        request_data = {'token': self.token, 'packageid': int(package_id), 'jobdefinition': json.dumps(job_def)}
        response = self.requests.post(self.submit_job_url, data=request_data, verify=False)
        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['status'] == 'success':
            job_id = response_dict['jobid']
            output_file_path = response_dict['outputpath']
            service_req = ServiceRequest(service_name='submit_job', service_id_name='jobID',
                                         service_id_value=job_id, service_status='success', file_path=output_file_path)
            _ServiceLog.add(service_req)
            print("Job submission successful.")
            self.save_service_call_history()
            #print json.dumps(response.content, indent=4)
            print(service_req.to_json())
            return service_req
        else:
            raise Exception('Error:%s' % response_dict['description'])

    def get_job_status(self, job_id):
        if self.get_token_expire_time() == 0:
            self.get_token()

        request_data = {'token': self.token, 'jobid': job_id}
        response = self.requests.get(self.job_status_url, params=request_data, verify=False)
        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['status'] == 'success':
            job_status = response_dict['state']
            service_req = ServiceRequest(service_name='retrieve_job_status', service_id_name='jobID',
                                         service_id_value=job_id, service_status=job_status)
            _ServiceLog.add(service_req)
            self.save_service_call_history()
            print("Job status for job ID:%s is %s." % (job_id, job_status))
            print(service_req.to_json())
            return job_status
        else:
            raise Exception('Error:%s' % response_dict['description'])

    def subset_dem(self, left, top, right, bottom, save_as=None):
        """
        Subsets a dem (dem tif file on the file server) and creates a new tif file with the subset data
        :param left: x-coordinate of the left-top corner of the bounding box
        :param top: y-coordinate of the left-top corner of the bounding box
        :param right: x-coordinate of the right-bottom corner of the bounding box
        :param bottom: y-coordinate of the right-bottom corner of the bounding box
        :param save_as: (optional) subset dem tif file to save as (file name with path)
        :return: an object of type ServiceRequest
        """

        url = 'http://129.123.41.158:8080/subsetdem'
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        payload = {'bbox': str(left) + ' ' + str(top) + ' ' + str(right) + ' ' + str(bottom)}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, 'subset_dem', save_as)

    def generate_watershed_raster(self, input_raster_url_path, outlet_shapefile_url_path, save_as=None):

        if save_as:
            if not self._validate_file_save_as(save_as):
                return

            # file_name = os.path.basename(save_as)
                # if not self._validate_file_name(file_name):
                #     print("Error: Invalid file name specified (%s)." % file_name)
                #     return

        url = self.dataserver_base_url + '/generatewatershedraster'
        # you need to only send the file name part from the actual url path and we are removing the .zip from the file name
        # given the file url path: "http://129.123.41.158:8080/dem/user2623623514710145932.txt.zip"
        # we will be passing: user2623623514710145932.txt
        # input_raster = input_raster.split("/")[-1][:-4]
        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        outlet_shapefile_name = self._get_file_name_from_url_file_path(outlet_shapefile_url_path)
        payload = {"raster": input_raster_name, 'outletshp': outlet_shapefile_name}

        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, 'generate_watershed_raster', save_as)

    def subset_raster(self, input_raster_url_path, ref_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        ref_raster_name = self._get_file_name_from_url_file_path(ref_raster_url_path)
        url = self.dataserver_base_url + '/rastersubset'
        payload = {"raster": input_raster_name, 'refraster': ref_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "subset_raster", save_as)

    def raster_to_netcdf(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        # Example: http://129.123.41.158:8080/rastertonetcdf?raster=demc8261d8ac7194149a3a9492bcf7f4024WS.tif

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        url = self.dataserver_base_url + '/rastertonetcdf'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "raster_to_netcdf", save_as)

    def raster_slope(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        url = self.dataserver_base_url + '/rasterslope'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "raster_slope", save_as)

    def raster_aspect(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        url = self.dataserver_base_url + '/rasteraspect'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "raster_aspect", save_as)

    def subset_NLCD_to_reference_raster(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)

        # Example: http://129.123.41.158:8080/projectandclipraster?raster=nedLogan.tif

        url = self.dataserver_base_url + '/projectandclipraster'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "subset_NLCD_to_reference_raster", save_as)

    def get_canopy_variables(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        #URL: http://129.123.41.158:8080/getcanopyvars?raster=dem701375934759328561234.tif
        url = self.dataserver_base_url + '/getcanopyvars'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "get_canopy_variables", save_as, strip_zip=False)

    def combine_rasters(self, input_one_raster_url_path, input_two_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_one_raster_name = self._get_file_name_from_url_file_path(input_one_raster_url_path)
        input_two_raster_name = self._get_file_name_from_url_file_path(input_two_raster_url_path)

        # Example: http://129.123.41.158:8080/combinerasters?raster1=dem701375934759328561234.tif&raster2=nedLogan.tif

        url = self.dataserver_base_url + '/combinerasters'
        payload = {"raster1": input_one_raster_name, "raster2": input_two_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "combine_rasters", save_as)

    def uncompress_raster(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)

        # Example: http://129.123.41.158:8080/uncompressraster?raster=nedLogan.tif

        url = self.dataserver_base_url + '/uncompressraster'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "uncompress_raster", save_as)

    def get_daymet_mosaic(self, start_year, end_year, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        # TODO: check with Tseganeh for the valid year range (1980 -2013)
        try:
            int(start_year)
        except:
            raise Exception("Error:Invalid start year. Year must be an integer value.")

        try:
            int(end_year)
        except:
            raise Exception("Error:Invalid end year. Year must be an integer value.")

        # Example: http://129.123.41.158:8080/downloaddaymetmosaic?startyear=2011&endyear=2012

        url = self.dataserver_base_url + '/downloaddaymetmosaic'

        if end_year > start_year:
            payload = {"startyear": start_year, "endyear": end_year}
        else:
            payload = {"startyear": end_year, "endyear": start_year}

        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "get_daymet_mosaic", save_as)

    def get_daymet_tile(self, start_year, end_year, start_tile, end_tile, save_as=None):
        if save_as:
            # TODO: should we check that the file extension must be  .tif type for saving
            if not self._validate_file_save_as(save_as):
                return

        # TODO: check with Tseganeh for the valid year range
        try:
            int(start_year)
        except:
            raise Exception("Error:Invalid start year. Year must be an integer value.")

        try:
            int(end_year)
        except:
            raise Exception("Error:Invalid end year. Year must be an integer value.")

        try:
            int(start_tile)
        except:
            raise Exception("Error:Invalid start tile number. Tile number must be an integer value.")

        try:
            int(end_tile)
        except:
            raise Exception("Error:Invalid end tile number. Tile number must be an integer value.")

        # Example: http://129.123.41.158:8080/downloaddaymettile?startyear=2011&endyear=2012&starttile=11715&endtile=11716

        url = self.dataserver_base_url + '/downloaddaymettile'

        if end_year > start_year:
            payload = {"startyear": start_year, "endyear": end_year}
        else:
            payload = {"startyear": end_year, "endyear": start_year}

        payload["starttile"] = start_tile
        payload["endtile"] = end_tile
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "get_daymet_tile", save_as)

    def concatenate_netcdf(self, input_one_netcdf_url_path, input_two_netcdf_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_one_netcdf_name = self._get_file_name_from_url_file_path(input_one_netcdf_url_path)
        input_two_netcdf_name = self._get_file_name_from_url_file_path(input_two_netcdf_url_path)
        #URL: http://129.123.41.158:8080/concatenatenetcdf?inputnc1=prcpLog_2010.nc&inputnc2=prcpLog_2011.nc
        url = self.dataserver_base_url + '/concatenatenetcdf'
        payload = {"inputnc1": input_one_netcdf_name, "inputnc2": input_two_netcdf_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "concatenate_netcdf", save_as)

    def combine_netcdf(self, input_one_netcdf_url_path, input_two_netcdf_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_one_netcdf_name = self._get_file_name_from_url_file_path(input_one_netcdf_url_path)
        input_two_netcdf_name = self._get_file_name_from_url_file_path(input_two_netcdf_url_path)

        # Example: http://129.123.41.158:8080/combinenetcdf?inputnc1=netcdf24685a2f0387402dabf46bf7b56abdcb.nc&inputnc2=netcdffd9a5b6f7d634d1cbd5325b98899b073.nc

        url = self.dataserver_base_url + '/combinenetcdf'
        payload = {"inputnc1": input_one_netcdf_name, "inputnc2": input_two_netcdf_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "combine_netcdf", save_as)

    def subset_netcdf(self, input_netcdf_url_path, ref_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_netcdf_name = self._get_file_name_from_url_file_path(input_netcdf_url_path)
        ref_raster_name = self._get_file_name_from_url_file_path(ref_raster_url_path)

        # URL: http://129.123.41.158:8080/getnetcdfsubset?inputnc=prcpSpawnProj_2010.nc&referencenc=SpawnProj.tif

        url = self.dataserver_base_url + '/getnetcdfsubset'
        payload = {"inputnc": input_netcdf_name, 'referencenc': ref_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "subset_netcdf", save_as)

    def project_raster_to_UTM_NAD83(self, input_raster_url_path, utm, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)

        # URL: http://129.123.41.158:8080/projectrasterutmnad83?raster=Spawn.tif&utm=12

        url = self.dataserver_base_url + '/projectrasterutmnad83'
        payload = {"raster": input_raster_name, 'utm': utm}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "project_raster_to_UTM_NAD83", save_as)

    def project_shapefile_to_UTM_NAD83(self, input_shapefile_url_path, utm, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_shapefile_name = self._get_file_name_from_url_file_path(input_shapefile_url_path)

        # URL: http://129.123.41.158:8080/projectshapefileutmnad83?shp=SpawnOutlet.shp&utm=12

        url = self.dataserver_base_url + '/projectshapefileutmnad83'
        payload = {"shp": input_shapefile_name, 'utm': utm}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "project_shapefile_to_UTM_NAD83", save_as)

    def create_outlet_shapefile(self, point_x, point_y, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        # URL: http://129.123.41.158:8080/createoutletshp?outletpointx=-111.576&outletpointy=41.829

        url = self.dataserver_base_url + '/createoutletshp'
        payload = {"outletpointx": point_x, 'outletpointy': point_y}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "create_outlet_shapefile", save_as)

    def delineate_watershed(self, input_raster_url_path, input_shapefile_url_path, utm, threshold, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        input_shapefile_name = self._get_file_name_from_url_file_path(input_shapefile_url_path)

        # URL: http://129.123.41.158:8080/delineatewatershed?raster=SpawnProj.tif&shp=shapee1aa4cdbc0f24fc8b282b738b6b577f7.shp&utm=12&threshold=600

        url = self.dataserver_base_url + '/delineatewatershed'
        payload = {"raster": input_raster_name, 'shp': input_shapefile_name, 'utm': utm, 'threshold': threshold}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "delineate_watershed", save_as)

    def upload_file(self, file_to_upload):
        import urllib2
        if not os.path.isfile(file_to_upload):
            raise Exception("Error: Specified file to upload (%s) does not exist." % file_to_upload)
            return

        url = self.dataserver_base_url + '/uploader'
        #upload_file_obj = open(file_to_upload, 'rb')
        #upload_file_obj = {'file': open(file_to_upload, 'rb')}
        with open(file_to_upload, 'rb') as upload_file_obj:
            response = self.requests.put(url, files={'file': upload_file_obj})

        # file_size = os.path.getsize(file_to_upload)
        # headers = {'content-type': 'application/octet-stream'}
        # with open(file_to_upload, 'rb') as upload_file_obj:
        #     response = self.requests.put(url, data=upload_file_obj.read(), params={'file': os.path.basename(file_to_upload)}, headers=headers)
        #response = self.requests.put(url, data=upload_file_obj, headers=headers)

        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['ret'] == 'success':
            uploaded_file_url = response_dict['url']
            print ("File upload was successful.")
            print("Uploaded file URL path:%s" % uploaded_file_url)
            service_req = ServiceRequest(service_name='upload_file', service_id_name='',
                                         service_id_value='', service_status='success', file_path=uploaded_file_url)
            _ServiceLog.add(service_req)
            self.save_service_call_history()
            print(service_req.to_json())
            return service_req
        else:
            self._raise_service_error(response_dict['message'])

    def download_file(self, file_url_path, save_as):
        if not self._validate_file_save_as(save_as):
            return

        with open(save_as, 'wb') as file_obj:
            response = requests.get(file_url_path, stream=True)

            if not response.ok:
                # Something went wrong
                raise Exception("Error: Error in downloading the file.")

            for block in response.iter_content(1024):
                if not block:
                    break
                file_obj.write(block)

        service_req = ServiceRequest(service_name='download_file', service_id_name='',
                                     service_id_value='', service_status='success', file_path=save_as)
        _ServiceLog.add(service_req)
        self.save_service_call_history()
        print("Downloaded file saved successfully at:%s" % save_as)
        print(service_req.to_json())
        return service_req

    def _process_service_response(self, response, service_name, save_as=None, strip_zip=True):
        if response.status_code != requests.codes.ok:
            raise Exception("Error: HydroGate connection error.")

        response_dict = json.loads(response.content)
        if response_dict['ret'] == 'success':
            file_url = response_dict['message']
            print("%s execution was successful.\n" % service_name)
            print("Output file URL path:%s\n" % file_url)
            service_req = ServiceRequest(service_name=service_name, service_id_name='',
                                         service_id_value='', service_status='success', file_path=file_url)

            _ServiceLog.add(service_req)
            self.save_service_call_history()
            if save_as:
                # get rid of the .zip part of the url
                if strip_zip:
                    file_url = file_url[:-4]
                self.download_file(file_url, save_as)

            print(service_req.to_json())
            return service_req
        else:
            self._raise_service_error(response_dict['message'])

    def _raise_service_error(self, message):
        raise Exception("Error:%s" % message)

    def save_service_call_history(self):
        _ServiceLog.save()

    def clear_service_log(self):
        _ServiceLog.delete_all()
        print ("Service call history deleted.")

    def _validate_file_name(self, file_name):
        try:
            name_part, ext_part = os.path.splitext(file_name)
            if len(name_part) == 0 or len(ext_part) < 2:
                return False

            ext_part = ext_part[1:]
            for c in ext_part:
                if not c.isalpha():
                    return False
            if not name_part[0].isalpha():
                return False
            for c in name_part[1:]:
                if not c.isalnum() and c not in ['-', '_']:
                    return False
        except:
            return False
        return True

    def _validate_file_save_as(self, save_as, file_ext=None):
        save_file_dir = os.path.dirname(save_as)
        if not os.path.exists(save_file_dir):
            raise Exception("Error: Specified save to file path (%s) does not exist." % save_file_dir)
            return False

        file_name = os.path.basename(save_as)
        if not self._validate_file_name(file_name):
            raise Exception("Error: Invalid file name (%s)." % file_name)
            return False

        if file_ext:
            file_extension = os.path.splitext(save_as)[1]
            if file_extension != file_ext:
                raise Exception("Error: Invalid save file type:%s. File type must be:%s " % (file_extension, file_ext))
                return False

        return True


    def _get_file_name_from_url_file_path(self, url_file_path):
        # given the file url path: "http://129.123.41.158:8080/dem/user2623623514710145932.txt.zip"
        # we will be returning: user2623623514710145932.txt
        file_name = url_file_path.split("/")[-1][:-4]
        return file_name


class _ServiceLog(object):
    _service_requests = []
    _pickle_file_name = r'hg_service_log.pkl'

    @classmethod
    def add(cls, service_request):
        if isinstance(service_request, ServiceRequest):
            cls._service_requests.append(service_request)
        else:
            raise Exception("Internal Error: Only an object of type 'ServiceRequest' can be added to the log.")

    @classmethod
    def remove(cls):
        pass

    @classmethod
    def delete_all(cls):
        cls._service_requests = []
        if os.path.isfile(cls._pickle_file_name):
            os.remove(cls._pickle_file_name)

    @classmethod
    def load(cls):
        if len(cls._service_requests) == 0:
            if os.path.isfile(cls._pickle_file_name):
                with open(cls._pickle_file_name, "rb") as f:
                    cls._service_requests = pickle.load(f)

    @classmethod
    def save(cls):
        if len(cls._service_requests) > 0:
            with open(cls._pickle_file_name, "wb") as f:
                pickle.dump(cls._service_requests, f)
        elif os.path.isfile(cls._pickle_file_name):
            os.remove(cls._pickle_file_name)

    @classmethod
    def print_log(cls, order='first', count=None):
        if len(cls._service_requests) == 0:
            print ("There are no service requests to display.")
            return

        if order == 'last':
            # reverse all items in the list
            service_requests = cls._service_requests[::-1]
        else:
            service_requests = cls._service_requests

        if count:
            try:
                count = int(count)
            except:
                raise ValueError("Count must be an integer value.")
            if count > len(cls._service_requests):
                count = len(cls._service_requests)
        else:
            count = len(cls._service_requests)

        service_requests = service_requests[0:count]
        for req in service_requests:
            print req.to_json()

    @classmethod
    def get_most_recent_request(cls, service_name=None, service_id_name=None, service_id_value=None):
        if len(cls._service_requests) == 0:
            return None

        if not service_name and not service_id_name:
            return cls._service_requests[-1]
        else:
            reversed_list = reversed(cls._service_requests)
            for item in reversed_list:
                selected_item = None
                if service_name:
                    if item.service_name == service_name:
                       selected_item = item
                if service_id_name:
                    if item.service_id_name == service_id_name:
                        if service_id_value:
                            if item.service_id_value == service_id_value:
                                selected_item = item
                            else:
                                selected_item = None
                        else:
                            selected_item = item
                    else:
                        selected_item = None

                if selected_item:
                    return selected_item

            return None


class ServiceRequest(object):
    def __init__(self, service_name, service_id_name, service_id_value, service_status, file_path=None, request_time=None):
        self.service_name = service_name            # e.g. upload_package
        self.service_id_name = service_id_name      # e.g package_id
        self.service_id_value = service_id_value    # e.g. 109879ghy67890
        self.service_status = service_status        # e.g. uploading
        self.file_path = file_path
        if request_time:
            self.request_time = request_time        # e.g. 10/6/2014 10:00:05
        else:
            self.request_time = datetime.datetime.now()

    def to_json(self):
        object_data = {}
        object_data['Service name'] = self.service_name
        object_data['Service ID name'] = self.service_id_name
        object_data['Service ID value'] = self.service_id_value
        object_data['Service status'] = self.service_status
        object_data['Output file path'] = self.file_path
        object_data['Request time'] = str(self.request_time)
        return json.dumps(object_data, indent=4)