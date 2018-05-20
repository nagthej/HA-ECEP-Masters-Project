"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
Deepa Rajendra Sangolli, Nagthej Manangi Ravindrarao,
Priyanka Chidambar Patil, Thrishna Palissery

REST API to fetch application from server and
to upload log file from edge node to server
"""

import json
import os
import requests

ip = "ec2-18-218-62-54.us-east-2.compute.amazonaws.com"
#ip = "127.0.0.1"
#local_ip = "192.168.0.131"
local_ip = "172.17.0.1"
port = 9000
download_route = '/download'
upload_route = '/upload'
file_root_path = None

def init_fetcher(root_path):
    global file_root_path
    if file_root_path is None:
        file_root_path = root_path


def get_file(**kwargs):
    """
    To download file from server
    :param kwargs: has to contain username, container name and file name
    :return: local path of the downloaded file
    """
    key = ['username', 'containerName', 'filename']
    print (kwargs)
    for param in key:
        if param not in kwargs:
            raise ValueError("Missing %s" % param)
	

    url = 'http://' + ip + ':' + str(port) + download_route
    print (url)
    print  (file_root_path + kwargs['username'] + "_" + kwargs['containerName'] + '/' + kwargs['filename'])

    #file_path = file_root_path + kwargs['username'] + "_" + kwargs['containerName'] + '/' + kwargs['filename']
    #local_path = file_root_path + kwargs['filename']
    #if not os.path.exists(file_root_path + kwargs['username']+'_'+kwargs['containerName']):
     #      os.makedirs(file_root_path + kwargs['username']+'_'+kwargs['containerName'])
    try:
        file_path = file_root_path + kwargs['username'] + "_" + kwargs['containerName'] + '/' + kwargs['filename']
        local_path = file_root_path + kwargs['filename']
        if not os.path.exists(file_root_path + kwargs['username']+'_'+kwargs['containerName']):
           os.makedirs(file_root_path + kwargs['username']+'_'+kwargs['containerName'])
        data = json.dumps(kwargs)
        print(data)
        headers = {'Content-Type': 'application/json'}
        req = requests.get(url, kwargs)
        req.raise_for_status()
        with open(file_path, 'wb') as fd:
             for chunk in req.iter_content(chunk_size=50000):
                 fd.write(chunk)

        return file_path
    except Exception as e:
            print(e)

def put_file(**kwargs):
    """
    To upload a file to server
    :param kwargs: contains container name, local path and if file is available or not.
    :return: True or false
    """
    key = ['containerName', 'local_path', 'isFile']
    print(kwargs)
    print("put_file###############################")
    for param in key:
        if param not in kwargs:
            raise ValueError("Missing %s" % param)

    url = 'http://' + ip + ':' + str(port) + upload_route
    upload_kwargs = {'containerName': kwargs['containerName'].split('_')[1], 'username': kwargs['containerName'].split('_')[0]}
    print (upload_kwargs)

    try:
        file_path = kwargs['local_path']
        if kwargs['isFile'] == True:
            input = {'file' : open(file_path, 'rb')}
        else:
            input = {'file': None}
        print ("input= ", input)
        requests.post(url, data=upload_kwargs, files=input)

        return kwargs['isFile']

    except Exception as e:
        print(e)


if __name__  == "__main__":

    #data = {'username':'admin','containerName':'pull','filename':'Doc1.docx'}
    #get_file(**data)

    data = {'containerName': 'abhi_test', 'local_path': '/home/abhi/output.log', 'isFile': True}
    put_file(**data)

