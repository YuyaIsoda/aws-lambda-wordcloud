#!/bin/sh
DIR=$(cd $(dirname $0); pwd)
source ../conf/sls_conf

# Create service directory
mkdir -p ~/${SLSDIR}/${ServiceName}

# Delete old service
cd ~/${SLSDIR}/${ServiceName}; sh sls_remove.sh;
rm -rf ~/${SLSDIR}/${ServiceName}

# Create new service using Serverless Framework
cd ~/${SLSDIR}
serverless create --template aws-python3 --name ${ServiceName} --path ${ServiceName}

# Copy files
cd ${DIR}; cd ../
cp -r common/* ~/${SLSDIR}/${ServiceName}
cp -r conf/* ~/${SLSDIR}/${ServiceName}
cp -r src/* ~/${SLSDIR}/${ServiceName}
cp -r mask ~/${SLSDIR}/${ServiceName}

# Show directory tree
cd ~/${SLSDIR}/${ServiceName}
pwd; find . | sort | sed '1d;s/^\.//;s/\/\([^/]*\)$/|--\1/;s/\/[^/|]*/|  /g'

# Create Virtual Enviroment for Python
cd ~/${SLSDIR}
python3 -m venv ${ServiceName}

# Install library to Serverless Framework
cd ~/${SLSDIR}/${ServiceName}
sh sls_install.sh

