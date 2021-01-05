#!/bin/sh
DIR=wordcloud

pip3 install -t python wordcloud

zip -r ${DIR}.zip python

aws lambda publish-layer-version \
	--layer-name ${DIR} \
	--description 'packages: six, cycler, python-dateutil, pyparsing, kiwisolver, numpy, matplotlib, pillow, wordcloud' \
	--zip-file fileb://${DIR}.zip \
	--compatible-runtimes python3.6 python3.7

rm -rf python ${DIR}.zip

