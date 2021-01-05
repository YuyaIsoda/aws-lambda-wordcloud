#!/usr/bin/env python
# encoding: utf-8

# Common Lib
from aws_common import *

# General Lib
import io
import boto3
import collections

# Additional Lib
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# User Lib
from h_conf import *
#####  #####  #####  #####

# AWS Services
## AWS Glue: Data Catalog
glue = boto3.client('glue')

def glue_get_databases():
    res = glue.get_databases()
    glue_database_list = res['DatabaseList']
    while 'NextToken' in res:
        res = glue.get_databases(NextToken=res['NextToken'])
        glue_database_list += res['DatabaseList']
    return glue_database_list

def glue_get_tables(DatabaseName):
    res = glue.get_tables(DatabaseName=DatabaseName)
    glue_table_list = res['TableList']
    while 'NextToken' in res:
        res = glue.get_tables(DatabaseName=DatabaseName, NextToken=res['NextToken'])
        glue_table_list += res['TableList']
    return glue_table_list

## AWS S3
s3 = boto3.client('s3')

def s3_put_object(Bucket, Key, Body):
    res = s3.put_object(Bucket=Bucket, Key=Key, Body=Body)
    return res

def s3_put_object_public_url(Bucket, Key):
    try:
        # PERMIT Public Access
        s3_res = s3.put_object_acl(Bucket=Bucket, Key=Key, ACL="public-read")
        s3_url = "https://{0}.s3.amazonaws.com/{1}".format(Bucket, Key)
    except:
        s3_url = "none"
    return s3_url

# WordCloud Functions
def get_aws_glue_catalog_tags():
    tags = {}
    dbs = glue_get_databases()
    for db in dbs:
        tags.update( { db['Name']: {} } )
        tbls = glue_get_tables(DatabaseName=db['Name'])
        for tbl in tbls:
            tags[db['Name']].update( { tbl['Name']: {} } )
            tags[db['Name']][tbl['Name']].update(tbl['Parameters'])
            if 'Parameters' in tbl['StorageDescriptor'].keys():
                tags[db['Name']][tbl['Name']].update(tbl['StorageDescriptor']['Parameters'])
        logging.debug(pprint.pformat(tags[db['Name']]))
    return tags

def count_aws_glue_catalog_tags(tags, db):
    clist = []
    for tbl in tags[db].keys():
        for key in tags[db][tbl].keys():
            val = tags[db][tbl][key]
            # val = key
            # val = key + '_' + val
            clist.append(val)
    return collections.Counter(clist)

def create_wordcloud(tags):
    # Select a mask of wordcloud
    MaskPath = "mask/" + WCMask + ".png"
    mask = np.array(Image.open(MaskPath))

    # Setup wordcloud
    wordcloud = WordCloud(width=480, height=320, scale=2, max_words=50, mask=mask, contour_width=2, contour_color='steelblue', background_color='white', colormap='winter')

    # Tag Count
    for db in tags.keys():
        # Count Tag
        cnt = count_aws_glue_catalog_tags(tags=tags, db=db)
        if len(cnt.keys()) == 0:
            continue

        # Archive Count
        Key = "wordcloud/aws_glue/data_catalog/" + strtime + "/counts_" + db + ".json"
        s3_put_object(Bucket=Bucket, Key=Key, Body=json_dumps(data=cnt))

        # Create WordCloud
        wordcloud.fit_words(cnt)
        # wordcloud.to_file('wdtest.png') # Output: Local

        # Get Image Body Data
        img = wordcloud.to_image()
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='PNG')
        imgbody = imgByteArr.getvalue()

        # Output: AWS S3
        Key = "wordcloud/aws_glue/data_catalog/" + strtime + "/wordcloud_" + db + ".png"
        s3_put_object(Bucket=Bucket, Key=Key, Body=imgbody)
        logging.debug('Path: ' + Key)

        # Public Access
        # url = s3_put_object_public_url(Bucket=Bucket, Key=Key)
        # logging.info(url)
    return None
