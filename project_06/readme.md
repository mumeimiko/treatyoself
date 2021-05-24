# I wanted to create a codepipeline that will update my root password for my MYSQL database. This is a continuation of my project_05 and actually impementing it in an environment through a pipeline. The pipeline does the following

1. Update the password on Secrets Manager
2. Pull the new password from Secrets Manager and update the Kubernetes Secret
3. Redeploy my MYSQL database with the new password 

As you can see with the screenshots, I was able to update the k8s secret and run a test pod to echo the values of the username and passsword. Then launch a mysql pod client that connects to the database using the password(hard coded ATM) And voila!

#k8ssecurity #awssecurity #secretsmanager #devops #deployment #eks #python #kubernetes #codesuite
