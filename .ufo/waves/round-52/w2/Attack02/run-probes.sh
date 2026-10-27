#!/usr/bin/env bash
# Attack02 fixture driver — builds a scratch fixture repo, commits one probe per
# revision, runs the W1 C1 draft counter against each, and transcripts everything.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
COUNTER=$LANE/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py
CONTROL=$LANE/.ufo/waves/round-52/controls/c1-do-nothing.md
SCRATCH=/fast/scratch/hyaku/mado-r52/Attack02
FIX=$SCRATCH/fix
OUT=$SCRATCH/transcript.txt

say() { printf '\n===== %s =====\n' "$*" | tee -a "$OUT"; }
run_counter() { # rev workdir [extra args...]
    local rev=$1; local work=$2; shift 2
    mkdir -p "$work"
    python3 -I "$COUNTER" --repo "$FIX" --rev "$rev" --work "$work" "$@" 2>&1
    echo "exit=$?"
}

: > "$OUT"

say "0. hygiene"
sha256sum "$COUNTER" | tee -a "$OUT"
git -C "$LANE" rev-parse HEAD | tee -a "$OUT"
df -h /fast | tail -1 | tee -a "$OUT"

rm -rf "$FIX"
mkdir -p "$FIX/tools" "$FIX/docs" "$FIX/quality"
cd "$FIX" || exit 1
git init -q
git config user.email attack02@fixture
git config user.name Attack02Fixture
git config commit.gpgsign false
# host guard: assert toplevel before any mutation
TOP=$(git rev-parse --show-toplevel)
[ "$TOP" = "$FIX" ] || { echo "TOPLEVEL MISMATCH: $TOP" | tee -a "$OUT"; exit 1; }
echo "fixture toplevel ok: $TOP" | tee -a "$OUT"

# --- population instruments (2 tools + 1 quality/*.py) ---
printf '#!/usr/bin/env python3\n# alpha resolves widget inventory during each ledger round.\nprint("alpha")\n' > tools/alpha.py
printf '#!/bin/sh\n# beta resolves widget inventory during each ledger round.\necho beta\n' > tools/beta.sh
printf '#!/usr/bin/env python3\n# gamma tallies evidence rows during each ledger round.\nprint("gamma")\n' > quality/gamma.py
chmod +x tools/alpha.py tools/beta.sh quality/gamma.py

# --- evidence documents ---
printf '# Evidence\nalpha.py is exercised by the fixture harness and pins its inputs.\n' > docs/alpha.md
printf '# Evidence\nbeta.sh is exercised by the fixture harness and pins its inputs.\n' > docs/beta.md
printf '# Evidence\ngamma.py is exercised by the fixture harness and pins its inputs.\n' > docs/gamma.md

write_ledger() { # writes quality/tool-ledger.md from stdin
    cat > quality/tool-ledger.md
}

commit_all() { # message
    git add -A
    git commit -q -m "$1"
    git rev-parse HEAD
}

GREEN_LEDGER='| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/alpha.md:1` |
| `tools/beta.sh` | beta resolves widget inventory during each ledger round. | `docs/beta.md:1` |
| `quality/gamma.py` | gamma tallies evidence rows during each ledger round. | `docs/gamma.md:1` |'

write_base_ledger() {
    {
        echo "# fixture tool ledger"
        echo
        echo '| instrument | description | accountability pointer |'
        echo '|---|---|---|'
        printf '%s\n' "$GREEN_LEDGER"
        echo
        echo 'Row grammar (fenced documentation, must be skipped):'
        echo
        echo '```'
        echo '| `tools/alpha.py` | documentation example row | `docs/alpha.md` |'
        echo '```'
    } | write_ledger
}

# ---------- P00 green baseline ----------
say "P00 fixture green baseline"
write_base_ledger
R=$(commit_all "P00 green baseline")
run_counter "$R" "$SCRATCH/work-P00" | tee -a "$OUT"
echo "P00_REV=$R" | tee -a "$OUT"

