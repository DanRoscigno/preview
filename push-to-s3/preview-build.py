#!/usr/bin/python3.11

import os
import sys
import boto3

# These first two vars are the auth that we pass to create 
# the boto3 client
AWS_ACCESS_KEY_ID = os.getenv("AWS_S3_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_S3_KEY_SECRET")

# This is the name of the bucket, you can get this from the ARN
# If the ARN is arn:aws:s3:::doc-pr-preview then just doc-pr-preview
bucket = os.getenv("AWS_S3_BUCKET")

# The local path (local to this scripts dir) to push up
local_directory = "./build"

# The folder in the S3 bucket to write to
destination = '/' + os.getenv("DOSSIER_BASE_URL", "") + '/'


client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# enumerate local files recursively
for root, dirs, files in os.walk(local_directory):

  for filename in files:

    # construct the full local path
    local_path = os.path.join(root, filename)

    # construct the full Dropbox path
    relative_path = os.path.relpath(local_path, local_directory)
    s3_path = os.path.join(destination, relative_path)

    # relative_path = os.path.relpath(os.path.join(root, filename))

    print ('Searching "%s" in "%s"' % (s3_path, bucket))
    try:
        client.head_object(Bucket=bucket, Key=s3_path)
        print ("Path found on S3! Skipping %s..." % s3_path)

        # try:
            # client.delete_object(Bucket=bucket, Key=s3_path)
        # except:
            # print ("Unable to delete %s..." % s3_path)
    except:
        print ("Uploading %s..." % s3_path)
        client.upload_file(local_path, bucket, s3_path)

'''
name: CI
on: [pull_request]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
        with:
          fetch-depth: 0
          
      - name: Setup Environment
        run: |
          export PREVIEW_BRANCH_DIR=$(echo $GITHUB_HEAD_REF | sed -e 's#^refs/heads/##; s#[^0-9a-zA-Z-]#-#g')
          echo "PREVIEW_BRANCH_DIR=$PREVIEW_BRANCH_DIR" >> $GITHUB_ENV

          export PR_NUMBER=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')
          echo "PR_NUMBER=$PR_NUMBER" >> $GITHUB_ENV      
      
      - name: build
        env:
          DOSSIER_BASE_URL: /${{ env.PREVIEW_BRANCH_DIR }}/
          AWS_DEFAULT_REGION: "us-east-1"
          AWS_S3_BUCKET: "doc-pr-preview"
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_BUCKET_ACCESS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_BUCKET_ACCESS_SECRET }}
          PR_ID: ${{ env.PREVIEW_BRANCH_DIR }}
        run: |
          mkdir -p ~/.aws
          touch ~/.aws/credentials
          echo "[default]
          aws_access_key_id = ${AWS_ACCESS_KEY_ID}
          aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}" > ~/.aws/credentials

          npm install -g yarn
          yarn install
          yarn build
          
          echo "Copying to website folder"
          aws s3 sync ./build s3://${AWS_S3_BUCKET}/${PR_ID}/ --exact-timestamps --delete --region ${AWS_DEFAULT_REGION} $*
          
          echo "Cleaning up things"
          rm -rf ~/.aws

      - name: Report
        env:
          GITHUB_TOKEN: ${{ secrets.PAT_WRITE_PR_COMMENTS }}
          PR: ${{ env.PR_NUMBER }}
        run: gh pr comment $PR --body "Preview is at https://d2dc3wdr1yqzl7.cloudfront.net/${{ env.PREVIEW_BRANCH_DIR }}/ "
'''


