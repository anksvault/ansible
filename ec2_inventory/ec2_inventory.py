#!/usr/bin/python

#-------------------------------------------------------------------------------#
##                                                                             ##
## Author       : Ankit Sharma                                                 ##
## Script       : ec2_inventory.py                                             ##
## Version      : 2.1                                                          ##
## Description  : Fetches EC2 Instances details from AWS                       ##
## Required     : boto3, time, os                                              ##
## Platform     : Python 2.7, 3.x                                              ##
## Execute      : python ec2_inventory.py                                      ##
##                                                                             ##
#-------------------------------------------------------------------------------#

import boto3
import time
import os

start_time = time.time()

# Temp Inventory File
TMP_FILE='/tmp/ec2_inv.ini'

# Regions (Specify your regions in the below list)
regions = ["us-east-1","ap-southeast-1","eu-central-1"]

def get_instance_details(res,reg):
    ctr=0   # Counter for Collected Hosts
    for i in ec2_re.instances.all():
        pvt_ip=i.private_ip_address
        i_type=i.instance_type
        os=i.platform
        i_arch=i.architecture
        tags=i.tags
        hypv=i.hypervisor
        iid=i.id
        i_id=i.instance_id
        i_state=i.state['Name']
        i_img=i.image

        # Get only Running Servers by default - Remove the condition to disable this check.
        if i_state == 'running':
            if os is None:
                os = 'linux'  # This is in place because by default platform field doesn't capture OS info for non windows servers
                # Write Instance Info to the TMP_FILE for linux servers
                with open(TMP_FILE, "a") as f:
                    f.write("\"" +pvt_ip+ "\"" " IPAddress=\"" +pvt_ip+ "\" ansible_host=" +pvt_ip+ " OS=\"" +os+"\"" " InstanceArch=\"" +i_arch+ "\"" " Hypervisor=\"" +hypv+ "\"" " InstanceID=\"" +i_id+ "\"" " Region=\"" +reg+ "\"" "\n")

            else:
                # Write Instance Info to the TMP_FILE for windows servers
                with open(TMP_FILE, "a") as f:
                    f.write("\"" +pvt_ip+ "\"" " IPAddress=\"" +pvt_ip+ "\" ansible_host=" +pvt_ip+ " OS=\"" +os+"\"" " InstanceArch=\"" +i_arch+ "\"" " Hypervisor=\"" +hypv+ "\"" " InstanceID=\"" +i_id+ "\"" " Region=\"" +reg+ "\"" "\n")
            ctr = ctr + 1
    return ctr


## Main Function

# Initialize Boto Session
session=boto3.session.Session()

fc=0  # Counter for total number of hosts 

# Collect Instance information for specified regions
for reg in regions:
    ec2_re=session.resource(service_name='ec2',region_name=reg)
    res=get_instance_details(ec2_re,reg)
    fc = fc + res

print("Collected Hosts: {}".format(fc))
print("Collection Time: %s" % (time.time() - start_time)) # Total time which took the script to fetch info from ec2.

# Below commands are to copy the inventory file into awx_task container and import using awx-manage. Refer Pre-requisites related to this.
os.system("/usr/bin/docker cp /tmp/ec2_inv.ini awx_task:/var/lib/awx/ec2_inv.ini")
os.system("/usr/bin/docker exec awx_task /usr/bin/awx-manage inventory_import --overwrite --inventory-name INV_AWS_EC2 --source /var/lib/awx/ec2_inv.ini")
os.system("/usr/bin/docker exec awx_task rm -f /var/lib/awx/ec2_inv.ini")
os.system("rm -f /tmp/ec2_inv.ini")

# Print total time which the script took to perform all operations.
print("Completion Time: %s" % (time.time() - start_time))