#!/usr/bin/env bash
set -e
[[ -f .v/bin/pycritty ]] && unlink .v/bin/pycritty
e=./exec.sh
source ./.v/bin/activate

BASIC_TESTS_ENABLED=${BASIC_TESTS_ENABLED:-0}
PROFILE_TESTS_ENABLED=${PROFILE_TESTS_ENABLED:-1}
SHELL_TESTS_ENABLED=${PROFILE_TESTS_ENABLED:-1}

NEW_PROFILE1=dev-profile1-$(date +%s)
NEW_PROFILE2=dev-profile2-$(date +%s)
NEW_SHELL1=/bin/bash
NEW_SHELL2=/usr/local/bin/bash
NEW_SHELL3=/usr/local/bin/zsh

of=$(mktemp)
ef=$(mktemp)
if ! python setup.py install >$of 2>$ef; then
	cat $of
	cat $ef
	exit 2
fi

export SKIP_BUILD=1

ansi --green "Build OK" >&2
echo

validate_config_shell_args() {
	program="$(command cat ~/.config/alacritty/alacritty.yml | yaml2json | jq '.shell.program' -Mrc)"
	args="$(command cat ~/.config/alacritty/alacritty.yml | yaml2json | jq '.shell.args' -Mr | tail -n2 | head -n1)"
	args="$(echo -e "$args" | tr -s ' ' | sed 's/^[[:space:]]//g')"
	(
		echo -e "$(ansi --cyan PROGRAM:)                 $program"
		echo -e "$(ansi --cyan ARGS:)                    $args"
		ef=$(mktemp)
		if ! bash -n <(echo -e "$args") 2>$ef; then
			ansi --green "args bash syntax failed"
			cat $ef
		else
			ansi --green "syntax ok"
		fi
	) >&2
}

validate_config_shell_args
exit

basic_tests() {
	ansi --green "List Help" >&2
	$e ls -h
	echo

	ansi --green "Listing PIDs" >&2
	$e ls -p
	echo

	ansi --green "Listing Hosts" >&2
	$e ls -H
	echo

	ansi --green "Listing Shells" >&2
	$e ls -S
	echo

	ansi --green "Listing Commands" >&2
	$e ls -C
	echo

}

profile_tests() {
	ansi --green "Loading Dark Profile" >&2
	$e load Dark
	echo

	cmd="$e save $NEW_PROFILE1"
	ansi --green "Saving profile $NEW_PROFILE1 :: $(ansi --cyan "$cmd")" >&2
	eval "$cmd"
	echo
}

shell_tests() {
	cmd="$e -S $NEW_SHELL1"
	ansi --green "Configuring shell $NEW_SHELL1 :: $(ansi --cyan "$cmd")" >&2
	eval "$cmd"
	echo

	cmd="$e -S $NEW_SHELL2"
	ansi --green "Configuring shell $NEW_SHELL2 :: $(ansi --cyan "$cmd")" >&2
	eval "$cmd"
	echo

	cmd="$e -S $NEW_SHELL3"
	ansi --green "Configuring shell $NEW_SHELL3 :: $(ansi --cyan "$cmd")" >&2
	eval "$cmd"
	echo

	ARGS="date && find / 2>/dev/null | pv >/dev/null"
	cmd="EXEC_CMD='$ARGS' ./exec.sh -S $NEW_SHELL3 -A EXEC_CMD"
	ansi --green "Configuring shell $NEW_SHELL3 and args $ARGS :: $(ansi --cyan "$cmd")" >&2
	eval "$cmd"
	echo

	$e save $NEW_PROFILE1 -o

}

main() {
	[[ "$BASIC_TESTS_ENABLED" == 1 ]] && basic_tests
	[[ "$PROFILE_TESTS_ENABLED" == 1 ]] && profile_tests
	[[ "$SHELL_TESTS_ENABLED" == 1 ]] && shell_tests
	true
}

main
