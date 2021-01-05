#!/usr/bin/env python
# encoding: utf-8

# Common Lib
from aws_common import *

# General Lib
# Additional Lib

# User Lib
from h_conf import *
from h_wordcloud import *
#####  #####  #####  #####

# Main Function
def m_create_wordcloud(event, context):
    # Get AWS Glue Catalog Tags
    tags = get_aws_glue_catalog_tags()

    # Archive AWS Glue Catalog Tags
    Key = "wordcloud/aws_glue/data_catalog/" + strtime + "/all_tags.json"
    s3_put_object(Bucket=Bucket, Key=Key, Body=json_dumps(data=tags))

    # Create wordcloud
    create_wordcloud(tags=tags)
    return respond(StatusCode=200, Body={'input': None, 'output': None, 'body': None})

if __name__ == "__main__":
    m_create_wordcloud('', '')
