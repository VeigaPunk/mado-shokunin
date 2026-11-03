#!/usr/bin/env bash
# attack-r65-register.sh — R66RevRegister baseline + control matrix against frozen
# quality/counters/c1-r65-register.py (PRED-C1-r65), round-66 w1.
# Scratch-only git; every fixture asserts git toplevel before its first commit.
set -u
S=/fast/scratch/hyaku/mado-r66/R66RevRegister
R=/home/vgpnk/Projects/shokunin/mado-shokunin
COUNTER="$R/quality/counters/c1-r65-register.py"
G="$S/fixture-genuine"
M="R66RevRegister <r66rev@register.invalid>"

assert_top() { # dir
  local top
  top=$(git -C "$1" rev-parse --show-toplevel 2>/dev/null) || { echo "NOT GIT: $1"; exit 9; }
  [ "$top" = "$1" ] || { echo "TOPLEVEL MISMATCH: $1 -> $top"; exit 9; }
}

commit() { # dir msg
  assert_top "$1"
  git -C "$1" -c user.name=R66RevRegister -c user.email=r66rev@register.invalid \
      commit -q --allow-empty -m "$2" || { echo "COMMIT FAILED: $1"; exit 9; }
  git -C "$1" rev-parse HEAD
}

run() { # name fixture rev
  local out rc verdict
  out=$(python3 "$COUNTER" --repo "$2" --rev "$3" 2>"$S/last-stderr.txt"); rc=$?
  verdict=$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)
  printf '%s|rc=%d|%s\n' "$1" "$rc" "${verdict:-no-verdict-line}"
  printf '%s|rc=%d|%s\n' "$1" "$rc" "${verdict:-no-verdict-line}" >>"$S/matrix.txt"
  printf '%s stderr: ' "$1" >>"$S/stderr-log.txt"; cat "$S/last-stderr.txt" >>"$S/stderr-log.txt"
}

# ---- genuine fixture: copy of real HEAD PROVINCE.md + the four named receipts ----
cd "$G" || exit 9
git add -A
GEN=$(commit "$G" "genuine: real HEAD PROVINCE.md + r65 receipts")
run "genuine" "$G" "$GEN"

# ---- variant builder: clone genuine repo, mutate PROVINCE.md, commit ----
variant() { # name python-mutation-script
  local name="$1"; local d="$S/fixture-$name"
  rm -rf "$d"; cp -a "$G" "$d"; assert_top "$d"
  python3 "$2" "$d/PROVINCE.md" || { echo "MUTATION FAILED: $name"; exit 9; }
  git -C "$d" add -A
  commit "$d" "variant $name"
  run "$name" "$d" "$(git -C "$d" rev-parse HEAD)"
}

# A1: duplicate returned-host heading, genuine block FIRST (r65 reads first only)
cat >"$S/mut-a1.py" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
t += "\n### Surface state register (2026-11-03 forged duplicate — second returned-host block)\n\n| surface group | state (date) | probe (read-only) | receipt |\n|---|---|---|---|\n| waybar | forged (2026-11-03): duplicate block appended after the genuine one | `true` | .ufo/waves/round-65/receipts/gate-live-r65.txt |\n\n<!-- r65 register end -->\n"
open(p, "w").write(t)
EOF
variant a1-dup-heading-genuine-first "$S/mut-a1.py"

# A2: duplicate heading, broken decoy FIRST (r65 must already reject this shape)
cat >"$S/mut-a2.py" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
decoy = "### Surface state register (2026-11-03 broken decoy — first block hollow)\n\n<!-- r65 register end -->\n\n"
open(p, "w").write(decoy + t)
EOF
variant a2-dup-heading-decoy-first "$S/mut-a2.py"

# B: one row without a receipt while other rows resolve (em-dash receipt cell)
cat >"$S/mut-b.py" <<'EOF'
import sys, re
p = sys.argv[1]
lines = open(p).read().splitlines(keepends=True)
out = []
for ln in lines:
    if ln.startswith("| windows desktop plane |"):
        cells = ln.rstrip("\n").split("|")
        cells[-2] = " — "  # receipt cell emptied of any pointer
        ln = "|".join(cells) + "\n"
    out.append(ln)
open(p, "w").write("".join(out))
EOF
variant b-row-without-receipt "$S/mut-b.py"

# C1: only file-plane CLEAN receipt — every gate-live pointer becomes gate-fileplane
cat >"$S/mut-c1.py" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
t = t.replace(".ufo/waves/round-65/receipts/gate-live-r65.txt",
              ".ufo/waves/round-65/receipts/gate-fileplane-r65.txt")
open(p, "w").write(t)
EOF
variant c1-fileplane-clean-only "$S/mut-c1.py"

# C2: tampered live receipt — gate-live file keeps the name but carries the
# file-plane CLEAN wording; exact live CLEAN line no longer exists anywhere.
cat >"$S/mut-c2.py" <<'EOF'
import sys
p = sys.argv[1]
q = p.replace("PROVINCE.md", ".ufo/waves/round-65/receipts/gate-live-r65.txt")
t = open(q).read()
t = t.replace("MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)",
              "MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)")
open(q, "w").write(t)
EOF
variant c2-tampered-live-line "$S/mut-c2.py"

