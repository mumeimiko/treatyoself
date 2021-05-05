#v.1.1.2
from kubernetes import client, config

import json 
import array 
import boto3 
import re
import pprint

#8-13 Getting stuff ready 
ec2 = boto3.client('ec2')
kubecfg = config.load_kube_config()
k8s_api = client.CoreV1Api()
list_node = k8s_api.list_node(watch=False, _preload_content=False)
http_decode = list_node.data.decode('utf8')
pp = pprint.PrettyPrinter(indent=4)

#15-39 For loop that looks at each node 
def node_status(http_decode):
    unhealthy_nodes = []
    healthy_nodes = []
    dict_obj = json.loads(http_decode)
    data = dict_obj['items']
    for i in data:
        node_info = {'instance_id': '', 'health_status': ''}
        k8s_node = i['metadata']['name']
        if re.search("fargate", k8s_node):
            pass
        else:
            provider_id = i['spec']['providerID'].split("/", 4)
            instance_id = provider_id[4]
            status = i['status']['conditions'][3]
            if status['status'] == 'True':
                node_info = {'instance_id': instance_id, "health_status": status['reason']}
                healthy_nodes.append(node_info)
            else:
                node_info = {'instance_id': instance_id, "health_status": status['reason']}
                unhealthy_nodes.append(node_info)
    determine_health(unhealthy_nodes, healthy_nodes)

def determine_health(unhealthy_nodes, healthy_nodes):
    print(f'These nodes are currently healthy: {healthy_nodes}')
    if len(unhealthy_nodes) != 0:
        print(f'there is {len(unhealthy_nodes)} unhealthy nodes, terminating them')
        ec2_asg_call(unhealthy_nodes)
    else:
        print(f'there are {len(unhealthy_nodes)} unhealthy nodes, nothing to do')

#48-57 Marking the nodes as unhealthy via the ASG
def ec2_asg_call(unhealthy_nodes):
    instance_ids = []
    for i in unhealthy_nodes:
        instance_ids.append(i['instance_id'])
    print(f'There is {len(instance_ids)} to terminate')
    response = client.terminate_instances(
        InstanceIds=[
        'string',
        ],
        DryRun=False
    )
    print(f"Terminating: {instance_ids}" )
