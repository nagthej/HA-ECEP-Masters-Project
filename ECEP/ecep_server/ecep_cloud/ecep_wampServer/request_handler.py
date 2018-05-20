"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakar,
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
Deepa Rajendra Sangolli, Nagthej Manangi Ravindrarao,
Priyanka Chidambar Patil, Thrishna Palissery

Handles user request. This integrates with DB and wamp server
"""
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import time
import json
import urllib.parse as urlparse
from multiprocessing import Queue
import sys

from ecep_cloud.ecep_wampServer.container_control import *
from ..ecep_db.controller import Compute_Manager, Image_Manager, Device_Manager, Location_Manager, Info_Manager, \
    init_db_lock
from ecep_cloud.ecep_wampServer.wamp_server import *
from ecep_cloud.ecep_wampServer.update_db import threaded

q = Queue()
@threaded
def checkConnection(name='checkConnection'):
    """
    This function broadcasts a message to all the registered
    devices
    """
    topic = "com.ecep.server.checkConnection"
    data = True
    sendTo(topic, data)


# Handle command request
def handleCmd(entries):
    """
    Check if the received request is valid / not valid.
    If valid, then update database and transmit to end node.
    """
    packet = sendCommand(entries)
    if packet['valid']:
        print ('valid command passed')
        sendTo(packet['topic'], packet['msg'])
    else:
        print ('invalid command passed')


# Handle request from user
class handleReq(tornado.web.RequestHandler):
    """
    Handle user command request
    """

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    def get(self):
        temp = contcmd = {'username': 'newlogin', 'command': 'create', 'deviceId': 'beaglebone', 'imageName': 'ubuntu',
                          'containerName': 'abhi'}
        handleCmd(temp)
        self.write('Edge Computing Project')

    def put(self, *kwargs):
        pdate = json.loads(self.request.body)

    def post(self, **kwargs):
        print("**********************************requesthandler handlerequest posti 1********************************************")    
        print(kwargs)
        try:
            print("**********************************requesthandler handlerequest post 2********************************************")
            data = tornado.escape.json_decode(self.request.body)
            print("after data",data)
        except:
            data = dict(urlparse.parse_qsl(self.request.body))

        for entry in data:
            if entry == 'command':
                print ('command')
                handleCmd(data)
        self.write(data)

    def prepare(self):
        print("**************requesthandler prepare**********************")
        if self.request.headers["Content-Type"].startswith("application/json"):
            #self.json_args = json.loads(self.request.body)
            self.json_args = tornado.escape.json_decode(self.request.body)
        else:
            self.json_args = None


class Download(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')
    
    @gen.coroutine
    def get(self, **kwargs):
        print("################################Download  get method######################")
        print(kwargs)
        print(self.get_argument(name='username'))
        username =  self.get_argument(name='username')
        containerName = self.get_argument(name='containerName')
        filename = self.get_argument(name='filename')
        file_root_path = "/home/ubuntu/ecep/"
        chunk = 2048
        keys = ['username', 'containerName', 'filename']

        #try:
         #   print("################################Download try ")
         #   data = tornado.escape.json_decode(self.request.body)
         #   print(data) 
        #except:
         #   data = dict(urlparse.parse_qsl(self.request.body))

        #for key in keys:
         #   if key not in data:
        print("################################key not in data  get method######################")
        #self.set_status(400, reason="param %s missing" % key)
        #raise tornado.web.HTTPError(400)

        file_path = file_root_path + username + '_' + containerName + '/' + filename
        print (file_path)
        try:
            print("################################Download try file_object ")
            file_object = open(file_path, 'rb')
            while True:
                d = file_object.read(chunk)
                #print(d)
                if not d:
                    break
                self.write(d)
                self.flush()
            self.finish()
        except Exception as e:
            print(e)


class Upload(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    @gen.coroutine
    def post(self, **kwargs):
        print("#################################### log fileupload######################")
        #file_root_path = "/home/chinmayi/ecep/"
        file_root_path = "/home/ubuntu/ecep/"
        chunk = 2048
        keys = ['username', 'containerName', 'filename']
        #print self.request.body
        username = self.get_argument(name='username')
        containerName = self.get_argument(name='containerName')
        filename = "output.log"

        fileinfo = self.request.files['file'][0]

        file_path = file_root_path + username + '_' + containerName+'/' + 'output.log'

        if fileinfo['body'] is None:
            print("fileinfo body", fileinfo['body'])
            q.put({'status':'fail'})
        fh = open(file_path, 'wb')
        fh.write(fileinfo['body'])
        print("fileinfo body2", fileinfo['body'])
        ret = {'status':'success'}
        q.put(ret)

class DeviceHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    def get_device_list(self, data):

        device = Device_Manager()
        ret = device.get_device_list_filter(**data)
        return ret

    def put(self, **kwargs):
        try:
            data = json.loads(self.request.body)
        except:
            data = dict(urlparse.parse_qsl(self.request.body))
        print(data)
        device = Device_Manager()
        ret = device.add_new_device_node(**data)
        self.write(json.dumps(ret))
        self.finish()
        return

    def get(self):

        try:
            data = json.loads(self.request.query)
        except:
            data = dict(urlparse.parse_qsl(self.request.query))

        print (data)

        if data['command'] == 'filter':
            data.__delitem__('command')

            ret = self.get_device_list(data)
            self.write(json.dumps(ret))
            self.finish()
            return
        if data['command'] == 'all':
            data.__delitem__('command')
            device = Device_Manager()
            ret = device.get_device_list()
            self.write(json.dumps(ret))
            self.finish()
            return
        return


class ImageHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    def put(self, **kwargs):
        try:
            data = json.loads(self.request.body)
        except:
            data = dict(urlparse.parse_qsl(self.request.body))
        print("***********************Imagehandlerput***************************")
        print(data)
        image = Image_Manager()
        ret = image.add_new_image_entry(**data)
        self.write(json.dumps(ret))
        self.finish()
        return

    def get(self):
        print("***********************Imagehandler get***************************")
        try:
            data = json.loads(self.request.query)
        except:
            data = dict(urlparse.parse_qsl(self.request.query))

        image = Image_Manager()
        #image = Image_Manager()
        image.add_new_image_entry(imageName="training/postgres", arch="x86_64")
        image.add_new_image_entry(imageName="ubuntu:latest", arch="x86_64")
        image.add_new_image_entry(imageName="tensorflow/tensorflow:latest-gpu", arch="x86_64")
        image.add_new_image_entry(imageName="nvidia/cuda", arch="x86_64")
        #self.write(json.dumps(ret))
        #self.finish()
        if data['command'] == 'filter':
            data.__delitem__('command')
            ret = image.get_image_list(**data)
            self.write(json.dumps(ret))
            self.finish()
            return
        if data['command'] == 'all':
            print (data)
            data.__delitem__('command')
            ret = image.get_image_list(**data)
            self.write(json.dumps(ret))
            self.finish()
            return
        return


class ComputeHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    def get(self, **kwargs):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except:
            data = dict(urlparse.parse_qsl(self.request.query))
        """get container list by username,
            get container list by deviceId"""

        compute = Compute_Manager()
       
        if data['command'] == 'filter':
            data.__delitem__('command')
            print(" compute handler kwargs get compute reququest *************************************************")
            print ("%%%%%%%%%%%%%%%%%%%%%%%data", data)

            ret = compute.get_compute_node_list(**data)
            self.write(json.dumps(ret))
            self.finish()
            return

        if "username" in data or "deviceId" in data:
            ret = compute.get_compute_node_list()
            print ("**************************************************ComputeHandler",  ret )
            self.write(json.dumps(ret))
            self.finish()
            return
        else:
            raise tornado.web.HTTPError(400)


class LocationHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    def get(self, **kwargs):
        loc_list = Location_Manager()
        loc = loc_list.get_location()
        ret = json.dumps(loc)
        self.write(ret)
        self.finish()


class CPUInfoHandler(tornado.web.RequestHandler):
    def set_default_header(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with,Origin')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT')

    def get(self, **kwargs):
        try:
            data = json.loads(self.request.body)
        except:
            data = dict(urlparse.parse_qsl(self.request.query))

        if 'deviceId' not in data:
            self.set_status(400, reason="param %s missing" % 'deviceId')
            raise tornado.web.HTTPError(400)

        info = Info_Manager()
        ret = info.get_device_info(**data)
        self.write(json.dumps(ret))
        self.finish()


class CPUInfoHandlerWS(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("cpuinfo websocket opened")
        pass

    @tornado.web.asynchronous
    def on_message(self, message):
        data = json.loads(message)
        print (data)
        if 'deviceId' not in data:
            self.write_message("error")
            return

        info = Info_Manager()
        ret = info.get_device_info(**data)
        self.write_message(json.dumps(ret))

    def on_close(self):
        print("websocket connecction closed")
        pass


class ComputeHandlerWS(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("compute websocket opened")
        pass

    @tornado.web.asynchronous
    def on_message(self, message):
        try:
            data = json.loads(message)
        except:
            self.close()
        """get container list by username,
            get container list by deviceId"""

        compute = Compute_Manager()

        if data['command'] == 'filter':
            data.__delitem__('command')
            print(" compute handler kwargs get compute reququest *************************************************")
            #print(kwargs)
            print(data)
            #compute.add_new_compute_node(username="admin", containerName="/fervent_minsky")
            #compute.add_new_compute_node(username="admin", containerName="wwww")
            #compute.update_compute_node(username="admin", containerName="/fervent_minsky", containerId="twyt3673", deviceId="deepa-Virt/08:00:27:be:1f:48")
             #                status="3")
            #compute.add_new_compute_node(username="admin", containerName="blah")
            #compute.add_new_compute_node(deviceId="deepa-Virt/08:00:27:be:1f:48", containerName="wwww")
            #compute.update_compute_node(username="admin", containerName="blah", containerId="twyt3673", deviceId="deepa-Virt/08:00:27:be:1f:48",
            print("********************ComputeHandlerWS***********************")
            print(data)
            ret = compute.get_compute_node_list(**data)
            ret = json.dumps(ret)
           # print ("*************************************ComputeHandlerWS return", ret)
            self.write_message(ret)
        else:
            print("Invalid Params")

    def on_close(self):
        print("websocket connecction closed")
        pass



class logHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=16)

    @run_on_executor
    def background_task(self):
        return q.get()

    @gen.coroutine
    def get(self, **kwargs):
        try:
            data = json.loads(self.request.body)
        except:
            data = dict(urlparse.parse_qsl(self.request.query))
        if 'deviceId' not in data:
            self.set_status(400, reason="param %s missing" % 'deviceId')
            raise tornado.web.HTTPError(400)
        print (data)

        handleCmd(data)

        item = yield self.background_task()

        self.write(json.dumps(item))
        self.finish()



application = tornado.web.Application([(r"/handle_request", handleReq),
                                       (r"/download", Download),
                                       (r"/device", DeviceHandler),
                                       (r"/image", ImageHandler),
                                       (r"/compute", ComputeHandler),
                                       (r"/location", LocationHandler),
                                       (r"/cpuinfo", CPUInfoHandler),
                                       (r"/log", logHandler),
                                       (r'/upload', Upload),
                                       (r"/cpuinfo_ws", CPUInfoHandlerWS),
                                       (r"/compute_ws", ComputeHandlerWS)])

if __name__ == "__main__":
    # params for wampserver
    ip = u'127.0.0.1'
    port = sys.argv[1]
    realm = str(sys.argv[2])
    server = wampserver()
    check = server.connect(ip, port, realm)

    # wait till the initialization of the wamp router
    time.sleep(5)

    # start a thread to check heartbeat
    uDB_instance = updateDB()
    handle_checkHeartbeat = uDB_instance.checkHeartbeat()
    #    handle_checkConnection = checkConnection()

    # start a tornado server to handle user requests
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
    handle_checkHeartbeat.join()
    q.join()
# handle_checkConnection.join()