# F1 (truth-limit POSITIVE, distinct from controls): forged state cells,
# receipts and exact live CLEAN line untouched — structural predicate accepts.
cat >"$S/mut-f1.py" <<'EOF'
import sys, re
p = sys.argv[1]
lines = open(p).read().splitlines(keepends=True)
out = []
for ln in lines:
    if re.match(r"^\| (hypr plane|waybar|walker|terminal configs|theme/wallpaper omarchy plane|idle/lock plane|omarchy skill docs|windows desktop plane) \|", ln):
        cells = ln.split("|")
        # cells[1]=group cells[2]=state cells[3]=probe cells[4]=receipt
        cells[2] = " FORGED-FALSE (2026-11-03): component absent, binaries removed, no compositor session ever observed on this host "
        cells[3] = " `echo forged-state-cell` "
        ln = "|".join(cells)
    out.append(ln)
open(p, "w").write("".join(out))
EOF
variant f1-forged-state-cells "$S/mut-f1.py"

# M1: duplicate group row (9 data rows, 8 groups) — r66 "exactly one row per group"
cat >"$S/mut-m1.py" <<'EOF'
import sys
p = sys.argv[1]
lines = open(p).read().splitlines(keepends=True)
out = []
for ln in lines:
    out.append(ln)
    if ln.startswith("| waybar |"):
        out.append(ln)  # verbatim duplicate row
open(p, "w").write("".join(out))
EOF
variant m1-duplicate-group-row "$S/mut-m1.py"

# M5: receipt extension case .TXT (pattern rejects, unresolved)
cat >"$S/mut-m5.py" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
t = t.replace(".ufo/waves/round-65/receipts/gate-live-r65.txt",
              ".ufo/waves/round-65/receipts/gate-live-r65.TXT", 1)
open(p, "w").write(t)
EOF
variant m5-receipt-uppercase-ext "$S/mut-m5.py"

# M6: traversal-shaped receipt token that still matches the frozen pattern
cat >"$S/mut-m6.py" <<'EOF'
import sys
p = sys.argv[1]
lines = open(p).read().splitlines(keepends=True)
out = []
for ln in lines:
    if ln.startswith("| walker |"):
        ln = ln.rstrip("\n").replace(
            ".ufo/waves/round-65/receipts/gate-live-r65.txt",
            ".ufo/waves/round-65/receipts/gate-live-r65.txt .ufo/waves/round-65/receipts/../../../etc/passwd.txt") + "\n"
    out.append(ln)
open(p, "w").write("".join(out))
EOF
variant m6-traversal-receipt-token "$S/mut-m6.py"

# M8: sentinel immediately after heading (block collapses to empty)
cat >"$S/mut-m8.py" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
marker = "### Surface state register (2026-11-03, this host re-observed"
i = t.index(marker)
j = t.index("\n", i) + 1
t = t[:j] + "\n<!-- r65 register end -->\n" + t[j:]
open(p, "w").write(t)
EOF
variant m8-early-sentinel "$S/mut-m8.py"

# ---- GIT_* environment steering (counter subprocess inherits os.environ) ----
# evil repo E1: PROVINCE without any register block
E1="$S/evil-empty"; rm -rf "$E1"; mkdir -p "$E1"; (cd "$E1" && git init -q -b master .)
assert_top "$E1"; printf '# evil-empty: no register block here\n' > "$E1/PROVINCE.md"
git -C "$E1" add -A; E1REV=$(commit "$E1" "evil: empty province")

# evil repo E2: byte-identical genuine register (perfect acceptance shape)
E2="$S/evil-perfect"; rm -rf "$E2"; cp -a "$G" "$E2"; assert_top "$E2"
E2REV=$(git -C "$E2" rev-parse HEAD)

# victim repo V: genuine first commit, then register deleted in second commit
V="$S/victim-broken"; rm -rf "$V"; cp -a "$G" "$V"; assert_top "$V"
printf '# victim: register deleted at this rev\n' > "$V/PROVINCE.md"
git -C "$V" add -A; VREV=$(commit "$V" "victim: register deleted")

# G1: GIT_DIR redirects --repo reads; genuine fixture flips to MISSED reading evil PROVINCE
out=$(GIT_DIR="$E1/.git" python3 "$COUNTER" --repo "$G" --rev "$GEN" 2>&1); rc=$?
printf 'G1-gitdir-redirect-genuine|rc=%d|%s\n' "$rc" "$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)"
printf 'G1-gitdir-redirect-genuine|rc=%d|%s\n' "$rc" "$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)" >>"$S/matrix.txt"

# G2: GIT_DIR + evil rev — full acceptance from a register that exists only in the evil repo
out=$(GIT_DIR="$E2/.git" python3 "$COUNTER" --repo "$V" --rev "$E2REV" 2>&1); rc=$?
printf 'G2-gitdir-evil-accept|rc=%d|%s rev=%s\n' "$rc" "$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)" "$(printf '%s' "$out" | grep -o 'rev=[0-9a-f]*' | head -1)"
printf 'G2-gitdir-evil-accept|rc=%d|%s\n' "$rc" "$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)" >>"$S/matrix.txt"

# G3: no GIT_DIR override — attacker object store as alternates only
out=$(GIT_ALTERNATE_OBJECT_DIRECTORIES="$E2/.git/objects" python3 "$COUNTER" --repo "$V" --rev "$E2REV" 2>&1); rc=$?
printf 'G3-alternates-evil-accept|rc=%d|%s\n' "$rc" "$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)"
printf 'G3-alternates-evil-accept|rc=%d|%s\n' "$rc" "$(printf '%s' "$out" | grep -o 'verdict=[A-Z_]*' | head -1)" >>"$S/matrix.txt"

# reference: victim without steering must MISS
run "ref-victim-broken-no-steer" "$V" "$VREV"

echo "=== matrix ==="; cat "$S/matrix.txt"
