#!/bin/sh
# Activate Python & Serverless
source bin/activate
source ./sls_conf

# Create Log Dir
mkdir -p ~/${SLSDIR}/log

# Delete AWS Lambda Functions
LOGFILE=${ServiceName}_${Region}_$(date "+%Y%m%d_%H%M%S")_remove.log
sls remove > ~/${SLSDIR}/log/$LOGFILE
cat ~/${SLSDIR}/log/$LOGFILE

# Deactivate Python & Serverless
deactivate
