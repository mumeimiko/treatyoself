from kubernetes import client, config
from botocore.exceptions import ClientError
import boto3, base64, json
#Blah blah blah
kubecfg = config.load_kube_config()
k8s_api = client.CoreV1Api()
sec  = client.V1Secret()
k8s_namespace = 'default'
region_name = "us-west-1" # Set region Username and Password located in
username = 'username_sql' # Secrets Manager name that has the username
password = 'password_sql' # Secrets Manager name that has the password
print("testing!!")
def get_secret(): #Grab Username/Password from Secret Manager
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        print("Grabbing Username & Password from Secrets Manager")
        get_secret_value_response_1 = client.get_secret_value(
            SecretId=username
        )
        get_secret_value_response_2 = client.get_secret_value(
            SecretId=password
        )   
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        if 'SecretString' in get_secret_value_response_1:
            secret_usr = get_secret_value_response_1['SecretString']
            secret_pwd = get_secret_value_response_2['SecretString']
            create_secret_agent(secret_usr,secret_pwd) 
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response_1['SecretBinary'])

def create_secret_agent(secret_usr,secret_pwd): #Creates k8s Secrets based on the values grabbed from Secrets Manager
    print("Creating k8s Secret")
    print(secret_usr)
    print(secret_pwd)
    sec.metadata = client.V1ObjectMeta(name="mysecret") #name of the secret that will be created is
    sec.type = "Opaque"
    sec.data = {"username": secret_usr, "password": secret_pwd}
    k8s_api.replace_namespaced_secret(name="mysecret",namespace=k8s_namespace, body=sec)
if __name__ == "__main__":
    get_secret()