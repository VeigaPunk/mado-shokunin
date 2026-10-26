# RevSessionMarker — w2 falsify, R3: the marker gate and registry reviewed

Seat: `RevSessionMarker` (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Lane tip while this seat ran: `9bddd6ac89c75a9b164b5dcc313de6f7aef2096c` (w1 evidence); freeze `d7527d60`, base `60edb66e`.
Reviewed: `.ufo/waves/round-47/w1/ExecSessionMarker/` — the delivered marker gate
(`check-session-material.py`, 1599 L, sha256 `a4a0a084e745f511048d5be445bed4959a18b5d64798a55da06c74cc0d08e9c9`),
its registry install set (`demo/registry-round47.txt`, 49 rows; `demo/registry-round47-refreshed.txt`, 51 rows),
the sidecars, `demo/triage.py`, `demo/mark.py`, `demo/verify-claims.py`, `demo/run-demo.sh`, `demo/skill-row.md`,
and receipts 00-17 — against round-46 closure R3 (`corpus/lessons/round-46-verifier-spotcheck.md:113-116`) and
SKILL rule 4 (`SKILL.md:336-337`, session material stays shape-only). No serial value is printed anywhere in
this report or its receipts; every locator below was computed with `grep -n`, never typed.

Verdict up front: the routed item's requirement (marker + prose serial rule, shown able to fail both ways, as
receipts not claims) is met and reproduces exactly; the waiver layer is fail-closed in every tamper direction I
attacked, and nothing in the lane claims a green it does not have. **One hole is real and fixable only before
data: the reserved synthetic title namespace admits real-world window titles** (F1) — a waiver broader than
synthetic fixtures, demonstrated end-to-end. Four smaller gaps (F2-F5) are coverage/doc mismatches that should
be declared or fixed in the same re-registration.

## 1. Reproduction matrix (all re-run by this seat, receipts in `w2/RevSessionMarker/receipts/`)

| claim (w1 report) | my run | result |
|---|---|---|
| selftest 63/63 (`receipts/00-selftest.txt`) | `TMPDIR=<scratch>/tmp python3 -I <seat>/check-session-material.py --selftest` | `SELFTEST: passed=63/63 failed=0`, rc 0 (`selftest.txt`) |
| base findings=115 (old gate, receipt 01) | seat gate `--no-waivers` semantics at `60edb66` | `files=18371 findings=136` with R5; the landed old gate's own R1-R4 tally at base is inside that (`base-ufo.txt`) |
| gate+no-markers findings=136 (receipt 02) | seat gate at `60edb66`, scope ufo | `files=18371 findings=136` (`base-ufo.txt`) — exact |
| install state: waived 55/49, findings=84 (receipt 13) | scratch clone of base + gate + seat tree + sidecars + registry | `SESSION_MATERIAL_WAIVED: findings=55 files=49`; `findings=84` (R1=26 R2=29 R3=6 R4=2 R5=21) (`c3-with-markers.txt`) — exact |
| `--no-waivers` parity (receipt 15) | same tree, `--no-waivers` | `PARITY ok` reproduced by receipt; the marker layer is the only delta |
| scope-all adds 8 (receipt 16) | seat gate at tip `--scope all` | `findings=147` = 139 + 8: 3 held `corpus/knowledge/` R5 carriers + the landed gate's own constants + the two r37/r38 counter fixtures (`tip-all.txt`) |
| refreshed variant: waived 61/51, findings=78 (receipt 10) | tip clone + gate + refreshed registry + both stale copies refreshed | `SESSION_MATERIAL_WAIVED: findings=61 files=51`; `findings=78` (`tip-refreshed.txt`) — exact |
| claims checker 49/49 (receipt 17) | `demo/verify-claims.py --seat <seat>` | `CLAIMS_CHECK passed=49 failed=0` (`claims-check.txt`) |
| seat carries no host serial (receipt 11) | gate module's `host_serials()` counted as substrings over all 85 seat files + report | `SEATDIR_R6_SCAN: files=85 serial_hits=0` (`seatdir-r6-scan.txt`) |

