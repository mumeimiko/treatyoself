Project 1

How To Add a User to EKS and Allow Codebuild Access to the EKS Cluster.

As I am working on random things, I wanted to run codebuild to run kubectl commands for me without using the EKS creator role. So in order to do this I need to do the following:

1. Create an EKS Role that codebuild can use via Admin Role
2. Then to run kubectl commands within Codebuild, I need to attach permissions to the CodeBuild Role
3. Run codebuild in a Amazon Linux 2 Environment and run commands agaisnt my EKS cluster

You would first need to:

1. Edit the bash.sh environmental values
2. Run the bash script with the Admin Role and a role that has access to write/create IAM policies 
3. Use the buildspec.yaml file in your codebuild. 
