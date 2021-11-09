#!/usr/bin/env bash
set -e
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [[ "$SKIP_BUILD" != 1 ]]; then
	./build.sh &
fi


if [[ ! -f ./.v/bin/activate ]]; then
  python3 -m venv ./.v
fi
wait
source ./.v/bin/activate

exec ./.v/bin/pycritty $@
