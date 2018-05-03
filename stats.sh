#!/bin/sh

curl -sS http://127.0.0.1:8865/stats | jq .
