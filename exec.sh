#!/usr/bin/env bash
set -e
source ./.v/bin/activate

if [[ "$SKIP_BUILD" != 1 ]]; then
	./build.sh
fi

exec ./.v/bin/pycritty $@
