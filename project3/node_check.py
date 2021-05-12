# v.1.1.3
# Release Notes: Added termination flag and CW Flag 
from kubernetes import client, config

import json
import array
import boto3
import re

# globs
ec2 = boto3.client('ec2')
cwatch = boto3.client('cloudwatch')
kubecfg = config.load_kube_config()
k8s_api = client.CoreV1Api()
list_node = k8s_api.list_node(watch=False, _preload_content=False)
http_decode = list_node.data.decode('utf8')
terminate_flag = False # If set to True, ASG nodes will be marked for termination
cw_flag = False # If set to True, CW Metrics will be pushed. 
# 19-54 eval logic

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
            status = i['status']['conditions']
            for i in status:
                if i['type'] == 'Ready':
                    if i['reason'] == 'NodeStatusUnknown':
                        node_info = {
                            'instance_id': instance_id,
                            "health_status": i['reason']
                        }
                        unhealthy_nodes.append(node_info)
                    elif i['reason'] == 'KubeletReady':
                        node_info = {
                            'instance_id': instance_id,
                            "health_status": i['reason']
                        }
                        healthy_nodes.append(node_info)
                else:
                    pass
    determine_health(
        unhealthy_nodes,
        healthy_nodes
    )

# 56-64 determines what node to terminate

def determine_health(unhealthy_nodes, healthy_nodes):
    global unhealthyfoos, healthyfoos
    uh_nodes_count = len(unhealthy_nodes)
    unhealthyfoos = len(unhealthy_nodes)
    healthyfoos = len(healthy_nodes)
    print(f'These nodes are currently healthy: {healthy_nodes}')
    print(f'These nodes are currently unhealthy: {unhealthy_nodes}')
    if uh_nodes_count != 0:
        print(f'there is {uh_nodes_count} unhealthy nodes')
        if terminate_flag == True:
            ec2_asg_call(unhealthy_nodes)
        else:
            print("Skipping Termination of nodes")
    else:
        print(f'there are {uh_nodes_count} unhealthy nodes, nothing to do')

# 69-81 this is only called when there is unhealthy nodes, terms in a batch


def ec2_asg_call(unhealthy_nodes):
    instance_ids = []
    for i in unhealthy_nodes:
        instance_ids.append(i['instance_id'])
    response = ec2.terminate_instances(
        InstanceIds=instance_ids,
        DryRun=False
    )
    print(f'Terminating the following nodes: {instance_ids}')

def input_metrics(unhealthyfoos,healthyfoos):
    if cw_flag == True:
        print("Pushing Cloudwatch Metrics")
        cwatch.put_metric_data(
            Namespace='MyService',
            MetricData=[
                {
                    'MetricName': 'NotReady_Check',
                    'Dimensions': [
                        {
                            'Name': 'EKS_Cluster',
                            'Value': 'NotReady'
                        },
                    ],
                    'Value': unhealthyfoos,
                    'Unit': 'Count'

                },
            ]
        )
        cwatch.put_metric_data(
            Namespace='MyService',
            MetricData=[
                {
                    'MetricName': 'Ready_Check',
                    'Dimensions': [
                        {
                            'Name': 'EKS_Cluster',
                            'Value': 'Ready'
                        },
                    ],
                    'Value': healthyfoos,
                    'Unit': 'Count'

                },
            ]
        )
    else:
        print("Skip Pushing CW Metrics")

if __name__ == "__main__":
    node_status(http_decode)
    input_metrics(unhealthyfoos,healthyfoos)
