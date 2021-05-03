So tl:Dr i noticed that EKS doesn't monitor the health of an EKS node from a Kubernetes standpoint. 

So I decided to create a python script that does the following:

1. Run a loop to gather nodes information
2. In the loop, grab the instance_id and the current status from a kubernetes standpoint(Ready or not ready)
3. Runs it runs through the loop, it will mark the not ready nodes as unhealthy from an ASG standpoint.
4. At this point it will terminate the the node and launch a new node in its place.
