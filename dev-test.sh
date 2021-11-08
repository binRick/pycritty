#!/usr/bin/env bash
set -e

cmd="nodemon --delay .2 -w . -e sh,yaml,py -V -x sh -- -c './test.sh $@||true'"
exec $cmd
