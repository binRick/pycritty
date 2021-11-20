#!/usr/bin/env bash
set -e
cd $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

APP_ICON=~/Downloads/terminal_icons/red-terminal.png
APP_NAME="MY_APP1"
APP_EXEC_ARGS=$@
APP_EXEC=$(mktemp)
rsync $(command -v alacritty) $APP_EXEC
chmod +x $APP_EXEC

APP_ICON=${APP_ICON:-~/Downloads/terminal_icons/red-terminal.png}

gen_wrapper() {
	local _cmd="$(
		cat <<EOF
cmd="appify -name \"$APP_NAME\" -icon \"$APP_ICON\" $APP_EXEC"
2>&1 echo -e "\$cmd"
eval "\$cmd"
EOF
	)"
	ansi --yellow --bg-black --italic "$_cmd"
	echo -e "\n$_cmd\n"
	eval "$_cmd"
}

xxx_cmd="$(
	cat <<EOF
cmd="appify -name $APP_NAME -icon \"$APP_ICON\" $APP_EXEC"
2>&1 echo -e "$cmd"
eval $cmd"
EOF
)"

if [[ "$DM" == 1 ]]; then
	gen_wrapper
	exit
fi

if [[ "$SKIP_BUILD" != 1 ]]; then
	./build.sh &
fi

if [[ ! -f ./.v/bin/activate ]]; then
	python3 -m venv ./.v
fi

wait
source ./.v/bin/activate
unlink $APP_EXEC
exec ./.v/bin/pycritty $@