## 2. Does the lane tip read green for the right reason?

**The tip does not read green under any state available today, and nothing claims it does:**

- The landed gate at the tip is still the **old** one: `quality/check-session-material.py` at `9bddd6ac` is
  682 L, sha256 `889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb` — zero hits for `MARKER_RE`,
  `R5_SERIAL_PROSE`, `serial-from-host` (grep over `git show HEAD:quality/check-session-material.py`). The
  SKILL-row entry command (`SKILL.md:770`) therefore runs the old gate: **`findings=118` (R1=30 R2=32 R3=54
  R4=2), exit 1** (`tip-landed-gate.txt`). The row itself declares this: "no synthetic marker yet, so a red
  exit is expected until it lands" (`SKILL.md:770`).
- The delivered marker gate without the install set: **`files=19179 findings=139`** (R1=30 R2=32 R3=54 R4=2
  R5=21), exit 1 (`tip-ufo.txt`) — no sidecars sit at their real paths and
  `quality/session-material-waivers.txt` is not tracked at the tip, so every marker would be refused
  `registry-absent` (fail-closed).
- With the install set applied at the tip: **waived 55/49, findings=84** (`tip-installed.txt`); refreshed
  variant: **waived 61/51, findings=78** (`tip-refreshed.txt`). The 84/78 are the w1 report §4 classes (real
  program rows, real titles, 3 serial dumps, 2 home listings, 1 vendor, 21 prose serials owned by the
  operator, 6 stale gate copies). Red is the honest state; `LOG.md:2521` records the round-46 red
  (`findings=115`) and `SCORECARD.md:2651` plans the install — no green is claimed anywhere.
- The install set still binds at the tip: the only tip-vs-base finding delta under scope ufo is the seat's own
  gate file (R1/R2/R3 on its selftest constants — `base-findings` vs `tip-findings` diff, 136 → 139), and the
  gate-copy row covers exactly those three. All 45 mons.json fixtures, `mutants.sh` and the two CritW2Gate
  files are byte-identical between base and tip (findings=84 at both states proves it).
- No waiver launders a real value in the actual tree: with `--serial-from-host` on the install state, R6 fires
  on 21 files and **none of them is a waived file** (`c3-r6.txt`, comm of R6 paths vs waived paths is empty);
  at the tip the 21 R6 carriers are all round-32/37 copies of the three held corpus entries (`tip-r6.txt`) —
  no round-47 w1 file carries the host serial.

So the answer is: there is no false green to attack today; the green that will be claimed after the owning
seats redact is safe **except through F1** (and the blind halves F2/F4/F5, which make a green weaker than it
looks rather than a wrong green).

## 3. Findings

### F1 (S2 — waiver broader than synthetic fixtures; fix before data) — the reserved title namespace admits real-world window titles

`SYNTH_TITLE_RE` (`w1/ExecSessionMarker/check-session-material.py:197-202`) second alternative is
`^(?:synthetic|fixture|selftest|probe|example|demo)(?:[ -][A-Za-z0-9 ._-]{0,60})?$` under `re.IGNORECASE`.
Any real title that begins with one of those six words and continues with a space/hyphen plus ≤60 chars of
`[A-Za-z0-9 ._-]` passes W4b. The docstring's own examples (`redacted`/`a live window title`/`synthetic-…`,
`:108-111`) undersell what the regex admits.

Repro (receipt `receipts/probe-waivers.txt`, script `probes/probe_waivers.py`, P1 block):

```
python3 -I .ufo/waves/round-47/w2/RevSessionMarker/probes/probe_waivers.py
```

