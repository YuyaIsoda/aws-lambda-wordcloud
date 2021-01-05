#!/bin/sh
# Activate Python & Serverless
source bin/activate

# Setup installed library for AWS Lambda
npm install --save serverless-python-requirements
# npm install --save serverless-api-gateway-caching

# Install library
pip install boto3 requests logger wordcloud
pip freeze | grep "requests" > requirements.txt

# Install library for Pandas on AWS (AWS Data Wrangler)
# pip3 install pandas awswrangler

# Deactivate Python & Serverless
deactivate
