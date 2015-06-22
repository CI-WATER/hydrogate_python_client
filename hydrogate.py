__author__ = 'Pabitra'

""""
HydroGate Python Client for accessing CI-WATER Data and Computational Web Services
"""
import requests
import os
import json
import pickle
import datetime

# TODO: create a custom Exception class
class HydroDSException(Exception):
    pass

class HydroDSArgumentException(Exception):
    pass

class HydroDSServerException(Exception):
    pass

class HydroDSBadRequestException(Exception):
    pass

class HydroDSNotAuthorizedException(Exception):
    pass

class HydroDSNotAuthenticatedException(Exception):
    pass

class HydroDSNotFoundException(Exception):
    pass

def singleton(cls):
    instances = {}

    def getinstance(base_url='https://hydrogate.uwrl.usu.edu/hydrogate', username=None, password=None, hpc=None):
        if cls not in instances:
            instances[cls] = cls(base_url, username, password, hpc)
        return instances[cls]
    return getinstance


@singleton
class HydroDS(object):
    def __init__(self, base_url='https://hydrogate.uwrl.usu.edu/hydrogate', username=None, password=None, hpc=None):
        self.base_url = base_url
        if self.base_url.endswith('/'):
            self.base_url = self.base_url.strip('/')

        self.hydrogate_base_url = 'https://129.123.41.158/hydrogate'    #http://ckan-fileserver.uwrl.usu.edu/hydrogate
        self.dataservice_base_url = 'http://hydro-ds.uwrl.usu.edu:20199/api/dataservice'
        self.irods_rest_base_url = 'http://hydro-ds.uwrl.usu.edu:8080/irods-rest-4.0.2.1-SNAPSHOT/rest'
        self.token_url = self.hydrogate_base_url + '/request_token/'
        self.upload_pkg_url = self.hydrogate_base_url + '/upload_package/'
        self.upload_pkg_status_url = self.hydrogate_base_url + '/retrieve_package_status'
        self.submit_job_url = self.hydrogate_base_url + '/submit_job/'
        self.job_status_url = self.hydrogate_base_url + '/retrieve_job_status'
        self.token_expire_time_url = self.hydrogate_base_url + '/retrieve_token_expire_time'
        self.hpc_program_names_url = self.hydrogate_base_url + '/return_hpc_program_names/'
        self.program_info_url = self.hydrogate_base_url + '/retrieve_program_info'
        self.username = username
        self.password = password
        self.requests = requests
        self.authorization = (username, password)
        # if self.username and self.password:
        #     self.requests.auth.HTTPBasicAuth(self.username, self.password)
        #     self.user_authenticated = True
        # else:
        #     self.user_authenticated = False

        self.token = None
        if not hpc:
            self.default_hpc = 'USU' #'MountMoran'
        else:
            self.default_hpc = hpc

        _ServiceLog.load()

    def check_irods_server_status(self):
        url = '/server'
        # headers = {'content-type': 'application/json'}
        # response_format = {'contentType': 'application/json'}
        # response = self.requests.get(url, params=response_format, headers=headers, auth=(self.username, self.password))
        response = self._make_irods_rest_call(url)
        if response.status_code != requests.codes.ok:
            raise Exception("Error: iRODS server connection error." + response.reason)

        print response.content

    def get_irods_collections(self, listing=False):
        url ='/collection//usu/home/rods'
        if listing:
            url += '?listing=true'

        response = self._make_irods_rest_call(url)
        if response.status_code != requests.codes.ok:
            raise Exception("Error:" + response.reason)

        print response.content

    def _make_irods_rest_call(self, url):
        url = self.irods_rest_base_url + url
        headers = {'content-type': 'application/json'}
        response_format = {'contentType': 'application/json'}
        response = self.requests.get(url, params=response_format, headers=headers, auth=(self.irods_username, self.irods_password))
        return response

    def login(self, username=None, password=None, hpc_username=None, hpc_password=None, hpc='USU'):
        self.irods_username = username
        self.irods_password = password
        if hpc_username and not hpc_password:
            raise Exception("Failed to login. Password for hpc system is missing.")

        if not hpc_username and hpc_password:
            raise Exception("Failed to login. Username for hpc system is missing.")

        if hpc_username and hpc_password:
            self.token = None
            self.user_hpc_authenticated = False
            try:
                self.get_token()
                self.requests.auth.HTTPBasicAuth(self.username, self.password)
                self.user_hpc_authenticated = True
                print("Login successful.")
            except:
                print("Login failed.")

    def authenticate_user(self, username, password, hpc=None):
        if hpc:
            if hpc in self.get_available_hpc():
                self.token = None
                self.user_hpc_authenticated = False
                self.hpc_username = username
                self.hpc_password = password
                try:
                    self.requests.auth.HTTPBasicAuth(self.hpc_username, self.hpc_password)
                    self.get_token()
                    self.user_hpc_authenticated = True
                    self.default_hpc = hpc
                    print("User authentication for HPC successful.")
                except:
                    print("User authentication for HPC failed.")
            else:
                raise Exception("User authentication for HPC failed. Provided HPC (%s) is not supported." % hpc)
        else:
            self.irods_username = username
            self.irods_password = password
            self.user_irods_authenticated = False
            try:
                self.check_irods_server_status()
                self.user_irods_authenticated = True
                print("User authentication for iRODS is successful.")
            except:
                raise Exception ("User authentication for iRODS failed.")

    def get_available_hpc(self):
        return ('USU',)

    def set_default_hpc(self, hpc):
        available_hpc = self.get_available_hpc()
        if hpc in available_hpc:
            self.default_hpc = hpc
        else:
            raise Exception("Invalid hpc resource.")

    def get_available_programs(self, hpc=None):
        # returns a list of installed program names that are installed on a specified hpc resource
        self._check_user_hpc_authentication()
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
        self._check_user_hpc_authentication()
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

        #self._check_user_hpc_authentication()

        user_data = {'username': self.hpc_username, 'password': self.hpc_password}
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
        self._check_user_hpc_authentication()
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
        self._check_user_hpc_authentication()

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
            return service_req
        else:
            raise Exception('Error:' + response_dict['description'])

    def submit_job(self, package_id, program_name, input_raster_file_name, **kwargs):
       # TODO: check that the user provided program_name is one of the supported programs using the get_available_programs()
        self._check_user_hpc_authentication()

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
                job_def['parameters'] = {'z': input_raster_file_name, 'fel': 'feloutput.tif'}
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
        self._check_user_hpc_authentication()

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

    def list_my_files(self):
        """
        Lists url file paths for all the files the user owns

        :return: List of url file paths

        :raises: HydroDSNotAuthenticatedException: provided user account failed validation

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.list_my_file()
            # print url file path all the files user owns
            for file_url in response_data:
                print(file_url)
        """

        url = self._get_dataservice_specific_url('myfiles/list')
        response = self._make_data_service_request(url=url)
        return self._process_dataservice_response(response, save_as=None)

    def delete_my_file(self, file_name):
        """
        Deletes a user file on the server
        :param file_name: name of the file to be deleted from the HydroDS ap server
        :return: name of the file that got deleted

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified file to be deleted does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.delete_my_file(file_name=logan.tif)

            # print name of the file that got deleted
            print(hds_response_data)
        """
        if not self._validate_file_name(file_name):
            raise HydroDSArgumentException("{file_name} is not a valid file name".format(file_name=file_name))

        url = self._get_dataservice_specific_url('myfiles/delete/{file_name}'.format(file_name=file_name))
        response = self._make_data_service_request(url=url, http_method='DELETE')
        return self._process_dataservice_response(response, save_as=None)

    def get_static_files_info(self):
        url = self._get_dataservice_specific_url('showstaticdata/info')
        response = self._make_data_service_request(url=url)
        return self._process_dataservice_response(response, save_as=None)

    def subset_raster(self, left, top, right, bottom, input_raster, output_raster=None, save_as=None):
        """
        Subsets a dem (dem tif file on the file server) and creates a new tif file with the subset data
        :param left: x-coordinate of the left-top corner of the bounding box
        :param top: y-coordinate of the left-top corner of the bounding box
        :param right: x-coordinate of the right-bottom corner of the bounding box
        :param bottom: y-coordinate of the right-bottom corner of the bounding box
        :param input_raster: raster from which the subset to be created. It can be either the name of the static DEM file or url path for the user DEM file
        :param save_as: (optional) subset dem tif file to save as (file name with path)
        :return: an object of type ServiceRequest

        example call format: http://129.123.41.184:20199/api/dataservice/rastersubset?xmin=-111.97&ymax=42.11&xmax=-111.35&ymin=41.66&input_raster=nedWesternUS.tif&output_raster=logan.tif
        """

        #url = 'http://129.123.41.158:8080/subsetdem'
        #self._check_user_irods_authentication()

        url = self._get_dataservice_specific_url(service_name='rastersubset')
        if save_as:
            self._validate_file_save_as(save_as)

        #payload = {'bbox': str(left) + ' ' + str(top) + ' ' + str(right) + ' ' + str(bottom)}
        payload = {'xmin': left, 'ymin': bottom, 'xmax': right, 'ymax': top, 'input_raster': input_raster}
        if output_raster:
            self._validate_output_raster_file_name(output_raster)
            payload['output_raster'] = output_raster

        response = self._make_data_service_request(url=url, params=payload)
        return self._process_dataservice_response(response, save_as)

    # TODO: the following function is porbably obsolete - replaced by the function delineate_watershed()
    def generate_watershed_raster(self, input_raster_url_path, outlet_shapefile_url_path, save_as=None):
        self._check_user_irods_authentication()

        if save_as:
            if not self._validate_file_save_as(save_as):
                return

            # file_name = os.path.basename(save_as)
                # if not self._validate_file_name(file_name):
                #     print("Error: Invalid file name specified (%s)." % file_name)
                #     return

        url = self.dataservice_base_url + '/generatewatershedraster'
        # you need to only send the file name part from the actual url path and we are removing the .zip from the file name
        # given the file url path: "http://129.123.41.158:8080/dem/user2623623514710145932.txt.zip"
        # we will be passing: user2623623514710145932.txt
        # input_raster = input_raster.split("/")[-1][:-4]
        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)
        outlet_shapefile_name = self._get_file_name_from_url_file_path(outlet_shapefile_url_path)
        payload = {"raster": input_raster_name, 'outletshp': outlet_shapefile_name}

        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, 'generate_watershed_raster', save_as)

    def subset_raster_to_reference(self, input_raster_url_path, ref_raster_url_path, output_raster=None, save_as=None):
        #self._check_user_irods_authentication()

        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('subsetrastertoreference')
        payload = {"input_raster": input_raster_url_path, 'reference_raster': ref_raster_url_path}
        if output_raster:
            self._validate_output_raster_file_name(output_raster)
            payload['output_raster'] = output_raster

        response = self._make_data_service_request(url=url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def raster_to_netcdf(self, input_raster_url_path, output_netcdf=None, save_as=None):

        if save_as:
            self._validate_file_save_as(save_as)

        # Example: 129.123.41.184:20199/api/dataservice/rastertonetcdf?input_raster=http://129.123.41.184:20199/files/data/user_2/SpawnProj.tif

        url = self._get_dataservice_specific_url('rastertonetcdf')
        payload = {"input_raster": input_raster_url_path}
        if output_netcdf:
            self._validate_output_netcdf_file_name(output_netcdf)
            payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def create_raster_slope(self, input_raster_url_path, output_raster, save_as=None):
        """
        Creates a raster with slope data

        :param input_raster_url_path: url file path of the raster file on HydroDS api server for which slope data
        is needed
        :param output_raster: name of the output slope raster file
        :param save_as: (optional) raster file name and file path to save the generated slope raster file locally
        :return:a dictionary with key 'output_raster' and value of url path for the slope raster file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified raster input file does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.create_raster_slope(input_raster_url_path=raster_url,
                                                        output_raster='slope_raster.tif',
                                                        save_as=r'C:\hydro-ds\slope_raster.tif')

            # print url path of the slope raster file
            output_slope_raster_url = hds_response_data['output_raster']
            print(output_slope_raster_url)
        """
        return self._create_raster_slope_or_aspect('computerasterslope', input_raster_url_path, output_raster, save_as)

    def create_raster_aspect(self, input_raster_url_path, output_raster, save_as=None):
        """
        Creates a raster with aspect data

        :param input_raster_url_path: url file path of the raster file on HydroDS api server for which aspect data
        is needed
        :param output_raster: name of the output aspect raster file
        :param save_as: (optional) raster file name and file path to save the generated aspect raster file locally
        :return:a dictionary with key 'output_raster' and value of url path for the slope raster file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified raster input file does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.create_raster_aspect(input_raster_url_path=raster_url,
                                                        output_raster='aspect_raster.tif',
                                                        save_as=r'C:\hydro-ds\aspect_raster.tif')

            # print url path of the aspect raster file
            output_aspect_raster_url = hds_response_data['output_raster']
            print(output_aspect_raster_url)
        """

        return self._create_raster_slope_or_aspect('computerasteraspect', input_raster_url_path, output_raster, save_as)

    def _create_raster_slope_or_aspect(self, service_name,  input_raster_url_path, output_raster, save_as=None):
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url(service_name)
        payload = {"input_raster": input_raster_url_path}
        if not self._validate_file_name(output_raster, ext='.tif'):
            err_msg = "Invalid output raster file name:{file_name}".format(file_name=output_raster)
            raise HydroDSArgumentException(err_msg)

        payload['output_raster'] = output_raster

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def project_clip_raster(self, input_raster, ref_raster_url_path, output_raster, save_as=None):
        """
        Project and clip a raster based on a reference raster

        :param input_raster: raster to be projected and clipped (just the file name if this data is supported by
                             HydroDS otherwise, url file path)
        :param ref_raster_url_path: url path of the raster to be used as the reference for projection and clipping
        :param output_raster: name for the output raster
        :param save_as: (optional) file name and file path to save the generated raster file locally
        :return: a dictionary with key 'output_raster' and value of url path for the generated raster file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified raster input file(s) does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            ref_input_raster_url = 'http://hydro-ds-uwrl.usu.edu:20199/files/data/user_2/SpawnProj.tif'
            input_raster = 'nlcd2011CONUS.tif'  # this a static data file on the HydroDS server
            hds_response_data =  hds.project_clip_raster(input_raster=input_raster,
                                                         ref_raster_url_path=ref_input_raster_url,
                                                         output_raster='nlcd_proj_spwan.tif')

            # print url path of the projected/clipped raster file
            output_raster_url = hds_response_data['output_raster']
            print(output_raster_url)
        """

        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('projectandcliprastertoreference')
        payload = {"input_raster": input_raster, 'reference_raster': ref_raster_url_path}
        self._validate_file_name(output_raster, ext='.tif')
        payload['output_raster'] = output_raster

        response = self._make_data_service_request(url=url, params=payload)
        return self._process_dataservice_response(response, save_as)

    # TODO: I think the following function is obsolete - use the function above (project_clip_raster)
    def subset_NLCD_to_reference_raster(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)

        # Example: http://129.123.41.158:8080/projectandclipraster?raster=nedLogan.tif

        url = self.dataservice_base_url + '/projectandclipraster'
        payload = {"raster": input_raster_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "subset_NLCD_to_reference_raster", save_as)

    def get_canopy_variable(self, input_NLCD_raster_url_path, variable_name, output_netcdf, save_as=None):
        """
        Generates a netcdf file that contains NLCD data for a given variable

        :param input_NLCD_raster_url_path: url file path for the raster for which NLCD data needs to be generated
        :param variable_name: name of the data variable (valid variable names are: 'cc', 'hcan', 'lai')
        :param output_netcdf: name for the output netcdf file
        :return: a dictionary with key 'output_netcdf' and value of url path for the netcdf file generated

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified raster input file does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            input_NLCD_raster_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/nlcd_proj_spwan.tif'
            hds_response_data = hds.get_canopy_variable(input_NLCD_raster_url_path=input_NLCD_raster_url_path,
                                                        variable_name='cc', output_netcdf='nlcd_cc_spwan.nc',
                                                        save_as=r'C:\hydro-DS_test\nlcd_cc_spwan.nc')

            # print the url path for the generated netcdf file containing canopy variable data
            output_canopy_netcdf_url = hds_response_data['output_netcdf']
            print(output_canopy_netcdf_url)

        """

        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('getcanopyvariable')
        payload = {"in_NLCDraster": input_NLCD_raster_url_path, 'variable_name': variable_name}
        self._validate_file_name(output_netcdf, ext='.nc')
        payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url=url, params=payload)
        return self._process_dataservice_response(response, save_as=save_as)

    # TODO: We should not support the following method. The functionality of this mkethod can be achieved by calling
    # 3 time the get_canopy_variable() method
    def get_canopy_variables(self, input_NLCD_raster_url_path, output_ccNetCDF=None, output_hcanNetCDF=None,
                             output_laiNetCDF=None):

        #URL: http://hostname/api/dataservice/getcanopyvariables?in_NLCDraster=http://hostname/
        # files/data/user_2/nlncd_spwan_proj_clip.tif

        # call with 3 output file names provided:
        #URL: http://hostname/api/dataservice/getcanopyvariables?in_NLCDraster=http://hostname/files
        # /data/user_2/nlncd_spwan_proj_clip.tif&out_ccNetCDF=cc_1.nc&out_hcanNetCDF=hcan_1.nc&out_laiNetCDF=lai_1.nc

        url = self._get_dataservice_specific_url('getcanopyvariables')
        payload = {"in_NLCDraster": input_NLCD_raster_url_path}
        if output_ccNetCDF:
            self._validate_output_netcdf_file_name(output_ccNetCDF)
            payload['out_ccNetCDF'] = output_ccNetCDF

        if output_hcanNetCDF:
            self._validate_output_netcdf_file_name(output_hcanNetCDF)
            payload['out_hcanNetCDF'] = output_hcanNetCDF

        if output_laiNetCDF:
            self._validate_output_netcdf_file_name(output_laiNetCDF)
            payload['out_laiNetCDF'] = output_laiNetCDF

        response = self._make_data_service_request(url=url, params=payload)
        return self._process_dataservice_response(response, save_as=None)

    def combine_rasters(self, input_one_raster_url_path, input_two_raster_url_path, output_raster, save_as=None):
        """
        Combines two rasters to create a new raster

        :param input_one_raster_url_path: url file path for the 1st raster file on HydroDS api server
        :param input_two_raster_url_path: url file path for the 2nd raster file on HydroDS api server
        :param output_raster: name of the output (combined) raster file
        :param save_as: (optional) raster file name and file path to save the generated combined raster file locally
        :return: a dictionary with key 'output_raster' and value of url path for the combined raster file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified netcdf input file(s) does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.combine_rasters(input_one_raster_url_path=raster_one_url,
                                                    input_two_raster_url_path=raster_two_url,
                                                    output_raster='combined_rasters.tif',
                                                    save_as=r'C:\hydro-ds\combined_raster.tif')

            # print url path of the combined raster file
            output_combined_raster_url = hds_response_data['output_raster']
            print(output_combined_raster_url)
        """
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('combinerasters')
        payload = {"input_raster1": input_one_raster_url_path, "input_raster2": input_two_raster_url_path}
        self._validate_output_raster_file_name(output_raster)
        payload['output_raster'] = output_raster

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def uncompress_raster(self, input_raster_url_path, save_as=None):
        if save_as:
            if not self._validate_file_save_as(save_as):
                return

        input_raster_name = self._get_file_name_from_url_file_path(input_raster_url_path)

        # Example: http://129.123.41.158:8080/uncompressraster?raster=nedLogan.tif

        url = self.dataservice_base_url + '/uncompressraster'
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

        url = self.dataservice_base_url + '/downloaddaymetmosaic'

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

        url = self.dataservice_base_url + '/downloaddaymettile'

        if end_year > start_year:
            payload = {"startyear": start_year, "endyear": end_year}
        else:
            payload = {"startyear": end_year, "endyear": start_year}

        payload["starttile"] = start_tile
        payload["endtile"] = end_tile
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "get_daymet_tile", save_as)

    def reverse_netcdf_yaxis(self, input_netcdf_url_path, output_netcdf=None, save_as=None):
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('reversenetcdfyaxis')
        payload = {"input_netcdf": input_netcdf_url_path}
        if output_netcdf:
            self._validate_output_netcdf_file_name(output_netcdf)
            payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    # TODO: this method has been replaced by the concatenate_netcdf method - need to delete this one
    def combine_netcdf(self, input_one_netcdf_url_path, input_two_netcdf_url_path, save_as=None):
        """
        Joins/combines two netcdf files to one netcdf file
        :param input_one_netcdf_url_path: url file path for the 1st netcdf file on HydroDS api server
        :param input_two_netcdf_url_path: url file path for the 2nd netcdf file on HydroDS api server
        :param save_as: (optional) file name and path to save the joined netcdf file locally
        :return: returns a dictionary with key 'output_netcdf' and value of url path for the joined netcdf file

        :raises:
            HydroDSArgumentException: one or more arguments failed validation

        """
        if save_as:
            self._validate_file_save_as(save_as)

        input_one_netcdf_name = self._get_file_name_from_url_file_path(input_one_netcdf_url_path)
        input_two_netcdf_name = self._get_file_name_from_url_file_path(input_two_netcdf_url_path)

        # Example: http://129.123.41.158:8080/combinenetcdf?inputnc1=netcdf24685a2f0387402dabf46bf7b56abdcb.nc&
        # inputnc2=netcdffd9a5b6f7d634d1cbd5325b98899b073.nc

        url = self.dataservice_base_url + '/combinenetcdf'
        payload = {"inputnc1": input_one_netcdf_name, "inputnc2": input_two_netcdf_name}
        response = self.requests.get(url, params=payload)
        return self._process_service_response(response, "combine_netcdf", save_as)

    def subset_netcdf(self, input_netcdf, ref_raster_url_path, output_netcdf=None, save_as=None):
        """
        :param input_netcdf: This can be either just a file name in which case this will be treated as a static data file
                             on the server or a url file path
        :param ref_raster_url_path:
        :param output_netcdf:
        :param save_as:
        :return:

        # URL: http://hostname/api/dataservice/subsetnetcdftoreference?input_netcdf=prcp_2010.nc4&reference_raster=http://129.123.41.184:20199/files/data/user_2/SpawnProj.tif
        """

        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('subsetnetcdftoreference')
        payload = {"input_netcdf": input_netcdf, 'reference_raster': ref_raster_url_path}
        if output_netcdf:
            self._validate_output_netcdf_file_name(output_netcdf)
            payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def subset_netcdf_by_time(self, input_netcdf_url_path, time_dimension_name, start_time_index, end_time_index,
                              output_netcdf=None, save_as=None):

        # URL: http://hostname/api/dataservice/subsetnetcdfbytime?input_netcdf=http://hostname/
        # files/data/user_2/subset.nc&output_netcdf=subset_time_1_10.nc&time_dim_name=time&start_time_index=1
        # &end_time_index=10

        if save_as:
            self._validate_file_save_as(save_as)

        try:
            int(start_time_index)
        except TypeError:
            raise ValueError("Value for start time index must be an integer")

        try:
            int(end_time_index)
        except TypeError:
            raise ValueError("Value for start time index must be an integer")

        if start_time_index > end_time_index:
            raise ValueError("Start time index must be smaller than end time index")

        url = self._get_dataservice_specific_url('subsetnetcdfbytime')
        payload = {"input_netcdf": input_netcdf_url_path, 'time_dim_name': time_dimension_name,
                   'start_time_index': start_time_index, 'end_time_index': end_time_index}
        if output_netcdf:
            self._validate_output_netcdf_file_name(output_netcdf)
            payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def project_netcdf(self, input_netcdf_url_path, utm_zone, variable_name, output_netcdf, save_as=None):
        """
        Project a netcdf file

        :param input_netcdf_url_path: url file path for the netcdf file to be projected
        :param utm_zone: UTM zone value to use for projection
        :param variable_name: name of the data variable
        :param output_netcdf: name for the output (projected) netcdf file
        :param save_as: (optional) file name and file path to save the projected netcdf file locally
        :return: a dictionary with key 'output_netcdf' and value of url path for the projected netcdf file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified netcdf input file(s) does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            input_netcdf_url_path = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/subset_netcdf_to_spawn.nc'
            hds_response_data = hds.project_netcdf(input_netcdf_url_path=input_netcdf_url_path, variable_name='prcp',
                                                   utm_zone=12, output_netcdf='projected_prcp_spwan.nc')

            # print the url path for the projected netcdf file
            output_projected_netcdf_url = hds_response_data['output_netcdf']
            print(output_projected_netcdf_url)
        """

        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('projectnetcdf')
        payload = {"input_netcdf": input_netcdf_url_path, 'variable_name': variable_name, 'utm_zone': utm_zone}
        self._validate_file_name(output_netcdf, ext='.nc')
        payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def project_subset_resample_netcdf(self, input_netcdf_url_path, ref_netcdf_url_path, variable_name,
                                       output_netcdf=None, save_as=None):
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('projectsubsetresamplenetcdftoreferencenetcdf')
        payload = {"input_netcdf": input_netcdf_url_path, 'reference_netcdf': ref_netcdf_url_path,
                   'variable_name': variable_name}
        if output_netcdf:
            self._validate_output_netcdf_file_name(output_netcdf)
            payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def concatenate_netcdf(self, input_netcdf1_url_path, input_netcdf2_url_path, output_netcdf, save_as=None):
        """
        Joins two netcdf files to create a new netcdf file

        :param input_netcdf1_url_path: url file path for the 1st netcdf file on HydroDS api server
        :param input_netcdf2_url_path: url file path for the 2nd netcdf file on HydroDS api server
        :param output_netcdf: name of the output (concatenated) netcdf file
        :param save_as: (optional) file name and file path to save the generated concatenated netcdf file locally
        :return: a dictionary with key 'output_netcdf' and value of url path for the joined netcdf file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified netcdf input file(s) does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.concatenate_netcdf(input_netcdf1_url_path='url_path_for_1st_netcdf_file',
                                                       input_netcdf2_url_path='url_path_for_2nd_netcdf_file',
                                                       output_netcdf='concatenated.nc',
                                                       save_as=r'C:\hydro-DS_test\concatenated_prcp_2015.nc')

            # print the url path for the concatenated netcdf file
            output_concatenated_netcdf_url = hds_response_data['output_netcdf']
            print(output_concatenated_netcdf_url)

        """
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('concatenatenetcdf')
        payload = {"input_netcdf1": input_netcdf1_url_path, "input_netcdf2": input_netcdf2_url_path}
        self._validate_output_netcdf_file_name(output_netcdf)
        payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def project_raster_to_UTM_NAD83(self, input_raster_url_path, utm_zone, output_raster, save_as=None):
        """
        Project a raster to UTM NAD83 projection

        :param input_raster_url_path: url file path for the user owned raster to be projected
        :param utm_zone: UTM zone value to be used for projection
        :param output_raster: name for the output (projected) raster file
        :param save_as: (optional) raster file name and file path to save the projected raster file locally
        :return: a dictionary with key 'output_raster' and value of url path for the projected raster file

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified raster input file(s) does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.project_raster_to_UTM_NAD83(input_raster_url_path='url_raster_file_path',
                                                                utm_zone=12, output_raster='projected_raster.tif')

            # print url path of the projected raster file
            output_projected_raster_url = hds_response_data['output_raster']
            print(output_projected_raster_url)
        """
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('projectraster')
        payload = {"input_raster": input_raster_url_path, 'utmZone': utm_zone}
        self._validate_output_raster_file_name(output_raster)
        payload['output_raster'] = output_raster

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def project_shapefile_to_UTM_NAD83(self, input_shapefile_url_path, utm_zone, output_shape_file=None, save_as=None):
        if save_as:
            self._validate_file_save_as(save_as)

        # URL: http://129.123.41.184:20199/api/dataservice/projectshapefile?utm_zone=12&input_shape_file=http://129.123.41.184:20199/files/data/user_2/outlet.zip

        url = self._get_dataservice_specific_url('projectshapefile')
        payload = {"input_shape_file": input_shapefile_url_path, 'utm_zone': utm_zone}
        if output_shape_file:
            err_msg = "Invalid output file name:{file_name}".format(file_name=output_shape_file)
            if len(output_shape_file.strip()) < 5 or not output_shape_file.endswith('.shp'):
                raise ValueError(err_msg)
            payload['output_shape_file'] = output_shape_file

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def create_outlet_shapefile(self, point_x, point_y, output_shape_file_name, save_as=None):
        """
        Create an outlet shapefile. The generated shapefile is stored on the server as a zip file

        :param point_x: X-coordinate of outlet point
        :param point_y: Y-coordinate of outlet point
        :param output_shape_file_name: name of the outlet shapefile
        :param save_as: (optional) shapefile name and file path to save the generated shapefile locally
        :return: a dictionary with key 'output_shape_file' and value of url path for the outlet shapefile

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.create_outlet_shapefile(point_x=-111.787, point_y=41.742,
                                                            output_shape_file='outlet-shape.shp'
                                                            save_as=r'C:\hydro-DS_test\outlet.zip')

            # print the url path for the outlet shapefile
            output_outlet_shape_file_url = hds_response_data['output_shape_file_name']
            print(output_outlet_shape_file_url)
        """
        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url(service_name='createoutletshapefile')
        payload = {"outletPointX": point_x, 'outletPointY': point_y}
        if not self._validate_file_name(output_shape_file_name, ext='.shp'):
            raise HydroDSArgumentException('{file_name} is not a valid shapefile '
                                           'name.'.format(file_name=output_shape_file_name))

        payload['output_shape_file_name'] = output_shape_file_name

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    # TODO: This method needs to be tested (6/19/2015)
    def delineate_watershed(self, input_raster_url_path, outlet_point_x, outlet_point_y, utm_zone, threshold,
                            output_raster, output_outlet_shapefile, save_as=None):
        """
        Delineate watershed

        :param input_raster_url_path: url file path for the raster file for which to delineate watershed
        :param outlet_point_x: X-coordinate of the outlet point
        :param outlet_point_y: Y-coordinate of the outlet point
        :param utm_zone: utm zone value to be used
        :param threshold: threshold value to be used
        :param: output_raster: file name for the delineated watershed raster file
        :param save_as: (optional) raster file name and file path to save the delineated watershed raster file locally
        :return:a dictionary with key 'output_raster' and value of url path for the watershed raster file, and
        key 'output_outlet_shapefile' and value of url path for the outlet shapefile

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSBadRequestException: one or more argument failed validation on the server side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified raster input file does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            hds_response_data = hds.delineate_watershed(input_raster_url_path=raster_url,
                                                        outlet_point_x=111.787,
                                                        outlet_point_y=41.742,
                                                        utm_zone=12,
                                                        threshold=60000,
                                                        output_raster='logan_watershed.tif',
                                                        output_outlet_shapefile='logan_outlet.shp',
                                                        save_as=r'C:\hydro-ds\delineated_ws.tif')

            # print url path of the delineated watershed raster file
            output_delineated_raster_url = hds_response_data['output_raster']
            print(output_delineated_raster_url)

            # print the url path of the outlet shapefile
            output_outlet_shapefile_url = hds_response_data['output_outlet_shapefile']
            print(output_outlet_shapefile_url)
        """
        if save_as:
            self._validate_file_save_as(save_as)
        if not self._validate_file_name(output_raster, ext='.tif'):
            raise HydroDSArgumentException("{file_name} is not a valid raster file name".format(file_name=output_raster))

        if not self._validate_file_name(output_outlet_shapefile, ext='.shp'):
            raise HydroDSArgumentException("{file_name} is not a valid shapefile name".format(file_name=output_outlet_shapefile))

        url = self._get_dataservice_specific_url(service_name='delineatewatershed')
        payload = {'utmZone': utm_zone, 'streamThreshold': threshold, 'outletPointX': outlet_point_x,
                   'outletPointY': outlet_point_y, "input_DEM_raster": input_raster_url_path,
                   "output_raster": output_raster, 'output_outlet_shapefile': output_outlet_shapefile}
        response = self._make_data_service_request(url=url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def resample_raster(self, input_raster_url_path, cell_size_dx, cell_size_dy, resample=None, output_raster=None, save_as=None):
        if save_as:
            self._validate_file_save_as(save_as)

        # example: http://129.123.41.184:20199/api/dataservice/resampleraster?dx=50&dy=50&
        # input_raster=http://129.123.41.184:20199/files/data/user_2/projected.tif

        url = self._get_dataservice_specific_url('resampleraster')
        payload = {"input_raster": input_raster_url_path, 'dx': cell_size_dx, 'dy': cell_size_dy}
        if resample:
            payload['resample'] = resample

        if output_raster:
            self._validate_output_raster_file_name(output_raster)
            payload['output_raster'] = output_raster

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def resample_netcdf(self, input_netcdf_url_path, ref_netcdf_url_path, variable_name, output_netcdf=None,
                        save_as=None):
        """
        :param input_netcdf_url_path: url file path to netcdf file on the api server which needs to be resampled
        :param ref_netcdf_url_path:
        :param output_netcdf:
        :param  variable_name: name of the variable in the input netcdf to be used for resampling
        :param save_as:
        :return:

        # URL: http://129.123.41.184:20199/api/dataservice/resamplenetcdftoreferencenetcdf?input_netcdf=
        http://129.123.41.184:20199/files/data/user_2/test_proj.nc&reference_netcdf=http://129.123.41.184:20199/files/
        data/user_2/SpawnWS_yrev.nc&output_netcdf=resample.nc&variable_name=prcp
        """

        if save_as:
            self._validate_file_save_as(save_as)

        url = self._get_dataservice_specific_url('resamplenetcdftoreferencenetcdf')
        payload = {"input_netcdf": input_netcdf_url_path, 'reference_netcdf': ref_netcdf_url_path,
                   'variable_name': variable_name}
        if output_netcdf:
            self._validate_output_netcdf_file_name(output_netcdf)
            payload['output_netcdf'] = output_netcdf

        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def upload_file_irods(self, file_to_upload):
        if not os.path.isfile(file_to_upload):
            raise Exception("Error: Specified file to upload (%s) does not exist." % file_to_upload)

        file_name = os.path.basename(file_to_upload)
        file_url_path = self.irods_rest_base_url + '/fileContents/usu/home/rods/' + file_name
        headers = {'accept': 'application/json'}
        with open(file_to_upload, 'rb') as upload_file_obj:
            response = self.requests.post(file_url_path, data={'uploadFile': file_name},
                                          files={'file': upload_file_obj}, auth=(self.username, self.password),
                                          headers=headers)

        if response.status_code != requests.codes.ok:
            raise Exception("Error: Failed to upload to iRODS." + response.reason)

        response_dict = json.loads(response.content)
        print "File upload was successful."
        uploaded_file_path = response_dict['dataPath']
        print("Uploaded file URL path:%s" % uploaded_file_path)
        service_req = ServiceRequest(service_name='upload_file', service_id_name='',
                                     service_id_value='', service_status='success', file_path=uploaded_file_path)
        _ServiceLog.add(service_req)
        self.save_service_call_history()
        print(service_req.to_json())
        return service_req

    def upload_file(self, file_to_upload):
        if not os.path.isfile(file_to_upload):
            raise Exception("Error: Specified file to upload (%s) does not exist." % file_to_upload)

        url = self._get_dataservice_specific_url('myfiles/upload')
        with open(file_to_upload, 'rb') as upload_file_obj:
            response = self._make_data_service_request(url=url, http_method='POST', files={'file': upload_file_obj})

        return self._process_dataservice_response(response, save_as=None)

    def download_file(self, file_url_path, save_as):
        """
        Download a file (that the user owns) from the HydroDS server

        :param file_url_path: url for the file to be downloaded
        :param save_as: file name and file path to save the downloaded file
        :return: nothing

        :raises: HydroDSArgumentException: one or more argument failed validation at client side
        :raises: HydroDSNotAuthenticatedException: provided user account failed validation
        :raises: HydroDSNotAuthorizedException: user making this request is not authorized to do so
        :raises: HydroDSNotFoundException: specified file to download does not exist on the server

        Example usage:
            hds = HydroDS(username=your_username, password=your_password)
            url_path_for_the_file_to_download = 'http://hydro-ds.uwrl.usu.edu:20199/files/data/user_2/nlcd_proj_spwan.tif'
            hds.download_file(file_url_path=url_path_for_the_file_to_download, save_as=r'C:\hydro-ds\nlcd_proj_spwan.tif')

            print("File download was successful")

        """
        self._validate_file_save_as(save_as)

        with open(save_as, 'wb') as file_obj:
            response = requests.get(file_url_path, stream=True, auth=self.authorization)

            if not response.ok:
                # raise appropriate HydroDS exception
                self._process_dataservice_response(response)

            for block in response.iter_content(1024):
                if not block:
                    break
                file_obj.write(block)


    def zip_files(self, files_to_zip, zip_file_name, save_as=None):
        # validate parameters
        if save_as:
            self._validate_file_save_as(save_as)
        if type(files_to_zip) is not list:
            raise Exception("Error: Invalid parameter value:{param}. It should be a list.".format(param=files_to_zip))

        if not self._validate_file_name(zip_file_name, ext='.zip'):
            raise Exception('Error: {file_name} is not a valid zip file name.'.format(file_name=zip_file_name))

        file_names = ','.join(files_to_zip)
        url = self._get_dataservice_specific_url('myfiles/zip')
        payload = {"file_names": file_names, 'zip_file_name': zip_file_name}
        response = self._make_data_service_request(url, params=payload)
        return self._process_dataservice_response(response, save_as)

    def download_file_old(self, file_url_path, save_as):
        self._check_user_irods_authentication()
        if not self._validate_file_save_as(save_as):
            return
        file_url_path = self.irods_rest_base_url + '/fileContents' + file_url_path
        with open(save_as, 'wb') as file_obj:
            response = requests.get(file_url_path, stream=True, auth=(self.irods_username, self.irods_password))

            if not response.ok:
                # Something went wrong
                raise Exception("Error: Error in downloading the file." + response.reason)

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

    def _validate_output_raster_file_name(self, file_name):
        err_msg = "Invalid output raster file name:{file_name}".format(file_name=file_name)
        if len(file_name.strip()) < 5 or not file_name.endswith('.tif'):
            raise HydroDSArgumentException(err_msg)

    def _validate_output_netcdf_file_name(self, file_name):
        err_msg = "Invalid output netcdf file name:{file_name}".format(file_name=file_name)
        if len(file_name.strip()) < 4 or not file_name.endswith('.nc'):
            raise HydroDSArgumentException(err_msg)

    def _make_data_service_request(self, url, http_method='GET', params=None, data=None, files=None):
        if http_method == 'GET':
            return self.requests.get(url, params=params, data=data, auth=self.authorization)
        elif http_method == 'DELETE':
            return self.requests.delete(url, params=params, data=data, auth=self.authorization)
        elif http_method == 'POST':
            return self.requests.post(url, params=params, data=data, files=files, auth=self.authorization)
        else:
            raise Exception("%s http method is not supported for the HydroDS API." % http_method)

    def _get_dataservice_specific_url(self, service_name):
        return "{base_url}/{service_name}".format(base_url=self.dataservice_base_url, service_name=service_name)

    def _process_dataservice_response(self, response, save_as=None):
        if response.status_code != requests.codes.ok:
            if response.status_code == 400:
                raise HydroDSBadRequestException("HydroDS Service Error. {response_err}".format(response_err=response.reason))
            elif response.status_code == 401:
                raise HydroDSNotAuthenticatedException("HydroDS Service Error. {response_err}".format(response_err=response.reason))
            elif response.status_code == 403:
                raise HydroDSNotAuthorizedException("HydroDS Service Error. {response_err}".format(response_err=response.reason))
            elif response.status_code == 404:
                raise HydroDSNotFoundException("HydroDS Service Error. {response_err}".format(response_err=response.reason))
            elif response.status_code == 500:
                raise HydroDSServerException("HydroDS Service Error. {response_err}".format(response_err=response.reason))
            else:
                raise HydroDSException("HydroDS Service Error. {response_err}".format(response_err=response.reason))

        response_dict = response.json() # json.loads(response.content)
        if response_dict['success']:
            if save_as:
                if len(response_dict['data']) != 1:
                    raise ValueError("Multiple output files found. Can't download multiple files.")
                file_url = response_dict['data'].values()[0]
                self.download_file(file_url, save_as)
            return response_dict['data']
        else:
            self._raise_service_error(response_dict['error'])

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
        raise HydroDSException("Error:%s" % message)

    def save_service_call_history(self):
        _ServiceLog.save()

    def clear_service_log(self):
        _ServiceLog.delete_all()
        print ("Service call history deleted.")

    def _validate_file_name(self, file_name, ext=None):
        try:
            name_part, ext_part = os.path.splitext(file_name)
            if len(name_part) == 0 or len(ext_part) < 2:
                return False

            if ext:
                if ext != ext_part:
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
            raise HydroDSArgumentException("Specified file path (%s) to save does not exist." % save_file_dir)

        if not os.access(save_file_dir, os.W_OK):
            raise HydroDSArgumentException("You do not have write permissions to directory '{0}'.".format(save_file_dir))

        file_name = os.path.basename(save_as)
        if not self._validate_file_name(file_name):
            raise HydroDSArgumentException("{file_name} is not a valid file name for saving the output "
                                           "file.".format(file_name=file_name))

        if file_ext:
            file_extension = os.path.splitext(save_as)[1]
            if file_extension != file_ext:
                raise HydroDSArgumentException("Invalid save as file type:{file_extension}. File type must "
                                               "be:{file_ext}".format(file_extension=file_extension, file_ext=file_ext))

    def _check_user_irods_authentication(self):
        if not self.user_irods_authenticated:
            raise Exception("You first need to get authenticated to iRODS.")

    def _check_user_hpc_authentication(self):
        if not self.user_hpc_authenticated:
            raise Exception("You first need to get authenticated to HPC.")

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