A tracked clients dump whose single client is real-shaped (`class` a real app id, real pid) with title
**"Example Domain"** — the live `<title>` of the IANA-reserved domain example.com — plus a valid sidecar and
registry row is **WAIVED, exit 0**; the same for the bare real-world title **"Demo"**. The control (a real
title outside the namespace) is refused `value-not-synthetic:title-not-synthetic`, so the boundary is exactly
the namespace list. This is the one path by which a real value disappears: capture a session where a window's
title happens to start with example/demo/probe/…, mark it, register it, and the gate reads green for the wrong
reason. The w1 report §7 declares the adjacent residual (retitle a real window `redacted` → waivable, "the
outcome the policy wants for R1") but not this width; the collision set is real ("Example Domain" is not a
contrived string).

Not hit in the actual tree: the four R1-waived files' title values classify as known fixture words or round-46
fixture strings (checked by classification only, values not printed) — so today's waived=55/49 is clean. Fix
direction for a v2 registration: require the reserved word to be the whole value, or require a
`synthetic-`/`fixture-`/`selftest-`-style prefix **with** the delimiter mandatory and drop bare
example/demo/probe, or drop IGNORECASE for the prefix words; keep `redacted` exact-match.

### F2 (S3 — coverage gap vs the round's own material set) — R3 is blind to a monitors dump with a real description but an empty/redacted serial

`_monitor_reason` (`:239-247`) requires a non-empty `serial` before description/make/model are even looked at,
and the selftest pins that as intended (`r3-empty-serial-clean`, `:1015`). But the round-47 goal and the
gate's own header question (`:8-11`) name "monitor serials/**descriptions**" as the material — the
description half is covered only when a serial is present. Repro (probe P2): a dump with real make/model/
description and `"serial": ""` → exit 0, no finding. No live instance in the tree (the committed
`"serial": ""` grep hits are not monitor objects — checked by key parse). The tool docstring declares the
rule's shape (`:112` "Redacted/empty serials do not match") but the w1 report's §7 residual list does not;
declare it there, or cover the serial-less case, in the same v2.

### F3 (S3 — caller-relocatable trust anchors) — `--waivers`/`--gate-source` accept any tracked non-`.ufo` path

`load_registry` (`:568-571`) refuses only registries under `.ufo/`; W1's "the waiver list is one reviewable
lane file outside the artefact tree" (`:104-106`) is enforced for the default path only. Repro (probe P3): a
registry at `notes/waivers.txt` is honoured via `--waivers notes/waivers.txt` and the waiver applies. Same
class: `--home-limit` raises the R4 threshold, `--scope ufo` hides everything outside `.ufo/`. The canonical
SKILL-row command pins the defaults, so this is a residual for anyone re-running the gate with flags — worth
one sentence in the SKILL row's pinned-value cell, not a code change.

### F4 (S3 — declared-by-construction, header question overpromises) — titles in prose and non-JSON renderings are invisible

R1 is JSON-object-scoped (`scan_json_objects` needs the literal `"class"` substring); a real window title in
prose produces no finding (probe P4, exit 0), and neither does a plain-text (non `-j`) clients listing. The
gate's header question (`:8-11`) asks about "live window titles" without the JSON qualifier the rules
implement. No shape rule for titles exists without a value list (the R6 pattern), so this is structural — but
it should be a named residual in the report/skill row, not implicit. (R2, by contrast, is a plain regex over
the whole text and does catch prose `ss` rows.)

### F5 (S3 — doc/behavior mismatch with a silent blind half) — blobs above 16 MiB are scanned only over their head, and both docstring claims about that are wrong

`decode()` (`:322-327`) truncates at `MAX_TEXT = 16 << 20` (`:154`). The docstring (`:131-134`) claims large
files are "scanned for R2/R4 only, and their object scan reports `truncated=True`". Measured
(`receipts/probe-bigfile.txt`, script `probes/probe_bigfile.py`): material placed **beyond** the cap → exit 0,
no finding, no `truncated=True` (that flag fires only on the 20000-object limit, never on size truncation);
the same material inside the cap of an equally large file → R1+R2 fire. So large files are scanned for **all**
rules but only over the first 16 MiB, and the tail is silently invisible. A >16 MiB receipt with a dump in its
tail reads green. Fix: correct the docstring and either scan large files in chunks or print a
`size-truncated=True` marker.

