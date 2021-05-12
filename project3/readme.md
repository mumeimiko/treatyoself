tl;dr liked the original script, made some slight changes to the syntax / structure while keeping the core logic intact
This script does the following, in order:

1. Retrieve the RAW HTTP response object from the V1ListNode api
2. Decode the response object into utf8
3. load the object into json so that we can work directly with the keys
4. iterate over the array of node objects and skips the fargate nodes
5. for ec2 nodes, it pulls the instanceID from the providerID key nested within `spec` 
6. for the same node object, it will then determine the status of the node and append it to a relevant list
7. once the lists are fully popluated and we've iterated across all of the nodes, it makes a call to a function to evaluate health
8. this function starts by printing healthy nodes, and if the length of the unhealthy nodes array isn't equal to 0 it calls a function to terminate the instances 
9. the function to terminate is only called when there is unhealthy instances, instead of making 1 api call for each instance in the list, I batched them and instead call the `terminate_instances` method so that we can terminate the unhealthy nodes in one go (this reduces the number of API calls made)

1.1.3 Release Notes

1. Added Termination Flag:
  - If set to true, Nodes are Marked for termination on the ASG.
  - If set to False, Nodes are not marked for termination on the ASG
2. Added a CloudWatch Flag which allows you to push CW metrics based on Ready and Not Ready Statuses on the Nodes 
  - This in turn can be added as a CloudWatch alarm to trigger when a node is not passing its health checks 

Notes:

By default, both Flags are set to false to give you the ability to either terminate the nodes immediately or raise an alarm to investigate the node in question for any issues that you can try to remediate. 
