# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc.small" 
private_net = "UPPMAX 2025/1-2 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 20.04 - 2023.12.07"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")

worker_name = sys.argv[1]

if key == None:
    sys.exit("key not defined.")

cfg_file_path =  os.getcwd()+f'/{worker_name}-cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_prod = open(cfg_file_path)
else:
    sys.exit(f'/{worker_name}-cloud-cfg.txt is not in current working directory') 

secgroups = ['default']

print ("Creating instance ... ")
instance_work = nova.servers.create(name=f"{worker_name}_group13_"+str(identifier), image=image, flavor=flavor, key_name='PRJ_Group13',userdata=userdata_prod, nics=nics,security_groups=secgroups)
inst_status_work = instance_work.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_work == 'BUILD':
    print ("Instance: "+instance_work.name+" is in "+inst_status_work+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_work = nova.servers.get(instance_work.id)
    inst_status_work = instance_work.status

ip_address_work = None
for network in instance_work.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_work = network
        break
if ip_address_work is None:
    raise RuntimeError('No IP address assigned!')


print ("Instance: "+ instance_work.name +" is in " + inst_status_work + " state" + " ip address: "+ ip_address_work)

# Add worker to [rayworkers] in etc/ansible/hosts
# The file is in root and require sudo to edit

## check if line [rayworkers] exists in /etc/ansible/hosts using regex
## if not, add it

# save the output of the command to a variable
output = os.popen('sudo sh -c "cat /etc/ansible/hosts"').read()
output = output.splitlines()
exists = False
for i in range(len(output)):
    if output[i] == '[rayworkers]':
        print('rayworkers-group exists, appending worker to it')
        exists = True
        break

if not exists:
    os.system(f'sudo sh -c "echo [rayworkers] >> /etc/ansible/hosts"')
    
os.system(f'sudo sh -c "echo \'{worker_name} ansible_host={ip_address_work} ansible_connection=ssh ansible_ssh_user=appuser\' >> /etc/ansible/hosts"')