from botocore.exceptions import ClientError
import boto3, base64, json
#Blah blah blah

region_name = "us-west-1" # Set region Username and Password located in
password = 'password_sql' # Secrets Manager name that has the password

session = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )
with open('file1.txt') as f:
    lines = f.read()

print(lines)

response = session.update_secret(
    SecretId=password,
    Description='some crazy password',
    SecretString=lines
)
