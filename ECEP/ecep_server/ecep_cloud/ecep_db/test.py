from ecep_db.controller import Compute_Manager,Device_Manager,Image_Manager,set_db_session
import json
import logging
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.debug('testing the ecep_db package')
    node = Compute_Manager()

    node.add_new_compute_node(username="chinmayi", containerName="blah")
    node.add_new_compute_node(username="chinmayi", containerName="wwww")
