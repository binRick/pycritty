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

ansi --green "Build OK" >&2

#./.v/bin/pycritty ls -c

ansi --green "List Help" >&2
./.v/bin/pycritty ls -h

ansi --green "Listing PIDs" >&2
./.v/bin/pycritty ls -p

ansi --green "Listing Hosts" >&2
./.v/bin/pycritty ls -H

ansi --green "Listing Shells" >&2
./.v/bin/pycritty ls -S

ansi --green "Listing Commands" >&2
./.v/bin/pycritty ls -C
