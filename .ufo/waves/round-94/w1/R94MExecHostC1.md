# R94MExecHostC1 — host name list + agreement + harm baseline (round 94, wave w1)

Seat: R94MExecHostC1 · 2026-11-07 · lane tip during work: `5a164538438c2f101e44a79ad9e05aaf3ca910fb`
(base `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` + the round-94 dispatch-evidence commit; tree dirty count 5 = other seats' in-flight wave files, untouched by me).

Godspeed axes for this seat: **(a)** host-name-list fidelity (does it stress the real globs2 surface), **(b)** oracle↔candidate agreement coverage, **(c)** harm-watch breadth and script correctness. Kept moves: seeded reproducible synthesis, byte-exact escaping contract, r93-faithful harm script. No move narrowed a claim.

## Deliverables written

| file | what |
|---|---|
| `.ufo/waves/round-94/controls/mimeglob-host-names-r94.txt` | frozen host name list, sha256 `4b6d6a6cc67a4ad59eb91c9e8af1cc605f2f278d2a2ecf57b4a81edad9344fa3` |
| `.ufo/waves/round-94/controls/harm-r94.sh` | round-94 harm watch (r93 watch + new C1 tool selftest), scratch-rooted |
| `.ufo/waves/round-94/w1/R94MExecHostC1-gen-names.py` | generator (copy of scratch script, cited below) |
| `.ufo/waves/round-94/w1/R94MExecHostC1-run-agreement.py` | oracle/candidate runner (copy of scratch script, cited below) |
| `.ufo/waves/round-94/w1/R94MExecHostC1.md` | this report |

No tool installs or upgrades were needed; none performed.

## 1. Host name list

Built only from glob patterns of the host's globs2 files, in xdgmime search order:
`/home/vgpnk/.local/share/mime/globs2` (162 B) then `/usr/share/mime/globs2` (52100 B); `/usr/local/share/mime/globs2` absent.
Both files decode as strict UTF-8. `patterns_sha256` (the two files' bytes concatenated in that order) =
`4022804f86c14b8a0cd8db461dcc88a49ff700d77b3d5c69807c54dc34f05250`.
Header line (the file's only comment line, so a counter can parse `lines[0]` as header, `lines[1:]` as names):

```
# mimeglob host names r94 seed=94 patterns_sha256=4022804f86c14b8a0cd8db461dcc88a49ff700d77b3d5c69807c54dc34f05250
```

Input scan: 1615 data lines → **1374 distinct patterns** (2 `__NOGLOBS__` sentinel lines skipped; 5 lines carry the 4th-field `cs` flag; no pattern contains `:` or `/`).
Per pattern (seed `94`, generator `w1/R94MExecHostC1-gen-names.py`):

- the literal itself;
- `*`→`x` name;
- UPPER variant (bytes.upper), Title variant (bytes.title), leading-`A` variant;
- a full-glob instance (`*`→`chunk`, `?`→`q`, `[...]`→first member / `z` for `[!...]`, `{a,b}`→first alt);
- a two-extension variant (`xname` + rotating `.gz/.tar/.bak/.new/.orig`) for dot-bearing names — the `x.tar.gz` shape (skipped for the 18 patterns whose `x`-name has no dot: `9600 = 1374×7 − 18`).

Plus **300 seeded random non-matching names** (`random.Random(94)`; consonant/vowel words, optional second word, extensions from `.zqx/.qv9/.xz/.wqk/.jv`/none; a candidate is kept only if it matches no pattern — `fnmatch.translate` regexes, case-insensitive for non-`cs` rows, case-sensitive for the 5 `cs` rows — and collides with no earlier name).
Sorted by raw bytes, deduplicated: **9745 names** (9600 derived + 300 random; 9608 contain `.`).

**Escaping contract (documented as required):** any byte outside printable ASCII `0x20–0x7E`, and a literal backslash `0x5C`, is written as `\xHH` (uppercase hex); consumers decode every `\xHH` back to the raw byte before passing the name as argv (`re.sub(rb"\\x([0-9A-F]{2})", …)`, runner cited below). In this list **0 of 9745 names required escaping** — every host glob pattern is printable ASCII — so the contract is defined and exercised by the runner's decoder but no line uses it. Every command below consumed the list through that decoder.

## 2. Oracle vs candidate on the whole list — AGREEMENT 9745/9745 (DRAFT run)

Environment used for both tools (my own shell's values, printed as required):
`HOME=/home/vgpnk` `XDG_DATA_HOME=/home/vgpnk/.local/share` `XDG_DATA_DIRS=/usr/local/share:/usr/share`.

- Oracle: `gcc -O1 -o $S/oracle controls/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)` (build OK), then
  `env -i LC_ALL=C HOME=/home/vgpnk XDG_DATA_HOME=/home/vgpnk/.local/share XDG_DATA_DIRS=/usr/local/share:/usr/share $S/oracle <names…>`.
- Candidate: `python3 -I .ufo/waves/round-94/build/mado-mimeglob.c1.py --json --home /home/vgpnk --data-home /home/vgpnk/.local/share --data-dirs /usr/local/share:/usr/share <names…>`, 500 names per invocation, results compared per name (type and uncertain flag).

Result: **`AGREEMENT 9745/9745 mismatches=0`**; candidate `mode: cache` (both the user and system mime dirs carry a valid `mime.cache`), oracle rc 0, candidate rc 0 on every chunk, mismatch file empty.
This is a DRAFT run against the unfrozen candidate (sha256 `0700915a…d63e` per the dispatch context); the predicate (iii) measurement happens post-freeze at `<rev>`. The runner (`w1/R94MExecHostC1-run-agreement.py`) aborts on any rc≠0, so an `UNSUPPORTED` refusal would have been reported, not silently scored.

Note: on this host the candidate answers entirely from cache mode; text mode (`globs2` without `mime.cache`) is exercised by the frozen cases (other seats), not here.

## 3. Harm baseline at base a3de9972 (+dispatch commit), enumerated commands

All run from the lane root against the working tree; full outputs kept in scratch (summarized here; scratch deleted after). Every check rc=0:

| # | command | rc | result line |
|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | 0 | `MADO_SELFTEST: 460/460 assertions passed` |
| 2 | `bash tools/mado-verify.sh --no-live` | 0 | `counts: pass=29 fail=0 unknown=0 skip=8 note=4` / `MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only — live layer skipped: --no-live)` |
| 3 | `python3 -I tools/mado-portals.py --selftest` | 0 | `MADO_PORTALS_SELFTEST: checks=28 failed=0` |
| 4 | `python3 -I tools/mado-mime.py --selftest` | 0 | `MADO_MIME_SELFTEST: checks=17 failed=0` |
| 5 | `python3 -I tools/mado-xdgmime.py --selftest` | 0 | `MADO_XDGMIME_SELFTEST: checks=12 failed=0` |
| 6 | `python3 -I tools/mado-mako.py --selftest --scratch-root $S/mako` (mkdir first) | 0 | `MADO_MAKO_SELFTEST: checks=62 failed=0` |
| 7 | `python3 -I quality/check-seat-reports.py --selftest` | 0 | `SEAT_REPORTS_SELFTEST: checks=23 failed=0` |
| 8 | `python3 -I quality/check-receipt-presence.py --selftest` | 0 | `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0` |
| 9 | `python3 -I quality/check-selftest-strength.py --selftest` | 0 | `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` |
| 10 | `…check-selftest-strength.py --tool quality/check-seat-reports.py --kills quality/selftest-kills/check-seat-reports.json --scratch-root $S/ss` | 0 | `SELFTEST_STRENGTH: OK tool=quality/check-seat-reports.py kills=32 held=32 survived=0 wrong_check=0` |

Extra DRAFT evidence: `python3 -I .ufo/waves/round-94/build/mado-mimeglob.c1.py --selftest` → rc 0, `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0`.

### Index/ledger gate commands (from SKILL.md + round-93 artifacts)

Round 93's harm watch ran the two record gates as
`python3 -I quality/check-index.py --repo . --rev "$REV"` and `python3 -I quality/check-tool-ledger.py --repo . --rev "$REV"`
(`.ufo/waves/round-93/controls/harm-r93.sh:6-7`; both rc=0 in `.ufo/waves/round-93/receipts/harm-final-r93.txt`).
SKILL.md documents the same instruments: line 923 lists `quality/check-index.py` as the instrument of the `mado-axis-scores` gate; lines 2579-2581 document `quality/check-tool-ledger.py` and its `--scratch-root` waiver semantics. My smoke run confirmed both still pass at the current tip:

```
MADO_INDEX: rev=5a164538438c2f101e44a79ad9e05aaf3ca910fb indexed=114/114 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   rc=0
LEDGER: population=179 ledger_rows=179 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=5a164538…   rc=0
```

### harm-r94.sh (mine) and its DRAFT smoke run

`.ufo/waves/round-94/controls/harm-r94.sh REV SCRATCH` re-runs the whole round-93 watch — verify --selftest/--no-live, check-index, check-tool-ledger, mako (with the round-93 `mkdir "$S/mako"` correction built in), portals, mime, xdgmime, seat-reports, receipt-presence, selftest-strength selftest + gate on the live kill-set, the r90/r92 C2 counters with their pinned shas, the expected-SETUP_ERROR r90 C1 counter, and the `git diff --stat 4c6f723f… REV` protected-tools check — **plus** the new tool's selftest `python3 -I tools/mado-mimeglob.py --selftest`, guarded by an existence check that prints an explicit `SKIP … rc=NA` line until the L1 integrates the candidate as `tools/mado-mimeglob.py`. `run()` prints each command and `rc=${PIPESTATUS[0]}` (round-93's grep filter `^(case|probe|fresh|mutant) ` kept verbatim); `TMPDIR` and every scratch-root live under the caller's SCRATCH. A trailing comment tells the L1 to append the r94 C2 counter line once `quality/counters/c2-r94-selftest-kills.py` lands.

Smoke run at the current tip (DRAFT/baseline; `REV=5a164538…`, SCRATCH under my scratch): script rc=0; all 17 executed checks rc=0 (verdicts identical to the table above, plus `MADO_RECEIPT_PRESENCE: … expectations=83 met=83 … mutants=28 killed=28` and `MADO_GATE_DEFECTS: TARGET_MET … fixtures=45 met=45 fresh=60/60 mutants=37 killed=37`); the one rc=2 line is the declared-expected refusal `MADO_PORTAL_ROUTING: SETUP_ERROR fresh leg: oracle run incomplete` (round-90 C1 counter on the ported tool — same expected-SETUP_ERROR class as the r93 receipt, different refusal leg); one SKIP line for the not-yet-integrated `tools/mado-mimeglob.py`; protected-tools diff empty. Nothing wrote outside my scratch; no receipt was written (frozen zone respected).

## Risks / notes for the L1

- `patterns_sha256` covers the **user** mime DB too (`~/.local/share/mime/globs2`); if `update-mime-database` rewrites it before the freeze, regenerate the list with the same seed and re-pin. The counter should pin the list **file** sha (`4b6d6a6c…`), which freezes content regardless.
- If a future host drops `mime.cache` from any xdgmime dir, the candidate flips to text mode wholesale (cache-only rule); the agreement result here is a cache-mode result.
- The seed (`94`) and the escaping contract live in this report + the generator copy; the list itself carries only the mandated single header line.
- Harness quirk observed (no action needed): `bash` tool calls raced in this seat's session and one long check (`verify --selftest`, 114.8 s) ran as a background job — its rc/result line above is from that completed job.

Scratch `/fast/scratch/hyaku/mado-r94/R94MExecHostC1` deleted after copying cited artifacts (final state checked below).
