#!/usr/bin/python3.11

import os

from sh import aws

# The local path (local to this scripts dir) to push up
local_directory = "./build/"

# This is the name of the bucket, you can get this from the ARN
# If the ARN is arn:aws:s3:::doc-pr-preview then just doc-pr-preview
bucket = os.getenv("AWS_S3_BUCKET", "")

# The folder in the S3 bucket to write to
destination = os.getenv("DOSSIER_BASE_URL", "")

#aws s3 sync ./build s3://${AWS_S3_BUCKET}/${PR_ID}/ --exact-timestamps --delete --region ${AWS_DEFAULT_REGION} $*
aws.s3.sync(local_directory, 's3://' + bucket + '/' + destination + '/')

