#!/usr/bin/env bash
set -e
[[ -f .v/bin/pycritty ]] && unlink .v/bin/pycritty
source ./.v/bin/activate

of=$(mktemp)
ef=$(mktemp)
if ! python setup.py install >$of 2>$ef; then
	cat $of
	cat $ef
	exit 2
fi
