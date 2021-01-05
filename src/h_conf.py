#!/usr/bin/env python
# encoding: utf-8

# Common Lib
from aws_common import *

# Enviroment Value: Setting
Region  = os.getenv('Region', None)
Bucket  = os.getenv('Bucket', None)
WCMask  = os.getenv('WCMask', 'cloud')
dtime   = datetime.date.today()
#dtime   = datetime.datetime.now()
strtime = dtime.strftime('%Y-%m-%d-%H-%M-%S')

