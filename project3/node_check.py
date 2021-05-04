#Author Mumeimiko Email@ mumeimiko@yahoo.com
#tl:dr check kubernetes nodes from k8s and marks them as unhealthy and delete them
#v.1.1.2
from kubernetes import client, config
import json, array, boto3

#8-13 Getting stuff ready 
client2 = boto3.client('autoscaling')
config.load_kube_config()
bad_nodes = []
good_nodes = []
v1 = client.CoreV1Api()
ret = v1.list_node(watch=False)

#15-39 For loop that looks at each node 
for i in ret.items:
    
    node = i.metadata.name
    print( f'EKS Node in question: {i.metadata.name} ')
    print( f'EC2 in question: {i.spec.provider_id} ')
    if "fargate" in i.spec.provider_id:
        print("This is a fargate node, ignoring")
    else:
        print("EC2 Node")
        #Locates the instance id
        ec2_node = i.spec.provider_id.split("/", 4)
        node = ec2_node[4]
    #29-32 Grab the Node Status from an EKS Standpoint
    test = i.status.conditions[-1:]
    test2=str(test)
    status = (test2.splitlines()[4])
    type = (test2.splitlines()[5])
    #24-39 Will append the node to the Bad/Good Node List
    if "True" in status:
        print ('Node Currently is in a Ready Status')
        good_nodes.append(node)
    else:
        print ('Node Currently is having issues')
        bad_nodes.append(node)
#41-45 print the current nodes
print("Currently the good nodes are:")
print (good_nodes)

print("Currently the bad nodes are:")
print (bad_nodes)

#48-57 Marking the nodes as unhealthy via the ASG
if len(bad_nodes) == 0:
    print("All nodes are marked as Ready")
else:
    for i in len(bad_nodes):
        client2.set_instance_health(
            HealthStatus='Unhealthy',
            InstanceId=bad_nodes[i],
            ShouldRespectGracePeriod=False
        )
        print("Terminating: " + bad_nodes[i] )
