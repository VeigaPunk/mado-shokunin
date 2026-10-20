# QualityDraft — round 18 (mado), scoped report

Seat: `MadoR18.QualityDraft` (leaf, no dispatch). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Tool installs or updates this seat: none. Host surface touched: none (file reads, `sha256sum`, one bash fixture with a stub `git` inside `mktemp`). No `git` or `jj` command run. No pacman/sudo/systemctl or omarchy command.

## Axes

- **calibration** (C1): literal QUALITY lesson-citation fraction, `measure.py` counter `^[0-9]+\. ` / `^[0-9]+\. .*lessons/`.
  Baseline on the working tree: 15/23. With the three drafted criteria appended (simulated in `/tmp/qr18/q.md`): **18/26**, meeting the C1 target.

## Output

- Draft: `.ufo/waves/round-18/drafts/QualityDraft.md` — append-only criteria 24, 25, 26 under one heading. Each first line carries `(lesson: lessons/round-18.md#mistakes M<n>; outside … R17-V<k> / jj audit F10)`:
  - 24 → `lessons/round-18.md#mistakes M1`; outside `lessons/round-17-verifier-spotcheck.md` R17-V1/V2.
  - 25 → `lessons/round-18.md#mistakes M2`; outside `lessons/round-17-verifier-spotcheck.md` R17-V5.
  - 26 → `lessons/round-18.md#mistakes M3`; outside `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md` F10 (jj audit, not the spot-check).
- The `M1..M3` ids are my proposal. `lessons/round-18.md` does not exist yet; L1 must write Mistakes rows with these ids (or renumber the three citations to match). Until then the citations are dangling.
- Each criterion's first line contains `lessons/`, so the literal counter credits all three (verified: `grep -cE '^(24|25|26)\. .*lessons/'` → 3).

## Runnable checks (planned paths; L1 commits them)

The criteria cite `.ufo/waves/round-18/checks/…`. I did not write into the lane beyond the draft and this report, so the sources are below. L1 commits them verbatim, then runs them once after integration. All were executed from `/tmp/qr18/` and their outputs are recorded here.

| criterion | check | observed on current tree | observed on fixture |
|---|---|---|---|
| 24 | `receipt-check.py RECEIPT...` | `tripwire-r13.txt` MISSING (no tool sha, no measured_commit); `tripwire-selftest-core.txt` MISSING (tool sha present, no measured_commit); `label-check-final.txt` MISSING (measured_commit present, no labelled tool sha); `frozen-tampered-recut.json` MISSING (measured_commit present, no labelled tool sha). `RECEIPT_SUMMARY: 0/4`, exit 1 | `receipt-green.txt` (labelled `tool_sha256` + `measured_commit`) ok, `1/1`, exit 0; missing file → UNKNOWN, exit 1 |
| 25 | `mutant-check.py RECEIPT.json` | `.ufo/waves/round-17/` has no mutant receipt → `MISMATCH no committed mutant receipt`, exit 1 | `mutant-green.json` (loose≠tight) → `ok`, exit 0; `mutant-equal.json` (loose=tight) → `MISMATCH loose and tight outputs identical`, exit 1 |
| 26 | `pipe-rc-fixture.sh` | — | `unguarded: git rc=128 became empty-input digest (FALSE VALUE)`; `guarded: UNKNOWN (producer rc=128)`; exit 0 (script prints both; the pass condition is the guarded line) |
| 26 | `pipe-rc-lint.py tools/*.sh` | `PIPE_RC_FLAGS: 9`, exit 1 (see findings) | — |

Each check fails on the current tree or on its red fixture, as the criterion text states.

## Findings (routed; not fixed here — lane files are L1/executor-owned)