## 4. What I attacked that held

- **The serial rules are structurally outside the waiver surface.** `MARKER_RE` (`:185-190`) accepts `R[1-4]_…`
  only; `apply_waivers` refuses a serial finding on a marked file before parsing the marker (`:623-626`);
  registry rows are validated against `WAIVABLE_RULES` (`:583-585`). Selftest cases
  `waiver-serial-rule-not-waivable`, `waiver-marker-cannot-name-serial-rule`,
  `waiver-real-serial-marked-file-kept`, `prose-serial-unmarked-kept` all reproduced inside my 63/63 run.
- **Fail-closed in every tamper direction:** appending a real dump to a waived file → `sha-mismatch`; sidecar
  without registry row → `unregistered`; registry absent at the scanned rev → `registry-absent`; registry
  under `.ufo/` → `registry-in-ufo`; target outside `.ufo/waves/` → `path-outside-waves`; altered gate copy →
  `gate-source-mismatch`; unlisted rule → `rule-not-listed`; real identity value → `value-not-synthetic:*`.
  Each is pinned by a selftest case; the w1 demo cases 3-5 (plant, append-into-waived, register-a-real-serial)
  are the end-to-end forms and their receipts hold the named reasons.
- **The generator cannot launder.** `demo/triage.py` writes markers for every waivable finding path, lets the
  gate decide in pass A, keeps only what the gate waived, and refuses to finish unless pass B waives and keeps
  exactly what pass A did (`triage.py:196-201`) — the registry can only contain rows the gate accepted.
- **`verify-claims.py` is substantive** (exact receipt-string assertions, 49 checks) and passes on re-run.
- **No flag drops a rule**: `--rules` is an argparse error (selftest `e2e-no-rule-can-be-dropped`); R6 is
  additive and its failure mode is exit 2, never a silent pass (`host_serials` raises on any failure, `:431-446`).
- **The both-ways requirement of R3 is met**: synthetic findings disappear (136 → 84 with the marker layer,
  parity under `--no-waivers`), real values do not (cases 3/4/5) — as receipts, and the SKILL/SCORECARD record
  claims nothing more.

## 5. Recommendation

Before the data commit, re-register the marker gate as v2 (the freeze is not yet consumed by any data) with:
(1) F1's title namespace tightened to the documented examples; (2) F2 either covered or declared in the
report's residual list; (3) F5's docstring corrected (and the tail either scanned or marked); (4) F4 named as
a residual in the report and the SKILL row; (5) F3 documented in the SKILL row's pinned-value cell. Everything
else — the registry content, the sidecar set, the refreshed variant, the triage generator, the claims checker
— reproduced exactly and needs no change.

## 6. Method and safety

Read-only over the lane: `git log/ls-tree/show/grep`, file reads, the seat gate run against the lane at
`60edb66`/`9bddd6ac` (it reads blobs via `git cat-file`, touches no worktree). Fixture clones and all probes
lived under `/fast/scratch/hyaku/mado-r47/RevSessionMarker/` (deleted at the end; every cited receipt was
copied into `w2/RevSessionMarker/receipts/` first); every fixture clone asserted
`git rev-parse --show-toplevel` equal to its own directory before any commit, and commits used a scratch
identity only. Compositor access: three `hyprctl monitors all -j` read verbs (twice inside the gate's
`--serial-from-host` mode, once for the seat-dir serial scan), no write verb, no terminal, no GUI program, no
pacman, no installs (Python 3 stdlib + git only). No serial value was printed or persisted; gate and probe
output is value-free by construction, and the seat-dir scan (`seatdir-r6-scan.txt`) confirms neither the w1
seat's artifacts nor this report carries one.
