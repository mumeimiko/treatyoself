#Author Mumeimiko Email@michael.zng@yahoo.com
#tl:dr check kubernetes nodes from k8s and marks them as unhealthy and delete them
#v.1.1.0
from kubernetes import client, config
import json, array, boto3

client2 = boto3.client('autoscaling')
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
bad_nodes = []
good_nodes = []
v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_node(watch=False)
for i in ret.items:
    
    node = i.metadata.name
    print( f'Node in question: {i.metadata.name} ')
    print( f'EC2 in question: {i.spec.provider_id} ')
    if "fargate" in i.spec.provider_id:
        print("This is a fargate node")
    else:
        print("this is an ec2 instance")
        ec2_node = i.spec.provider_id.split("/", 4)
        node = ec2_node[4]
    test = i.status.conditions[-1:]
    #print( test )
    test2=str(test)
    status = (test2.splitlines()[4])
    type = (test2.splitlines()[5])
    #print (status)
    #print (type)
    if "True" in status:
        print ('Node Currently is in a Ready Status')
        good_nodes.append(node)
    else:
        print ('Node Currently is having issues')
        bad_nodes.append(node)
    #print (i)
print("Currently the good nodes are:")
print (good_nodes)

print("Currently the bad nodes are:")
print (bad_nodes)
#print (bad_nodes[0])
response = client2.set_instance_health(
    HealthStatus='Unhealthy',
    InstanceId=bad_nodes[0],
    ShouldRespectGracePeriod=False
)

print(response)
""" test2=str(test)
    print (test2)
    lastline = test2[-5]
    print (lastline)"""



#cordon https://www.programcreek.com/python/example/96328/kubernetes.client.CoreV1Api

#
#
#
