#!/usr/bin/env python
# encoding: utf-8
import sys, os
import json
import time
import datetime
import logging
import pprint
sys.path.append('..')

# Additional: https://github.com/UnitedIncome/serverless-python-requirements
try:
    import unzip_requirements
except ImportError:
    pass

import requests

# Log setting
logging.basicConfig(level=logging.INFO)

# Env
os.environ['AWS_DEFAULT_REGION'] = os.getenv('Region', None)
#####  #####  #####  #####

# Common Functions
## JSON
def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def json_dumps(data):
    return json.dumps(data, default=json_serial, ensure_ascii=False)

## EC2
def ec2_get_public_ip():
    url = 'http://checkip.amazonaws.com'
    res = requests.get(url)
    return res.text.split()[0]

## Lambda: Input
def handler_get_parameter(event, context, Key):
    if Key in event: # ex. sls invoke -f {lambda function} --log -d '{"test":"100"}'
        return event[Key]

    elif 'httpMethod' in event: # HTTP Request
        if event['body'] != None and Key == 'Body': # ex. curl -X POST {API URL} -d '{"test":"100"}'
            if not (isinstance(event['body'], (dict, list))):
                return json.loads(event['body'])
            else:
                return event['body']

        if event['pathParameters'] != None: # ex. curl -X GET {API URL}/{test1}/{test2}
            if Key in event['pathParameters']:
                return event['pathParameters'][Key]

        if event['queryStringParameters'] != None: # ex. curl -X GET {API URL}?test=100
            if Key in event['queryStringParameters']:
                return event['queryStringParameters'][Key]

    if os.environ.get(Key, 'None') != 'None': # Lambda Environment
        return os.environ.get(Key)
    return None

def handler_get_parameters(event, context, Input):
    keys = Input.keys()
    for key in keys:
        Value = handler_get_parameter(event=event, context=context, Key=key)
        if Value != None:
            Input[key] = Value
        elif Input[key] == None:
            raise ValueError('Input Error')
    logging.debug('AWS Lambda: Input: ' + pprint.pformat(Input))
    return Input

## Lambda: Output
def respond(StatusCode, Body):
    body = {
        'statusCode': StatusCode,
        'body': json_dumps(Body),
        'headers': {
            'Access-Control-Allow-Origin' : '*',
            'Content-Type': 'application/json'
        }
    }
    logging.debug('AWS Lambda: Output: ' + pprint.pformat(body))
    return body
