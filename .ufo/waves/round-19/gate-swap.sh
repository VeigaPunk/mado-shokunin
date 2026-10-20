#!/usr/bin/env bash
# gate-swap.sh — round 19 / R18-V2: a header-bound red-before receipt for
# QUALITY criterion 26 (a producer's failed read is UNKNOWN, never a value).
#
# The measurement
#   Build the fixture by taking the landed gate and swapping in exactly one
#   block — the d9a5a18 `omarchy.skill.vs_head` arm — then run the landed
#   gate's own `--selftest` against it in a /tmp copy. The landed selftest
#   asserts OM9 (STUB_GIT_SHOW_RC=128 must read UNKNOWN naming the path and
#   rc=128, never "local edit"); the d9a5a18 arm pipes `git show` into
#   sha256sum without the producer's rc, so the empty-input digest
#   e3b0c44298fc1c14… becomes the value and the row claims a local edit. That
#   is the red-before the criterion's byte-pinned receipt must carry.
#
# Output (stdout; the receipt is line 1, then one `# blocks:` record line, the
# selftest's own stdout verbatim, a `stderr:` block only when non-empty, then
# `exit=<N>`):
#
#   RECEIPT tool=.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh \
#           tool_sha256=<sha of the fixture> measured_commit=<REV> utc=<...> \
#           cmd=bash .ufo/waves/round-19/gate-swap.sh <REV>
#
#   The fixture (the measured tool) is written to
#   .ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh.
#
# Pinned inputs (immutable commits; any drift refuses — a block is located by
# content, never by line number, and must appear exactly once in each file):
#
#   base gate  17661e0fa83f978fb659f5bb8fef47f0969f6945:tools/mado-verify.sh
#              sha256 c9fb0cef…  block lines 3467-3489  sha256 c86f51b8…
#   old gate   d9a5a18e17cd3a68b52148fcc01c4a30e340ba98:tools/mado-verify.sh
#              sha256 fba82a66…  block lines 3402-3415  sha256 414bf6ed…
#   fixture    sha256 6e6782c3…  (landed gate with that one block exchanged)
#
# Usage: gate-swap.sh REV
#   REV is the lane commit the receipt binds to (recorded as measured_commit).
#   At the post-commit re-cut it is the commit that carries the fixture, so
#   tool_sha256 equals git show REV:.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh
#   (criterion 24). Before that commit the fixture is absent at REV; the run
#   prints `provisional=1` on the `# blocks:` line and is not credit until L1
#   re-cuts it. If REV does carry the fixture, its committed bytes must hash to
#   the same fixture sha — otherwise the run refuses rather than bind bytes it
#   did not measure.
#
# Discipline
#   * Read-only on the lane: `git rev-parse` / `git cat-file` / `git show`
#     only, no worktree index read (`git show`, index-free). No jj command.
#   * Every `git show | sha256sum` pipeline's producer status is captured into
#     an array immediately after the pipeline (criterion 26 applied to this
#     receipt itself); the empty-input digest is refused as a measurement.
#   * The selftest is the gate's hermetic mode (fixture trees under
#     /tmp/w5-mado-m52-selftest.*, no substrate read, no live gate).
#   * The evidence file is written only when absent; an existing file with
#     different bytes is never overwritten (refuse, exit 2).
#
# Exit: 0 receipt produced (the selftest's rc is recorded as `exit=<N>`, which
#       is expected to be 2 for this red-before); 2 refused / could-not-measure.
set -u -o pipefail
export LC_ALL=C

SELF=$(readlink -f -- "${BASH_SOURCE[0]}")
LANE=$(cd -- "$(dirname -- "$SELF")/../../.." && pwd)
SCRIPT_REL=.ufo/waves/round-19/gate-swap.sh
EV_REL=.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh
EV=$LANE/$EV_REL

BASE_REV=17661e0fa83f978fb659f5bb8fef47f0969f6945
OLD_REV=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98
GATE_REL=tools/mado-verify.sh

BASE_GATE_SHA=c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5
OLD_GATE_SHA=fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207
BASE_BLOCK_SHA=c86f51b85c9b469409dec4896cf7088ff1fe5d3e3f887fac64b4149ebe939c4a
OLD_BLOCK_SHA=414bf6ed658c30c6ad3094127e1a85607af51068815268525e422766cdb4e315
BASE_BLOCK_RANGE=3467-3489
OLD_BLOCK_RANGE=3402-3415
FIXTURE_SHA=6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e
EMPTY_SHA=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

usage() {
    printf 'usage: %s REV\n' "${0##*/}" >&2
}

refuse() {
    printf '%s: REFUSED: %s\n' "${0##*/}" "$*" >&2
    exit 2
}

REV_ARG=""
while [ $# -gt 0 ]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            usage
            refuse "unknown option: $1"
            ;;
        *)
            [ -z "$REV_ARG" ] || { usage; refuse "unexpected extra argument: $1"; }
            REV_ARG=$1
            shift
            ;;
    esac
