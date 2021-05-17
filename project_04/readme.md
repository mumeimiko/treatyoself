v1.1.1
Release Notes: Python script that checks the pods in a namespace for their statuses and create a list of pods that are healthy and unhealthy. You then have the option to do the following:

1. Ability to terminate the pods not in a ready state
2. Push metrics to CloudWatch

Flow of code:

1. Grab Info from pods in a namespace
2. Then check which pods pods statuses 
  - Pods will be added to an array based if they are in a ready status or not
3. After this, the terminate_flag is checked for the following:
  - True: Will terminate the pods in the namespace that are not in a running state
  - False: Will not terminate the pods
4. Then it will check for the cw_flag flag for the following:
  - True: Will create/update a Cloudwatch Metric with the following: 
        - Create a Custom Namespace in Cloudwatch
        - Will create a Metric Group named NS_default
        - Two metrics are pushed into this metric group:
           1. Pods_Ready
           2. Pods_NotReady
           