# ---------- P03 basename reference to the ledger + accountable doc ----------
say 'P03 pointer = `tool-ledger.md` and `docs/alpha.md:1` (bare ledger basename + doc)'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `tool-ledger.md` and `docs/alpha.md:1` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P03 basename ledger ref plus doc")
run_counter "$R" "$SCRATCH/work-P03" | tee -a "$OUT"
echo "P03_REV=$R" | tee -a "$OUT"

# ---------- P04 own-basename reference + doc ----------
say 'P04 pointer = `alpha.py` and `docs/alpha.md:1` (row own basename + doc)'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `alpha.py` and `docs/alpha.md:1` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P04 own basename plus doc")
run_counter "$R" "$SCRATCH/work-P04" | tee -a "$OUT"
echo "P04_REV=$R" | tee -a "$OUT"

# ---------- P05 ./basename + doc ----------
say 'P05 pointer = `./tool-ledger.md` and `docs/alpha.md:1`'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `./tool-ledger.md` and `docs/alpha.md:1` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P05 dot-slash basename plus doc")
run_counter "$R" "$SCRATCH/work-P05" | tee -a "$OUT"
echo "P05_REV=$R" | tee -a "$OUT"

# ---------- P06 trailing punctuation inside backticks + doc ----------
say 'P06 pointer = `quality/tool-ledger.md)` and `docs/alpha.md:1`'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `quality/tool-ledger.md)` and `docs/alpha.md:1` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P06 trailing paren inside backticks plus doc")
run_counter "$R" "$SCRATCH/work-P06" | tee -a "$OUT"
echo "P06_REV=$R" | tee -a "$OUT"

# ---------- P07 non-numeric line suffix + doc ----------
say 'P07 pointer = `quality/tool-ledger.md:x` and `docs/alpha.md:1`'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `quality/tool-ledger.md:x` and `docs/alpha.md:1` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P07 nonnumeric line suffix plus doc")
run_counter "$R" "$SCRATCH/work-P07" | tee -a "$OUT"
echo "P07_REV=$R" | tee -a "$OUT"

# ---------- P08 bare basename alone ----------
say 'P08 pointer = `tool-ledger.md` alone'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `tool-ledger.md` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P08 bare basename alone")
run_counter "$R" "$SCRATCH/work-P08" | tee -a "$OUT"
echo "P08_REV=$R" | tee -a "$OUT"

# ---------- P09 symlink alias to the row's own file ----------
say 'P09 pointer = `docs/alpha-evidence.md` (symlink -> ../tools/alpha.py)'
ln -s ../tools/alpha.py docs/alpha-evidence.md
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/alpha-evidence.md` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P09 symlink alias to own file")
git ls-tree "$R" -- docs/alpha-evidence.md | tee -a "$OUT"
git show "$R:docs/alpha-evidence.md" | tee -a "$OUT"
run_counter "$R" "$SCRATCH/work-P09" | tee -a "$OUT"
echo "P09_REV=$R" | tee -a "$OUT"
git rm -q docs/alpha-evidence.md

# ---------- P10 symlink to the ledger ----------
say 'P10 pointer = `docs/ledger-copy.md` (symlink -> ../quality/tool-ledger.md)'
ln -s ../quality/tool-ledger.md docs/ledger-copy.md
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/ledger-copy.md` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P10 symlink to ledger")
git show "$R:docs/ledger-copy.md" | tee -a "$OUT"
run_counter "$R" "$SCRATCH/work-P10" | tee -a "$OUT"
echo "P10_REV=$R" | tee -a "$OUT"
git rm -q docs/ledger-copy.md

