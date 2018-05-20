"""
Edge Computing Embedded Platform
Developed by Abhishek Gurudutt, Chinmayi Divakara
Praveen Prabhakaran, Tejeshwar Chandra Kamaal
"""

import ecep_endNode.ecep_wampClient.wamp_client
import ecep_endNode.ecep_wampClient.callContainer_api
import ecep_endNode.ecep_wampClient.deviceRegister
import ecep_endNode.ecep_wampClient.fetcher
client = None
def init(path):
    ecep_endNode.ecep_wampClient.fetcher.init_fetcher(path)
