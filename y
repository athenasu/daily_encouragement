version = 0.1
[default.deploy.parameters]
stack_name = "daily-encouragement"
resolve_s3 = true
s3_prefix = "daily-encouragement"
region = "us-west-2"
profile = "default"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []
