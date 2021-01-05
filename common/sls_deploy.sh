#!/bin/sh
# Activate Python & Serverless
source bin/activate
source ./sls_conf

# Create Log Dir
mkdir -p ~/${SLSDIR}/log

# Check Serverless Framework
LOGFILE=${ServiceName}_${Region}_$(date "+%Y%m%d_%H%M%S").yml
sls print > ~/${SLSDIR}/log/$LOGFILE
cat ~/${SLSDIR}/log/$LOGFILE

# Deploy AWS Lambda Functions
LOGFILE=${ServiceName}_${Region}_$(date "+%Y%m%d_%H%M%S")_deploy.log
sls deploy -v > ~/${SLSDIR}/log/$LOGFILE
cat ~/${SLSDIR}/log/$LOGFILE

# Deactivate Python & Serverless
deactivate
