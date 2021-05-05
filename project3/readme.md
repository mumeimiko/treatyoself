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

