#project 00

I noticed that alot of people reached out asking how to create a pipeline. So in short, I created project 00 that would create a pipeline that you can simply just upload your files to a repo and codepipeline takes care of the test. 

You will do the following:

1. Create a CodeCommit Repo 
2. Create a CodeBuild
3. Create a Pipeline to use both 

1. Create a CodeCommit Repo

1. Go to Codecommit -> Create Repository 
  - Repository Name: staging
  Then go to Code and then upload the file in project_00/buildspec.yaml
2. Go to CodeBuild -> Create Build Project 
  - Project Name: staging_build
  - Source:
    Source Provider: AWS CodeCommit
    Repository: Staging
    Branch: Main
  - Environment
    Managed Image
      - Operating System: Amazon Linux 2 
      - Runtime: Standard
      - Image: Standard 3.0 x86
      - Privileged: Enabled
      - New Service Role
      - Role Name: codebuild-staging_build-service-role
    BuildSpec 
      - UseBuildSpec File
    Logs
      - CloudWatch Logs: Enabled(if applicable)
3. Go to CodePipeline -> Create Pipeline
  - Step 1
    - Pipeline name: staging_pipeline
    - RoleName: AWSCodePipelineServiceRole-us-east-1-staging_pipeline
    - Leave Everything default
  - Step 2
    - Source Provider: AWS CodeCommit
    - Repository Name: staging
    - Branch Name: main
  - Step 3
    - Build Provider: AWS Codebuild
    - Project Name: staging_build
  - Step 4
    - Skip Deploy
    - At the moment, focusing on building things and then deploy into an environment. 
  - Step 5 
    - Create

You should now see your pipeline working, you should see source and build succeeding. 
