#How To Add a User to EKS and Allow Codebuild Access to the EKS Cluster.
# 1 Create a role that CodeBuild will assume to run commands agaisnt EKS
## Create ENV Variable for the CodeBuild Role ARN and the EKS Cluster Role
ACCOUNT_ID='123456789'
CODE_BUILD_ARN='arn:aws:iam::12354689:role/service-role/codebuild-test1-service-role'
CODE_BUILD_NAME='codebuild-test1-service-role'
EKS_ROLE_NAME='EksCodeBuildkubectlRole'
#EKS_ROLE="arn:aws:iam::'$ACCOUNT_ID':role/'$EKS_ROLE_NAME'"
ECHO $EKS_ROLE_NAME

## Create the EKS Roles to be allowed access to from the CodeBuild Role 
EKS_ROLE=$(aws iam create-role --role-name "$EKS_ROLE_NAME" --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"AWS": "'$CODE_BUILD_ARN'"}, "Action": "sts:AssumeRole"}]}' --output text --query 'Role.Arn')
echo $EKS_ROLE

#2 Update Configmap to Allow the EKSRole access to the cluster

ROLE="    - rolearn: '$EKS_ROLE'\n      username: build\n      groups:\n        - system:masters"; kubectl get -n kube-system configmap/aws-auth -o yaml | awk "/mapRoles: \|/{print;print \"$ROLE\";next}1" > /tmp/aws-auth-patch.yml
cat /tmp/aws-auth-path.yml

## Patch EKS 
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"

#3 Create Policy and attach to codebuild role 
cat <<EOF > policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EKSREADONLY",
            "Effect": "Allow",
            "Action": [
                "eks:DescribeNodegroup",
                "eks:DescribeUpdate",
                "eks:DescribeCluster"
            ],
            "Resource": "*"
        },
        {
            "Sid": "STSASSUME",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "$EKS_ROLE"
        }
    ]
} #Contents Truncated
EOF

# create policy
aws iam create-policy --policy-name ekscode --policy-document file://policy.json
# attach role
aws iam attach-role-policy --role-name $CODE_BUILD_NAME --policy-arn arn:aws:iam::$ACCOUNT_ID:policy/ekscode