done
[ -n "$REV_ARG" ] || { usage; refuse "missing REV"; }

command -v git >/dev/null 2>&1 || refuse "git not on PATH"
command -v python3 >/dev/null 2>&1 || refuse "python3 not on PATH"
command -v sha256sum >/dev/null 2>&1 || refuse "sha256sum not on PATH"

full=$(git -C "$LANE" rev-parse --verify --quiet "${REV_ARG}^{commit}") \
    || refuse "cannot resolve '$REV_ARG' to a lane commit"
[ -n "$full" ] || refuse "cannot resolve '$REV_ARG' to a lane commit"

WORK=$(mktemp -d "${TMPDIR:-/tmp}/mado-r19-gate-swap.XXXXXX") || refuse "mktemp failed"
trap 'rm -rf -- "$WORK"' EXIT

# --- 1. pinned source gates (bytes and producer status) ---------------------
git -C "$LANE" show "$BASE_REV:$GATE_REL" > "$WORK/base.sh"
brc=$?
[ "$brc" = 0 ] || refuse "git show $BASE_REV:$GATE_REL failed rc=$brc"
git -C "$LANE" show "$OLD_REV:$GATE_REL" > "$WORK/old.sh"
orc=$?
[ "$orc" = 0 ] || refuse "git show $OLD_REV:$GATE_REL failed rc=$orc"
[ -s "$WORK/base.sh" ] || refuse "base gate bytes are empty at $BASE_REV:$GATE_REL"
[ -s "$WORK/old.sh" ] || refuse "old gate bytes are empty at $OLD_REV:$GATE_REL"

base_gate_sha=$(sha256sum -- "$WORK/base.sh")
base_gate_sha=${base_gate_sha%% *}
old_gate_sha=$(sha256sum -- "$WORK/old.sh")
old_gate_sha=${old_gate_sha%% *}
[ "$base_gate_sha" = "$BASE_GATE_SHA" ] \
    || refuse "base gate sha256 $base_gate_sha != pinned $BASE_GATE_SHA"
[ "$old_gate_sha" = "$OLD_GATE_SHA" ] \
    || refuse "old gate sha256 $old_gate_sha != pinned $OLD_GATE_SHA"
[ "$base_gate_sha" != "$EMPTY_SHA" ] || refuse "base gate is the empty-input digest"

# --- 2. locate each vs_head block by content, exactly once, and swap ---------
python3 -I - "$WORK/base.sh" "$WORK/old.sh" "$WORK/fixture.sh" "$WORK/meta" <<'PY'
import hashlib
import sys

START = b'    if ! have git || [ "$omtree" = 0 ] || ! have sha256sum || [ ! -f "$leaf" ]; then\n'
END = b'    fi\n'


def die(msg):
    print("gate-swap.py: " + msg, file=sys.stderr)
    raise SystemExit(3)


def locate(path):
    with open(path, "rb") as fh:
        data = fh.read()
    lines = data.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line == START]
    if len(starts) != 1:
        die("vs_head block start marker appears %d time(s) in %s (want exactly 1)"
            % (len(starts), path))
    s = starts[0]
    e = None
    for i in range(s + 1, len(lines)):
        if lines[i] == END:
            e = i
            break
    if e is None:
        die("no closing '    fi' after the vs_head block start in %s" % path)
    block = b"".join(lines[s:e + 1])
    if not block:
        die("empty block in %s" % path)
    return data, lines, s, e, block


base_data, base_lines, bs, be, base_block = locate(sys.argv[1])
old_data, old_lines, os_, oe, old_block = locate(sys.argv[2])
if base_block == old_block:
    die("the two blocks are byte-identical; nothing to swap")
fixture = b"".join(base_lines[:bs]) + old_block + b"".join(base_lines[be + 1:])
if fixture.count(old_block) != 1:
    die("the swapped block appears %d times in the fixture (want 1)"
        % fixture.count(old_block))
if fixture.count(base_block) != 0:
    die("the base block survived the swap")
if len(fixture) != len(base_data) - len(base_block) + len(old_block):
    die("fixture length is not base - base_block + old_block")
with open(sys.argv[3], "wb") as fh:
    fh.write(fixture)
rows = {
    "fixture_sha": hashlib.sha256(fixture).hexdigest(),
    "fixture_bytes": str(len(fixture)),
    "base_block_sha": hashlib.sha256(base_block).hexdigest(),
    "base_block_range": "%d-%d" % (bs + 1, be + 1),
    "old_block_sha": hashlib.sha256(old_block).hexdigest(),
    "old_block_range": "%d-%d" % (os_ + 1, oe + 1),
}
with open(sys.argv[4], "w") as fh:
    for k in sorted(rows):
        fh.write("%s=%s\n" % (k, rows[k]))
