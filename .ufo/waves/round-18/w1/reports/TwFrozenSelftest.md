# TwFrozenSelftest — round 18 / wave 1

Seat: `MadoR18.TwFrozenSelftest` (leaf executor). Scope: the frozen-mode selftest
suite under `.ufo/waves/round-18/tripwire/frozen/` only, plus this report.

## 1. Deliverable

Created **only** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen/`:

- `expected.json` — outer suite, schema `mado-tripwire-selftest-v1`, **17 cases**, every
  case `"mode": "frozen"` with `want_exit` and `want_label`. sha256
  `a75f4db4b21474a654c8a548ad85f3fffd89b77e054b4e7bc6522a5f0a2522d5`.
- 17 fixture directories, each with its own `expected.json` (schema
  `mado-tripwire-frozen-v1`, digest-pinned `inputs`, `permit`, `expected_exit`,
  `expected_label`, `expected_findings`, optional `known_misses`) and `inputs/`:

```
match-findings            match-clean              match-permitted-only
match-permit-partial      verdict-missing-finding  verdict-extra-finding
verdict-exit-label        known-miss-violated      tampered-input-byte
missing-input             extra-unlisted-input     symlink-input
path-traversal            absolute-input           unpinned-entry
malformed-expected-json   wrong-schema
```

All JSONL is **synthetic OMP-shaped** (assistant `toolCall` records only); no real
transcript bytes, no host observation. Case dirs are portable: paths are relative,
pins are content digests only.

## 2. Landing timeline (tool digest drift observed)

`tools/mado-tripwire.py` was under concurrent edit throughout this wave (frozen mode
plus other fixes), so these are observed snapshots — not one authoritative revision:

| observed sha256 (abbrev) | state | frozen suite | existing suites |
|---|---|---|---|
| `962919ce…` (task start) | no `--frozen` anywhere in the file | not runnable | n/a |
| `593b3aaf…` (first frozen landing) | `--frozen`, `MADO_TRIPWIRE_FROZEN:`, frozen selftest branch | 17/17, rc 0 | 88/88 |
| `3e791ee…` | frozen block behaviourally unchanged (`+256/−10` lines elsewhere) | 17/17, rc 0 | 88/88 |
| `762cf56f…` | further edits elsewhere; suite re-run only | 17/17, rc 0 | not re-run |
| `c87a31ef…` (latest observed at report write) | further edits elsewhere; suite re-run only | 17/17, rc 0 | 88/88 |

The frozen block (`validate_frozen`, `frozen_snapshot`, the comparison and the
selftest branch) was re-read in full at `593b3aaf` and `3e791ee`; at the last two
revisions the file kept moving, so the suite and coexistence passes were simply
re-established rather than re-read. Because of that drift, L1 must re-run the suite
once after the last integration edit. The suite is digest-agnostic — relative paths,
content-only pins — so no fixture change is needed for that re-run.

## 3. Case table

`fixture exit/label` = the fixture's own `expected_exit` / `expected_label`;
`want` = the outer case's `want_exit` / `want_label` (outcome word after
`MADO_TRIPWIRE_FROZEN: `).

| # | case | defect isolated | fixture exit/label | want exit/label | observed detail |
|---|---|---|---|---|---|
| 1 | `match-findings` | true replay: 2 findings on line 1 + honest `known_miss` on line 2 (`ls -la …`) | 1 / findings | 0 / frozen_match | scan exit 1, label findings, multiset exact, missing=[] extra=[] |
| 2 | `match-clean` | clean replay, `known_misses` omitted (optional key) | 0 / clean | 0 / frozen_match | scan exit 0, label clean |
| 3 | `verdict-missing-finding` | expected row that never occurs (`package_query pacman:-Q`) | 1 / findings | 1 / frozen_verdict_mismatch | `missing_findings=[pacman:-Q]`, `extra_findings=[]` |
| 4 | `verdict-extra-finding` | expected list omits observed `pacman:-Syu` | 1 / findings | 1 / frozen_verdict_mismatch | `extra_findings=[pacman:-Syu]`, missing=[] |
| 5 | `known-miss-violated` | `known_misses` asserts line 1, which does yield findings | 1 / findings | 1 / frozen_verdict_mismatch | forces rows into `extra_findings` (`sudo`, `pacman:-Syu`) |
| 6 | `tampered-input-byte` | one byte differs from pin (id `a1`→`b1`; still valid JSON, identical classification) | 1 / findings | 2 / snapshot_tampered | `error: snapshot does not match its pin` |
| 7 | `missing-input` | listed `inputs/absent.jsonl` absent | 1 / findings | 2 / snapshot_tampered | lstat fails before any scan |
| 8 | `extra-unlisted-input` | stray `inputs/stray.jsonl` not listed | 0 / clean | 2 / snapshot_tampered | listed pin itself is valid; only defect is the stray file |
| 9 | `symlink-input` | listed `inputs/link.jsonl` → `payload.txt` | 0 / clean | 2 / snapshot_tampered | detected via `lstat` before digest |
| 10 | `path-traversal` | listed `../x.jsonl` | 0 / clean | 2 / snapshot_tampered | `..` component rejected |
| 11 | `unpinned-entry` | entry has no `sha256` key | 0 / clean | 2 / unpinned_legacy | `error: input entry without sha256` |
| 12 | `malformed-expected-json` | truncated JSON (unparseable) | — | 2 / frozen_error | `expected.json not JSON (JSONDecodeError)` |
| 13 | `wrong-schema` | valid object, `schema` = `mado-tripwire-frozen-v0` | 0 / clean | 2 / frozen_error | `error: bad schema` |
| 14 | `match-permitted-only` | `permit=[package_query]`, only `pacman:-Qi` | 0 / permitted_only | 0 / frozen_match | permitted-only replay |
| 15 | `match-permit-partial` | `permit=[package_query]`, `host_mutation` remains unpermitted | 1 / findings | 0 / frozen_match | multiset includes both classes |
| 16 | `absolute-input` | listed `/tmp/not-a-snapshot.jsonl` | 0 / clean | 2 / snapshot_tampered | absolute path rejected |
| 17 | `verdict-exit-label` | finding multiset exact, but expected exit/label disagree (0/clean vs scan 1/findings) | 0 / clean | 1 / frozen_verdict_mismatch | isolates exit/label comparison from the multiset |

Input pins (full sha256): `incident.jsonl`
`cafde03a0290c1afef61f53b2e64b11f52b3bfa9251a0f2f247d46aedb011829`;
tampered copy `ca9340e7a46ed302d1e84bf1d996fdeee26323c9f2545d43353bf09054c897b4`;
`clean.jsonl` `cb6090d8f281e3d09fc70663ba903e6858f468fcb2fef3c00b0da779cda08660`;
`query.jsonl` `d82c42a468427cb2a51d500bc26dfb4c10acdc1e159efa9cd4ae6120e13a81ab`;
`mixed.jsonl` `04ba81e407b7ac897c22dbbb27419f4aaba63afe37f4489a4c749e193be019c1`;
`stray.jsonl` `9e4a5349351ae6901ad8bbb68e406f9ed99d07f780a470a2a849c9ce28f616d7`;
`payload.txt` `8f10562a852a4017747a5fb94afc0bdad1dc7ea3ce8c9951f9b9d106f73ef59f`;
`placeholder.txt` `0e69843553b8c53f60fa5436e2a0d10cb23f9aa0d9b60ac42f0d8e23232a6e30`.

## 4. Validation actually exercised

1. **Builder/validator** (`/tmp/twf-build.py`, run `python3 -I`): deterministic build;
   re-parsed every fixture `expected.json`; checked suite schema, unique names, case-dir
   existence, `want_exit`↔`want_label` mapping (match 0, verdict mismatch 1, error paths 2),
   finding `file` ∈ listed inputs, class ∈ {host_mutation, package_query, live_probe},
   every pin against bytes, and the unlisted-`*.jsonl` probe. Intended defects exempted by
   name only (`tampered-input-byte`, `wrong-schema`), and both asserted present.
   Result: `cases=17 … VALIDATION OK`.
2. **Classifier truth**: the existing `--scan` was run on the ordinary inputs of the eight
   non-defect fixtures; declared `expected_findings`/exit/label equal scan output exactly
   (e.g. `match-findings` → exit 1, `findings`, `[sudo@1, pacman:-Syu@1]`;
   `match-permitted-only` → exit 0, `permitted_only`, `[pacman:-Qi@1]`).
3. **Independent contract model** (`/tmp/twf-modelcheck.py`): re-implements the documented
   order *without importing the tool* — parse → schema/type → absolute/`..`/symlink/
   non-regular/missing + unlisted walk → pin presence → digests → scan → exit/label/
   multiset/known_misses. Modelled outcome == declared outcome+exit for **17/17**,
   `mismatches=0` (this ran before the mode landed, proving the fixtures encode the
   contract and not the implementation).
4. **Landed implementation runs**:
   `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen`
   → every `CASE … ok`, `SELFTEST_SUMMARY: 17/17 passed failed=[]`, **rc 0 at each of
   the four observed frozen-capable revisions** (`SELFTEST_SCRIPT_SHA256`:
   `593b3aaf…`, `3e791ee…`, `762cf56f…`, `c87a31ef…`; see §2).
5. **Coexistence** (unchanged suites, same run window):
   core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30 — 88/88 passed.
6. **Raw verdicts spot-checked** for `tampered-input-byte` (`snapshot_tampered`, rc 2,
   `inputs[0].ok=false`), `verdict-missing-finding` (`missing_findings=[pacman:-Q]`),
   `verdict-extra-finding` (`extra_findings=[pacman:-Syu]`),
   `known-miss-violated` (both line-1 rows forced into `extra_findings`),
   `match-permitted-only` (`scan_label=permitted_only`, rc 0).

## 5. Contract points these fixtures pin

- `schema` is validated **by value** (`bad schema` → `frozen_error`); this was the only
  reading asserted beyond "missing key / bad type", and the landed code confirms it.
- Path checks precede pins: absolute path, `..` component, `lstat` symlink, non-regular,
  missing, and any unlisted `*.jsonl` under `DIR/inputs` → `snapshot_tampered`.
- A pin-less entry is `unpinned_legacy`, checked after paths and before digests.
- Digest comparison is over raw bytes; the pin may be upper/lower case
  (implementation strips/lowercases) — fixtures pin lowercase hex.
- A `known_miss` line that does yield a finding forces those rows into
  `extra_findings` (no separate outcome).
- The frozen selftest branch compares **exit + first line only**; `want_findings` is
  ignored. Each case still carries `"want_findings": []` so the outer file is also
  consumable by the pre-frozen runner path without a schema change.
- The symlink fixture is fail-safe under checkout systems that materialise symlinks as
  regular files: the pin then mismatches and the case still resolves to
  `snapshot_tampered`.

## 6. Risks / notes for integration

1. **Location is round-scoped.** The suite lives under `.ufo/waves/round-18/…` as assigned.
   If the gate should be durable beyond round 18, move the directory (e.g. under `tests/`);
   relocation is safe because all fixture paths are relative and pins are content digests.
2. **Pins bind classifier behaviour.** Any intentional classifier change that alters replay
   makes `match-*`/`verdict-*` cases fail by design — that is the frozen-gate property and
   requires a re-pin, not a fixture edit.
3. **Two fixtures encode contract readings** (`wrong-schema`, `absolute-input`). Both were
   confirmed against the landed code; a future loosening of either check will (correctly)
   fail the suite.
4. **No real-transcript coverage here.** This suite is synthetic by assignment. The
   real-transcript frozen replay is the separate `frozen-tripwire/` snapshot owned by
   another seat; nothing in this suite substitutes for it.
5. `.ufo/waves` is git-tracked and not ignored (`git check-ignore` rc 1), so the fixtures —
   including the one relative symlink — are committable as-is by L1.

## 7. Non-claims

- No host binaries were run; no `pacman`/`systemctl`/`journalctl`/`hyprctl`/omarchy
  commands, no compositor or service operations.
- No web fetches (so no fetch receipts), no tool installs, no `git`/`jj` writes, no OMP
  transcripts or `agent.db` reads.
- Only the assigned suite files and this report were written.
