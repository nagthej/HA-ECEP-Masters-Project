# High Availability of Edge Computing Embedded Platform using Container Migration 


###File Functions
1. request_handler.py - its tornado REST API request handler. requests from user dashboard is first received to this file for processing the command taking actions accordingly
2. wamp_server.py - its where WAMP messaging server is initilazed and subscriptiion to various topics happens and also has API for pusblishing.
3. update_db.py - its a interface between request_handler.py(which handles user request and calls update_db API to fetch the database info accordingly) and the controller.py(present in ecep_db which performs actual db operations). It also update the database according to the response received from end node (ex:deviceRegister, AddComputeNode)
4. container_control.py- its a helper file to filter and validate request from user dashboard.