PY
prc=$?
[ "$prc" = 0 ] || refuse "block extraction/swap failed (python rc=$prc)"

meta() { sed -n "s/^$1=//p" "$WORK/meta"; }
fixture_sha=$(meta fixture_sha)
fixture_bytes=$(meta fixture_bytes)
base_block_sha=$(meta base_block_sha)
base_block_range=$(meta base_block_range)
old_block_sha=$(meta old_block_sha)
old_block_range=$(meta old_block_range)
[ -n "$fixture_sha" ] || refuse "no fixture digest from the swap step"
[ "$base_block_sha" = "$BASE_BLOCK_SHA" ] \
    || refuse "base block sha256 $base_block_sha != pinned $BASE_BLOCK_SHA"
[ "$old_block_sha" = "$OLD_BLOCK_SHA" ] \
    || refuse "old block sha256 $old_block_sha != pinned $OLD_BLOCK_SHA"
[ "$base_block_range" = "$BASE_BLOCK_RANGE" ] \
    || refuse "base block range $base_block_range != pinned $BASE_BLOCK_RANGE"
[ "$old_block_range" = "$OLD_BLOCK_RANGE" ] \
    || refuse "old block range $old_block_range != pinned $OLD_BLOCK_RANGE"
[ "$fixture_sha" = "$FIXTURE_SHA" ] \
    || refuse "fixture sha256 $fixture_sha != pinned $FIXTURE_SHA"
written_sha=$(sha256sum -- "$WORK/fixture.sh")
written_sha=${written_sha%% *}
[ "$written_sha" = "$fixture_sha" ] \
    || refuse "fixture file digest $written_sha != computed $fixture_sha"
[ "$fixture_sha" != "$EMPTY_SHA" ] || refuse "fixture is the empty-input digest"

# --- 3. bind to REV when REV carries the fixture ----------------------------
provisional=0
if git -C "$LANE" cat-file -e "$full:$EV_REL" 2>/dev/null; then
    git -C "$LANE" show "$full:$EV_REL" | sha256sum > "$WORK/rev.sha"
    prc=("${PIPESTATUS[@]}")
    if [ "${prc[0]}" != 0 ]; then
        refuse "git show '$full:$EV_REL' failed rc=${prc[0]} (no digest accepted; the empty-input digest is never evidence)"
    fi
    [ "${prc[1]}" = 0 ] || refuse "sha256sum on the committed fixture failed rc=${prc[1]}"
    rev_sha=$(cut -d' ' -f1 < "$WORK/rev.sha")
    [ -n "$rev_sha" ] || refuse "empty digest for the committed fixture"
    [ "$rev_sha" != "$EMPTY_SHA" ] || refuse "committed fixture hashed as empty input"
    [ "$rev_sha" = "$fixture_sha" ] \
        || refuse "fixture at $full has sha256 $rev_sha, this run builds $fixture_sha — refusing to bind bytes REV does not carry"
else
    provisional=1
fi

# --- 4. the evidence fixture (write only when absent; never overwrite) ------
if [ -e "$EV" ]; then
    [ -f "$EV" ] || refuse "evidence path exists and is not a regular file: $EV_REL"
    cur_sha=$(sha256sum -- "$EV")
    cur_sha=${cur_sha%% *}
    [ "$cur_sha" = "$fixture_sha" ] \
        || refuse "existing $EV_REL has sha256 $cur_sha != this run's $fixture_sha — refusing to overwrite evidence"
else
    install -m 0644 -- "$WORK/fixture.sh" "$EV" || refuse "cannot write $EV_REL"
    cur_sha=$(sha256sum -- "$EV")
    cur_sha=${cur_sha%% *}
    [ "$cur_sha" = "$fixture_sha" ] || refuse "written $EV_REL does not hash to the fixture digest"
fi

# --- 5. run the selftest from a /tmp copy ----------------------------------
cp -- "$WORK/fixture.sh" "$WORK/gate-swap-d9a5a18.sh" || refuse "cannot stage the /tmp copy"
bash "$WORK/gate-swap-d9a5a18.sh" --selftest > "$WORK/out" 2> "$WORK/err"
rc=$?

# --- 6. receipt ------------------------------------------------------------
utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
hdr="RECEIPT tool=$EV_REL tool_sha256=$fixture_sha measured_commit=$full utc=$utc cmd=bash $SCRIPT_REL $REV_ARG"
blocks="# blocks: base=$BASE_REV:$base_block_range sha256=$base_block_sha; old=$OLD_REV:$old_block_range sha256=$old_block_sha; fixture_bytes=$fixture_bytes; provisional=$provisional"
printf '%s\n' "$hdr"
printf '%s\n' "$blocks"
cat "$WORK/out"
if [ -s "$WORK/err" ]; then
    printf 'stderr:\n'
    cat "$WORK/err"
fi
printf 'exit=%s\n' "$rc"
exit 0
