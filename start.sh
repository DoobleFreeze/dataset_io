#!/bin/bash
app="datasetio"
docker build -t ${app} .
docker run -d -p 9889:9889 \
  --name=${app} \
  -v $PWD:/app ${app}