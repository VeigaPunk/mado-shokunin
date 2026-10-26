#!/bin/bash
# One pass of every instrument check of c1-r47-terminal.py, receipts into the seat's receipts/ directory.
# Usage: run-final-battery.sh <scratch-dir>
set -u
D=$(cd "$(dirname "$0")" && pwd)
S=${1:?usage: run-final-battery.sh SCRATCH}
L=$(cd "$D/../../../../.." && pwd)
FIX="$D/fixtures-placeholder.json"
mkdir -p "$S/repos"

mk() { # mk <name> <source tool> -> prints the fixture repo path
	local name=$1 src=$2 R
	R=$(mktemp -d -p "$S/repos" "repo-$name-XXXX") || return 1
	git -C "$R" init -q || return 1
	if [ "$(git -C "$R" rev-parse --show-toplevel)" != "$R" ]; then echo "TOPLEVEL-MISMATCH $R" >&2; return 1; fi
	mkdir -p "$R/tools"
	cp "$src" "$R/tools/mado-terminal.py" || return 1
	git -C "$R" -c user.name=ctl -c user.email=ctl@example.invalid add -A || return 1
	git -C "$R" -c user.name=ctl -c user.email=ctl@example.invalid commit -q -m "$name" || return 1
	echo "$R"
}

{
	echo "# counter sha256 $(sha256sum "$D/c1-r47-terminal.py" | cut -d' ' -f1)"
	echo "# fixtures sha256 $(sha256sum "$FIX" | cut -d' ' -f1)"
	echo "== controls (stub, lietest, delegator, subproc, embed): every one must MISS"
	python3 "$D/run-controls.py" --counter "$D/c1-r47-terminal.py" --work "$S/ctl" --fixtures "$FIX" \
		--nonce 47 --receipts "$D/receipts" 2>&1 | grep -E "^CTL_C1"
} > "$D/receipts/controls-run.txt" 2>&1

{
	echo "# counter sha256 $(sha256sum "$D/c1-r47-terminal.py" | cut -d' ' -f1)"
	echo "== guards: every guard and every comparison must be able to fail"
	python3 "$D/check-counter-guards.py" --counter "$D/c1-r47-terminal.py" --fixtures "$FIX" \
		--work "$S/guards" 2>&1 | grep -E "^GUARD"
} > "$D/receipts/counter-guards.txt" 2>&1

{
	echo "# counter sha256 $(sha256sum "$D/c1-r47-terminal.py" | cut -d' ' -f1)"
	echo "== the real script must answer the same generated case identically in two case roots"
	python3 "$D/check-oracle-determinism.py" --counter "$D/c1-r47-terminal.py" --work "$S/det" --nonce 47
} > "$D/receipts/oracle-determinism.txt" 2>&1

{
	REF="$L/ExecRefB/mado-terminal.py"
	echo "# reference $(sha256sum "$REF")"
	R=$(mk refb "$REF") || exit 1
	python3 "$D/c1-r47-terminal.py" --repo "$R" --rev HEAD --work "$S/refb" --fixtures "$FIX" --nonce 47
} > "$D/receipts/refb-met.txt" 2>&1

{
	REF="$L/ExecRefB/mado-terminal.py"
	MUT="$S/cacheread.py"
	python3 "$D/make-cacheread-mutant.py" --ref "$REF" --out "$MUT"
	echo "# mutant sha256 $(sha256sum "$MUT" | cut -d' ' -f1)"
	R=$(mk cacheread "$MUT") || exit 1
	python3 "$D/c1-r47-terminal.py" --repo "$R" --rev HEAD --work "$S/mut" --fixtures "$FIX" --nonce 47 2>&1 |
		grep -E "forged_cache_runs|clause=(s|g |r exec)|PRED-C1-r47:"
	echo "cacheD_failures=$(python3 "$D/c1-r47-terminal.py" --repo "$R" --rev HEAD --work "$S/mut" --fixtures "$FIX" \
		--nonce 47 2>&1 | grep -c 'cacheD:')"
} > "$D/receipts/cacheread-mutant.txt" 2>&1

grep -hE "^CTL_C1 VERDICT|^GUARD VERDICT|^DET [0-9]+/|verdict=" "$D/receipts/"*.txt
