# High Availability of Edge Computing Embedded Platform using Container Migration 
Project aims at providing a common platform for edge computing applications such as video analytics, smart city and supports both CPU and GPU application upload.
Deploy a webserver and launch user dashboard through this repo.

### Hardware Requirements: 
AWS or any cloud server (ex:ubuntu ec2 instance in AWS)
Please add your respective public IP for the port 9000, 8096, HTTP, ssh to allow access from AWS 
ec2 inbound security rules

### Software Requirements: 
**Server:** 
* Crossbar, Used for wamp messaging. Libraries to be installed are crossbar.io, autobahn, twisted.

      `pip install crossbar autobahn`
      
* node.js has to installed to run the Dashboard.

      `curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -`
      `sudo apt-get install -y nodejs`

  optional - `sudo apt-get install -y build-essential`
  
* DB : sqlite, DB packages: SQLAlchemy

      `apt-get install sqlite` for debian


# Run install_dependencies.sh with sudo command to install all the required packages.
# Then run ecep_server.sh

# The current software is tested on Python3.


###Folder organisation
1. install_dependency.sh - its the library dependencies required for the platform to be run. Execute on the machine which will act as platform server.
2. demo.db - its the database which gets created once platform server is running
3. ecep_server.sh - its the shell script which we need to execute to start the platform server code.
4. ecep_cloud - Source folder for server side.