1. **R17-V1 confirmed by the check.** Four committed round-17 receipts fail criterion 24 (`0/4`). `tripwire-selftest-core.txt` has a `SELFTEST_SCRIPT_SHA256:` label but no `measured_commit`; `label-check-final.txt` has `measured_commit=f71ccbe…` but no labelled tool sha. Other selftest receipts were not opened by this seat.
2. **Lint sites in `tools/mado-verify.sh`** (`PIPE_RC_FLAGS: 9`, no `PIPESTATUS` in the next two lines):
   - `:244` `done | sha256sum | cut`
   - `:942`, `:944`, `:1377`, `:1383` `find … | xargs sha256sum | sha256sum` (digest of a tree; a failed `find` yields a partial digest, not UNKNOWN)
   - `:1133` `wc -l` of `find` output, used as a count
   - `:2788` `wc -l` of `find` output (`nbak`)
   - `:3406` `git show HEAD:… | sha256sum` — **F10**, the empty-input value `e3b0c442…` on failed git, plus a false "local edit" FAIL; the `UNKNOWN` arm at `:3408` is unreachable.
   - `:3474` `find … | wc -l | tr -d ' '` (`nd`)
   The lint is a screen: `:244`, `:1133`, `:2788`, `:3474` may be harmless on success-only paths, but each needs an explicit decision (rc-guarded or noted as a non-value). A count of zero from a failed `find` is still a value under criterion 26.
3. **The `PIPESTATUS` idiom does not work inside `$(…)`.** `blob=$(a | b); grc=${PIPESTATUS[0]}` reads the parent shell's array, not the substitution's, so the guard must capture the producer output and `$?` separately. The fixture uses that form (`out=$(git show …); grc=$?`). The lint accepts a `PIPESTATUS` mention as a guard, so a line that uses it wrongly passes the lint. The fixture is the proof; the lint is only a screen. L1 should not cite the lint alone as clearance.
4. **Measure check is literal.** `measure.py` counts any line starting with a digit and dot. The three criteria add to that count only as intended because continuation lines are indented. A future criterion starting at column 0 without a number would not count; do not depend on it.

## Dependencies on other seats / L1

- `lessons/round-18.md` Mistakes rows M1 (receipt provenance, R17-V1/V2), M2 (mutant receipts, R17-V5), M3 (pipe status, jj F10) must exist with these ids.
- `.ufo/waves/round-18/checks/` must receive the four scripts below. Their sources are reproduced here so the commit is verbatim.
- The "tool sha" in criterion 24 must be recorded for both the measured revision and any later revision (R17-V2, separate row).
- C1 target 18/26 holds only if the three criteria are appended to `corpus/QUALITY.md` (L1 owns that file).

## Check sources (verbatim, for L1 to commit)

`receipt-check.py`:
```python
#!/usr/bin/env python3
"""Criterion 24 check: every named receipt carries a labelled tool sha256 and a 40-hex measured_commit.
Usage: python3 -I receipt-check.py RECEIPT... ; exit 0 only if all pass; 1 otherwise; unreadable -> UNKNOWN (counted as fail)."""
import re, sys
TOOL = re.compile(r'(?:tool[_ ]?sha(?:256)?|SCRIPT_SHA256)\W{0,6}[0-9a-f]{64}', re.I)
COMMIT = re.compile(r'measured_commit\W{0,6}[0-9a-f]{40}')
bad = 0
paths = sys.argv[1:]
for p in paths:
    try:
        text = open(p, encoding='utf-8', errors='replace').read()
    except OSError as e:
        print(f'UNKNOWN {p}: {e.strerror}'); bad += 1; continue
    t, c = bool(TOOL.search(text)), bool(COMMIT.search(text))
    ok = t and c
    bad += not ok
    print(f"{'ok' if ok else 'MISSING'} {p} tool_sha={t} measured_commit={c}")
print(f'RECEIPT_SUMMARY: {len(paths)-bad}/{len(paths)}')
sys.exit(1 if bad or not paths else 0)
```

