#!/bin/sh
# ExecFixtureMap: deterministic probe of the LINENO shift inside a heredoc $( ) body.
# Writes nothing (the probe is fed to bash on stdin); exit 0 only if the shift is -1.
# Run from anywhere: sh heredoc-lineno-probe.sh
out=$(PS4='+${LINENO} ' bash -x -s 2>&1 <<'PROBE'
f() {
	read -r h _d <<- EOH
		$(
			echo AAA
			echo BBB
		)
	EOH
	printf '[%s]\n' "$h"
}
f
PROBE
)
printf '%s\n' "$out"
printf '\n-- expected: the two echo commands sit on lines 4 and 5 of the probe, and their trace\n'
printf -- '-- lines above are the ones bash reports for them.\n'
printf '%s\n' "$out" | grep -q '^++3 echo AAA$' && printf 'echo AAA (line 4) reported as 3: OK\n' || printf 'echo AAA: SHIFT NOT -1\n'
printf '%s\n' "$out" | grep -q '^++4 echo BBB$' && printf 'echo BBB (line 5) reported as 4: OK\n' || printf 'echo BBB: SHIFT NOT -1\n'
printf '%s\n' "$out" | grep -q '^\[AAA\]$' && printf 'body value correct (AAA): OK\n' || printf 'body value: FAIL\n'
