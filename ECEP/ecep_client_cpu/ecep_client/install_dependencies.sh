#!/bin/bash

sudo apt-get  update
sudo apt-get install  python3-dev -y
sudo /usr/bin/python3 -m pip install sqlalchemy
sudo /usr/bin/python3 -m pip install crossbar==17.6.1-3
sudo /usr/bin/python3 -m pip install autobahn==17.6.2
sudo /usr/bin/python3 -m pip install twisted==17.5.0
sudo /usr/bin/python3 -m pip install tornado==4.4.2
sudo /usr/bin/python3 -m pip install docker-py
sudo apt-get install docker.io
sudo usr/bin/python3 -m pip install psutil simplejson requests

platform='Linux'