`mutant-check.py`:
```python
#!/usr/bin/env python3
"""Criterion 25 check: an instrument tightening counts as biting only with a committed mutant receipt.
Usage: python3 -I mutant-check.py RECEIPT.json ; receipt keys: mutant, loose_instrument_sha256,
tight_instrument_sha256, measured_commit, loose_output, tight_output. Exit 0 only if all hold and loose_output != tight_output."""
import json, re, sys
REQ = ['mutant', 'loose_instrument_sha256', 'tight_instrument_sha256', 'measured_commit', 'loose_output', 'tight_output']
HEX64, HEX40 = re.compile(r'^[0-9a-f]{64}$'), re.compile(r'^[0-9a-f]{40}$')
def fail(msg):
    print(f'MISMATCH {msg}'); sys.exit(1)
if len(sys.argv) != 2:
    fail('usage: mutant-check.py RECEIPT.json')
try:
    r = json.load(open(sys.argv[1], encoding='utf-8'))
except OSError as e:
    fail(f'no committed mutant receipt: {e.strerror}')
except ValueError as e:
    fail(f'receipt not JSON: {e}')
missing = [k for k in REQ if k not in r]
if missing:
    fail(f'receipt lacks {missing}')
if not HEX64.match(r['loose_instrument_sha256']) or not HEX64.match(r['tight_instrument_sha256']):
    fail('instrument sha256 not 64-hex')
if not HEX40.match(r['measured_commit']):
    fail('measured_commit not 40-hex')
if r['loose_output'] == r['tight_output']:
    fail('loose and tight outputs identical: tightening does not bite on this mutant')
print(f"ok mutant={r['mutant']} loose!=tight measured_commit={r['measured_commit'][:7]}")
sys.exit(0)
```

`pipe-rc-lint.py`:
```python
#!/usr/bin/env python3
"""Criterion 26 static check: a digest/count taken through a pipe must capture the producer status.
Flags any line piping into sha256sum/md5sum/sha1sum/wc -l unless PIPESTATUS appears on that line or the next two.
A screen, not a proof: the fixture pipe-rc-fixture.sh is the behavioural check. Usage: python3 -I pipe-rc-lint.py FILE... ; exit 1 if any flagged site."""
import re, sys
SINK = re.compile(r'\|\s*(?:sha256sum|md5sum|sha1sum|shasum|wc -l)\b')
flags = 0
for p in sys.argv[1:]:
    lines = open(p, encoding='utf-8', errors='replace').read().split('\n')
    for i, ln in enumerate(lines):
        if SINK.search(ln) and not any('PIPESTATUS' in x for x in lines[i:i+3]):
            flags += 1
            print(f'UNGUARDED {p}:{i+1}: {ln.strip()[:120]}')
print(f'PIPE_RC_FLAGS: {flags}')
sys.exit(1 if flags else 0)
```

`pipe-rc-fixture.sh`:
```bash
#!/usr/bin/env bash
# Criterion 26 behaviour check: a failing producer must become UNKNOWN, never a digest value.
set -u
EMPTY=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
d=$(mktemp -d); mkdir -p "$d/bin"
printf '#!/bin/sh\nexit 128\n' > "$d/bin/git"; chmod +x "$d/bin/git"
export PATH="$d/bin:$PATH"
# (a) idiom at tools/mado-verify.sh:3406 — producer rc discarded
blob=$(git show HEAD:x 2>/dev/null | sha256sum | cut -d' ' -f1)
[ "$blob" = "$EMPTY" ] && echo "unguarded: git rc=128 became empty-input digest (FALSE VALUE)" || echo "unguarded: value=$blob"
# (b) guarded idiom — capture producer output and rc separately; failure -> UNKNOWN
out=$(git show HEAD:x 2>/dev/null); grc=$?
if [ "$grc" -ne 0 ]; then echo "guarded: UNKNOWN (producer rc=$grc)"; else echo "guarded: value=$(printf '%s' "$out" | sha256sum | cut -d' ' -f1)"; fi
rm -rf "$d"
```

## Out of scope / not done

- No edit to `corpus/QUALITY.md`, `lessons/`, `SCORECARD.md`, `tools/`, or `.gitignore`.
- No fetch receipts (no web source opened).
- Round-17 receipts were checked only for the labelled-field presence; their content was not re-measured.
- `mado-verify.sh` was not executed (it reads the host omarchy checkout); F10 was reproduced with the idiom and a stub git only.
