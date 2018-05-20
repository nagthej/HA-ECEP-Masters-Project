#!/bin/sh


# Change the parameters according to the configuration of wamp server, the port number should be same as the server
ip="ec2-18-218-62-54.us-east-2.compute.amazonaws.com"
#ip="127.0.0.1"
port="8096"
realm="realm1"
path=$HOME/ecep_files/


# Do not edit the below line
python3 -m ecep_endNode.ecep_wampClient.deviceRegister $ip $port $realm $path
