#!/bin/sh

# jane
url="http://127.0.0.1:8865/rev?format=json&lat=48.85833&lon=3.29513&zoom=18&addressdetails=1"

curl -sS $url 
echo
