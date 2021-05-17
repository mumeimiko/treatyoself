# v1.1.1
# Release Notes: PYthon scripts that checks the pods in a namespace for their statuses and create a list of pods that are healthy and unhealthy
# 1. Ability to terminate the pods not in a running status
# 2. Push metrics to CloudWatch
 
from kubernetes import client, config
import json
import array
import boto3
import re
# blah blah
config.load_kube_config()
ec2 = boto3.client('ec2')
cwatch = boto3.client('cloudwatch')
eks_namespace = "default" #Namespace you want to monitor pods in
terminate_flag = False # If set to True, pods will be marked for termination
cw_flag = False # If set to True, CW Metrics will be pushed. 
k8s_api = client.CoreV1Api()
pod_list = k8s_api.list_namespaced_pod(eks_namespace,_preload_content=False) #Grabs pods info from the namespace
http_decode = pod_list.data.decode('utf8')

def pod_status(http_decode): # Check status of the pods
    unhealthy_pods = []
    healthy_pods = []
    dict_obj = json.loads(http_decode)
    data = dict_obj['items']
    for i in data:
        pod_info = i['metadata']['name']
        pod_status = i['status']['phase']
        print(pod_info)
        print(pod_status)
        if i['status']['phase'] == 'Running':
            healthy_pods.append(pod_info)
        else:
            unhealthy_pods.append(pod_info)
    determine_health(
        unhealthy_pods,
        healthy_pods
    )           
def determine_health(unhealthy_pods, healthy_pods):
    global unhealthyfoos, healthyfoos
    uh_pods_count = len(unhealthy_pods)
    unhealthyfoos = len(unhealthy_pods)
    healthyfoos = len(healthy_pods)
    print(f'These pods are currently healthy: {healthy_pods}')
    print(f'These pods are currently unhealthy: {unhealthy_pods}')
    if uh_pods_count != 0:
        print(f'There are {uh_pods_count} unhealthy pods')
        if terminate_flag == True:
            for i in range(len(unhealthy_pods)):
                k8s_api.delete_namespaced_pod(unhealthy_pods[i],eks_namespace)
                print(f'Terminated Pod {unhealthy_pods[i]}')
                i += 1
        else:
            print("Skipping Termination of pods")
    else:
        print(f'there are {uh_pods_count} unhealthy pods, nothing to do')

def input_metrics(unhealthyfoos,healthyfoos):
    if cw_flag == True:
        print("Pushing Cloudwatch Metrics")
        cwatch.put_metric_data(
            Namespace='EKS_Cluster1',
            MetricData=[
                {
                    'MetricName': 'Pod_NotReady',
                    'Dimensions': [
                        {
                            'Name': 'NS_'+eks_namespace,
                            'Value': 'Pod_NotReady'
                        },
                    ],
                    'Value': unhealthyfoos,
                    'Unit': 'Count'

                },
            ]
        )
        cwatch.put_metric_data(
            Namespace='EKS_Cluster1',
            MetricData=[
                {
                    'MetricName': 'Pod_Ready',
                    'Dimensions': [
                        {
                            'Name': 'NS_'+eks_namespace,
                            'Value': 'Pod_Ready'
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
    pod_status(http_decode)
    input_metrics(unhealthyfoos,healthyfoos)