# ---------- P11/P12 control-shape 4-cell row, basename vs full path ----------
say 'P11 4-cell control shape, bare basename `tool-ledger.md` in Reads cell'
{
    echo '# fixture tool ledger'; echo
    echo '| Tool | Reads | Writes | Owner and adjacent lanes |'
    echo '|---|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/alpha.md:1` |'
    echo '| tools/beta.sh | reads tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |'
    echo '| `quality/gamma.py` | gamma tallies evidence rows during each ledger round. | `docs/gamma.md:1` |'
} | write_ledger
R=$(commit_all "P11 control shape bare basename")
run_counter "$R" "$SCRATCH/work-P11" | tee -a "$OUT"
echo "P11_REV=$R" | tee -a "$OUT"

say 'P12 4-cell control shape, full path `quality/tool-ledger.md` in Reads cell'
{
    echo '# fixture tool ledger'; echo
    echo '| Tool | Reads | Writes | Owner and adjacent lanes |'
    echo '|---|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/alpha.md:1` |'
    echo '| tools/beta.sh | reads quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |'
    echo '| `quality/gamma.py` | gamma tallies evidence rows during each ledger round. | `docs/gamma.md:1` |'
} | write_ledger
R=$(commit_all "P12 control shape full path")
run_counter "$R" "$SCRATCH/work-P12" | tee -a "$OUT"
echo "P12_REV=$R" | tee -a "$OUT"

# ---------- P13 evidence cycle ----------
say 'P13 evidence cycle: alpha -> doc naming alpha (about beta), beta -> doc naming beta (about alpha)'
printf '# Cycle evidence\nalpha.py checks beta.sh outputs during the round.\n' > docs/beta-cycle.md
printf '# Cycle evidence\nbeta.sh checks alpha.py outputs during the round.\n' > docs/alpha-cycle.md
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/beta-cycle.md` |'
    echo '| `tools/beta.sh` | beta resolves widget inventory during each ledger round. | `docs/alpha-cycle.md` |'
    echo '| `quality/gamma.py` | gamma tallies evidence rows during each ledger round. | `docs/gamma.md:1` |'
} | write_ledger
R=$(commit_all "P13 evidence cycle")
run_counter "$R" "$SCRATCH/work-P13" | tee -a "$OUT"
echo "P13_REV=$R" | tee -a "$OUT"

# ---------- P14 shared registry document ----------
say 'P14 all rows point at one shared registry doc naming all basenames'
printf '# Registry\nInstruments: alpha.py, beta.sh, gamma.py.\n' > docs/registry.md
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `docs/registry.md` |'
    echo '| `tools/beta.sh` | beta resolves widget inventory during each ledger round. | `docs/registry.md` |'
    echo '| `quality/gamma.py` | gamma tallies evidence rows during each ledger round. | `docs/registry.md` |'
} | write_ledger
R=$(commit_all "P14 shared registry")
run_counter "$R" "$SCRATCH/work-P14" | tee -a "$OUT"
echo "P14_REV=$R" | tee -a "$OUT"

# ---------- P15 closed-hole regression: full-path ledger + doc ----------
say 'P15 pointer = `quality/tool-ledger.md` and `docs/alpha.md:1` (closed-hole regression)'
{
    echo '# fixture tool ledger'; echo
    echo '| instrument | description | accountability pointer |'
    echo '|---|---|---|'
    echo '| `tools/alpha.py` | alpha resolves widget inventory during each ledger round. | `quality/tool-ledger.md` and `docs/alpha.md:1` |'
    printf '%s\n' "$GREEN_LEDGER" | tail -2
} | write_ledger
R=$(commit_all "P15 full path ledger plus doc")
run_counter "$R" "$SCRATCH/work-P15" | tee -a "$OUT"
echo "P15_REV=$R" | tee -a "$OUT"

# ---------- P16 selftest ----------
say "P16 counter --selftest"
mkdir -p "$SCRATCH/work-P16"
python3 -I "$COUNTER" --selftest --work "$SCRATCH/work-P16" 2>&1 | tee -a "$OUT"
echo "exit=$?" | tee -a "$OUT"

say "DONE fixture probes"
