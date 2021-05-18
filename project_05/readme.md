# project 5

I wanted to create a python script that does the following:
1. Grab two Secrets(Username/Password) from Secret Manager that are encoded in base64
2. Then create a secret in k8s named "mysecret" in the declared namespace(set to default) that will inject the username and password grabbed from Secret Manager

I created a quick pod manifest(test1.yaml) that will launch a busybox container that will intake the secret I created from the python script and mount it in a path declared

As you can see from the screenshots, I was sucessfull