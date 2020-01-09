**Pre-Requisites**

Following pre-requisites should be satisfied before using this script.

1. An Empty Inventory is created for the script to run import
2. `boto3` should be already installed and configured in the AWX/Ansible Server
3. Script should be executed in the Ansible/AWX server
4. Validate and update paths, values in the script wherever required as per your environment

----

**Installation Steps**

**Step 1:** Check-in the python script in your repo.

**Step 2:** Create an empty inventory in AWX (where you want to import the inventory file created by the script).

**Step 3:** Create a Job template in AWX to run the python script and ensure that you are targetting the host server where your AWX containers resides. You can also execute this directly inside the awx_task container using the interal container IP Address.

**Step 4:** Execute the Job template.
