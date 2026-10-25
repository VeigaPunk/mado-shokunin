# RevC1v3 — C1 v3 counter review (round‑38 wave‑1)

Reviewer: `L1Mado38.RevC1v3` · date 2026‑10‑25 · lane `mado-shokunin`
Object: `quality/counters/c1-r38-event-ground.py` (`PRED-C1-r38-v3`) against the registration's C1 v3 spec
(`.ufo/waves/round-38/registration.md`), including the two mandated runs.
Blob identity: worktree sha `6872e18d3003b5fcbf94adac4b259a4a3651d313e848dda8999572851fe71866` ==
`b6c1d31:quality/counters/c1-r38-event-ground.py` (verified) — the code reviewed is the code at the measured rev.
No tool installs were made (stdlib/git only). Lane bounds respected: read-only on production files; scratch under
`/tmp/mado38-RevC1v3/` and this report only.

The counter's docstring is the operative clause text: a–g are v2's (defined in
`c1-r37-event-ground.py` docstring), h–l are v3 additions (defined in the v3 docstring). The registration's C1
deliverable sentence maps to h (pin binding), i (located-quote floor), j (unique registry rows), k (parsed header
values), l (lineage floor). The registration's *four fixture cases, `lagging=0`, read-only clause, three-artifact
live clause* belong to `c2-r38-eventq.py`, not this file.

## Evidence runs (exact commands, quoted output)

### 1. Counter at rev (registration counting command, direct instrument run)
```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev b6c1d3124555d7d4c38bc467d85d5efa4a65c053
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S189,S201,S212 lineage=6/4 ok=1
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S189,S213,S214,S215,S216,S217 lineage=2/2 ok=1
PRED-C1-r38-v3 admitted=2/2 verdict=TARGET_MET rev=b6c1d3124555d7d4c38bc467d85d5efa4a65c053 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
exit=0
```

### 2. Counter at base
```
$ python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev b4e47e980bfb0cbc8a4e788f59a41db858751fd8
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 h=0 j=0 k=0 l=0 ids=- lineage=0/4 ok=0
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 h=0 j=0 k=0 l=0 ids=- lineage=0/2 ok=0
PRED-C1-r38-v3 admitted=0/2 verdict=TARGET_MISSED rev=b4e47e980bfb0cbc8a4e788f59a41db858751fd8 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
exit=1
```
Base semantics independently confirmed: `git ls-tree b4e47e98 -- corpus/knowledge/{event-delivery-limits-r26.md,event-queue-observability-r37.md}` → both ABSENT; precondition (frozen tokens at base) passed (exit 0 run ⇒ no exit 2), corroborated by `git grep -n -e 'MAX_QUEUED_EVENTS' -e 'overflowed event queue' -e 'debug:disable_logs' -e 'm_logsEnabled' b4e47e98 -- corpus/knowledge` → no matches, rc=1.

### 3. Discrimination gate at b6c1d31 (registration's counting command)
```
$ python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-38/controls/manifest.json --rev b6c1d3124555d7d4c38bc467d85d5efa4a65c053
control=c1-live instrument=c1 expected=TARGET_MET observed=TARGET_MET ok=1
control=c1-donothing instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-selfreceipt instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-quotefloor instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-nolineage instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-r28-verbatim instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-token-stub instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c1-clause-b instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-live instrument=c2 expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-donothing instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-forged instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-impsock instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-lagconst instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-missall instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-onepass instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-docconn instrument=c2 expected=TARGET_MET observed=TARGET_MET ok=1
control=c2-stub-clean instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
control=c2-proc-mismatch instrument=c2 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
exit=0
```
Note: a first invocation (09:18-ish, HEAD=bb1adce) crashed `NameError: name 'shutil' is not defined` (at `shutil.rmtree` after control 1, no output). Not reproducible on the settled file: the gate script changed mid-session under concurrent sibling work (worktree sha `c4bad89d…` → `581bf2ed…`; `import shutil` now at line 31). The settled file runs clean (above).

### 4. PINS digests vs `sha256sum` of committed receipts at b6c1d31
```
$ git -C LANE show b6c1d31:.ufo/waves/round-37/fetch/<f> | sha256sum   (per pin)
eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d  S189.bin
799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e  S201.bin
1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9  S212.bin
1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58  S213.receipt.txt
d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868  S214.bin
a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754  S215.bin
74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0  S216.bin
aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe  S217.bin
```
All 8 == PINS == the `GATE`-declared digests in `corpus/lessons/round-37.md` (`## Gate`, lines 28–37). Receipts are byte-identical between the round-37 tip `f6e3247` and `b6c1d31` (`git diff f6e3247 b6c1d31 -- .ufo/waves/round-37/fetch` empty).

## Clause-by-clause: implementing code vs spec sentence

| Clause | Spec sentence (source) | Implementing code (file:line) | Verdict |
|---|---|---|---|
| a | "the entry exists at REV and did not exist at BASE" (v2) | `c["a"] = int(body is not None and show(repo, base, path) is None)` (190–193) | MATCHES (verified ABSENT at `b4e47e98`, present at rev) |
| b | "its first 15 lines carry `source:`, `verified-at:` and `recheck:`; the `source:` lines name at least one S-id" (v2) | `head = body.splitlines()[:15]` (195); `src_lines` regex `^[-* ]*source *:` (196); `ids = sorted(set(re.findall(r"\bS\d{3,}\b", " ".join(src_lines))))` (197); line-presence checks (198–201) | MATCHES — both entries put `source:`/`verified-at:`/`recheck:` at lines 3/4/5; mined ids match run output |
| c | "every cited S-id is a `## Registry` row of corpus/SOURCES.md with 11 cells, status `mined`, and `used-by` naming the entry" (v2) | `len(rows.get(i, [])) == 1 and (lambda r: len(r) == 11 and r[7] == "mined" and path in [u.strip() for u in r[10].split(",")])(rows[i][0])` (203–206) | MATCHES for mined ids — see F2 for "cited" scope. Schema verified: SOURCES.md:11 header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`; index 7 = status, index 10 = used-by; the 8 cited rows (lines 201/203/214–219) all parse to 11 cells, no escaped pipes, status `mined`, `used-by` contains the full target path(s) |
| d | "every cited S-id has a `GATE <id> receipt=<path> sha256=<hex> quote="<text>"` line under `## Gate` ... the receipt is committed at REV, its sha256 equals the declared digest, the quote has at most 25 words and occurs verbatim in the receipt bytes" (v2) | gate collection `GATE_RE` (line 30); pin filter `if pin and (rpath, digest) == pin ...` (217–219); blob check `hashlib.sha256(blob).hexdigest() == digest and len(quote.split()) <= 25 and quote.encode() in blob` (227–230) | MATCHES — replayed for all 10 GATE lines: `pin_match=True digest_ok=True in_blob=True`; all inside `## Gate` (lesson lines 18–79, next `##` at 80, zero GATE_RE matches outside) |
| e | "a `## Coverage map` table row of corpus/README.md names `knowledge/<basename>` in its first cell" (v2) | `map_cells` from `section(readme, "## Coverage map")` (167); `c["e"] = int(any(base_name in cell for cell in map_cells))` (247) | MATCHES — both entries present as first cells (README "## Coverage map") |
| f | "each of the entry's frozen surface tokens occurs in the entry and in at least one receipt its Gate lines bind" (v2) | `c["f"] = int(all(t in body and any(t.encode() in b for b in receipts) for t in tokens))` (248); `receipts` filled only from pin-matching, digest-verified gates (230) | MATCHES — both tokens present in each body and in bound receipt blobs |
| g | "the body carries one of that id's located Gate quotes verbatim and at least one `**OBS**` line naming the id" (v2) | `stated = stated or quote in body` (231); `any("**OBS**" in l and re.search(rf"\b{i}\b", l) for l in lines)` (232) | MATCHES — replayed: limits all stated=True; observ S189 q1=False/q2=True (any suffices); OBS lines present. Docstring's "next to" not enforced (F6) |
| h | "every cited S-id must name, in `## Gate` ... a `GATE` line whose (receipt path, sha256) equals the frozen pin for that id ... Only pin-matching Gate lines count for d, f and g" (v3) | `pin = PINS.get(i)`; `if pin and (rpath, digest) == pin and quote_floor_ok(...)` (217–219); `h_ok = h_ok and bool(good)` (225) | MATCHES — all 8 ids have pin-matching gates; fabricated/unpinned ids cannot bind (pin=None ⇒ empty) |
| i | "a Gate quote is not a bare surface token ... and is at least 3 words or at least 24 characters" (v3) | `quote_floor_ok` (149–153): `quote.strip() in tokens or re.fullmatch(r"S\d{3,}", quote.strip()) → False`; `len(quote.split()) >= 3 or len(quote) >= 24` | MATCHES — tests: `"e"`→False, `MAX_QUEUED_EVENTS`→False, `S189`→False, `"if (!m_logsEnabled)"`→False (19 chars/2 words), 24-char→True, 3 words→True. Effect visible: S217's first gate quote is floor-rejected; only `"bool m_logsEnabled = true;"` binds S217 |
| j | "every cited id has exactly one `## Registry` row" (v3) | `len(rows.get(i, [])) == 1` in c (203) and j (226) | MATCHES — each of the 8 ids has exactly one row-start match in the whole file (grep) and one parsed row |
| k | "`verified-at:` carries a YYYY-MM-DD date and `recheck:` carries an ISO date, an `NNd` count, or a `on-*` cadence (v2 accepted `x`)" (v3) | `DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")` (103); `RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$")` (104); first-token parse (208–211) | MATCHES — `2026-10-25` ✓, `90d` ✓, `on-change` ✓, `x` ✗, `2026-1-4` ✗, `on-` ✗. Leniences in F4 |
| l | "a normalized (id-free, case/*/` -insensitive) scan must find at least four of seven frozen claim phrases for the package entry, or two of three frozen mechanism phrases for the observability entry" (v3) | `hits = sum(1 for p in phrases if p in norm(body))` (250); `LINEAGE` (87–102); `norm` (146) | PARTIAL MISMATCH — see F1. Hits replayed: limits 6/7 (queue, cap, removed, writeoffset, eagain, 1024), observ 2/3 (null channel, core-logger); all hit contexts genuine content |
| precondition | "no corpus/knowledge/ file at BASE contains any frozen surface token" | `base_files`/`held` loop (168–175) | MATCHES — verified at `b4e47e98` (git grep rc=1) |
| target | "admitted == 2 -> TARGET_MET, exit 0" | verdict/return (257–259) | MATCHES |

## Hunt answers

1. **Clause-c short-circuit** — yes: `len(rows.get(i, [])) == 1` evaluates before the lambda (`and` short-circuit). Demos: missing id → `False` without KeyError; 10-cell row → `False` without IndexError. No error path.
2. **Rows outside `## Registry`** — excluded: `registry_rows` iterates `section(text, "## Registry")` only. Demo: a row under `## Paths` is not mined. But `section()` **breaks** at the first subsequent `##` (line ~127), so a *second* `## Registry` section later in the file is never scanned — v2's `section` rescanned every occurrence (demo: two-Registry text → v3 `{S189: 1}`, v2 `{S189: 2}`). At this rev SOURCES has exactly one Registry (lines 9→224); latent. A 4-space-indented duplicate row is invisible to `ROW_RE` (`^ {0,3}`) in both versions — markdown-correct (4-space = code block).
3. **r[7]/r[10] vs 11-column schema** — correct as above (header line 11; separator has 11 cells; all 8 rows parse to 11; no escaped pipes).
4. **head[:15] src_lines** — correct for the honest entries (lines 3–5). Gap: ids cited elsewhere in the body are not mined → see F2.
5. **`## Gate` parsing** — stops at the next `##` (lesson: `## Gate` at 18, `## Census after` at 80; all 10 GATE lines inside; 0 outside).
6. **DATE_RE/RECHECK_RE** — correct as above.
7. **PINS digests** — all equal `sha256sum` of the committed fetch receipts at b6c1d31 (quoted above), and equal the Gate-declared digests.

## Findings by severity

**[MEDIUM] F1 — `norm()` id-strip is a no-op (line 146)**
`return re.sub(r"[*`]", "", re.sub(r"\bS\d{3,}\b", " ", text.lower()))` — text is lowercased *before* the uppercase-`S` pattern runs, so `\bS\d{3,}\b` never matches; ids are never stripped. Demo: `norm("cite S1024 now") == 'cite s1024 now'` and `'1024' in norm('cite S1024 now')` → `True`. Contradicts the clause-l spec ("id-free") and the code comment ("ids and *` stripped"). Concrete crib vector: any body token `S1024` (a fabricated 4-digit id) satisfies the `"1024"` lineage phrase — cheaper than the declared "invented lineage phrases" residual. Honest run unaffected: no 4+digit ids in either entry; limits' seven `"1024"` occurrences are real buffer-size content (`std::array<char, 1024> buffer`, "cut to 1024 bytes", etc.).

**[MEDIUM] F2 — "every cited S-id" is implemented as head[:15] `source:`-mined ids only**
Per-id clauses c/d/g/h/j cover only ids mined from the first 15 lines' `source:` lines (line 197). Body citations escape all of them. Instances at b6c1d31:
- `event-delivery-limits-r26.md:80`: `the source ids (package S187 → S189, S188 → S201, S214 → S212, by document)` — cites S187/S188/S214;
- `event-queue-observability-r37.md:76`: `**INF** S201: Waybar never reconnects (backend.cpp:105,119-122), ...` — an evidentiary INF grounded on S201, whose receipt/pin binding is verified only for the *other* entry.
The honest pass depends on this narrow mining: S201's `used-by` does not name the observ entry and S214's does not name limits, so a whole-body reading of clause c would fail both honest entries. The v2/v3 spec sentences say "every cited S-id"; the implementation is more lenient. (Provenance and INF lines are legitimate content — the lenience is the issue, not the entries.)

**[LOW] F3 — `section()` breaks after the first `## <heading>`** (line ~127). Duplicate rows inserted under a *later* `## Registry` section escape uniqueness (v2 scanned all occurrences). Latent at this rev; weakens j-vs-v2. Same for a second `## Gate` in the lesson.

**[LOW] F4 — regex leniences**: `RECHECK_RE` accepts `0d` (`\d+d`); clause-k parses only the first whitespace token of each value (`v.split()[0]`), so `verified-at: 2026-10-25 garbage` passes. Consistent with the spec words ("carries a ... date"), but looser than a full-value parse.

**[INFO] F5 — BASE_DEFAULT `b4e47e98` is the round-36 tip, not the registration base `f6e3247` (round-37 tip)**. Inherited from v2 and required: both target entries landed in round 37, so clause a can only hold against the pre-round-37 base. The precondition is therefore evaluated at `b4e47e98` (verified unheld). Document, not a defect.

**[INFO] F6 — v3 docstring says OBS lines name each cited id "next to" its quote; code checks any OBS line naming the id + quote anywhere in the body** — matches the v2 spec sentence; the docstring wording is looser than the code.

**[INFO] F7 — post-freeze counter/manifest patches are already declared** (not a fresh finding). `LOG.md` (round-38 errata, commit `3f14bd2`, wave-1 `RevCommitChain` F1–F3): *"the C1 v3 counter was patched post-freeze (`859d0cf`, clause-c uniqueness) and the discrimination manifest was patched post-data (`b6c1d31`, `c1-duprow` in-table insert). At the frozen pair (`58e55ec`) the gate scores 18/19 — `c1-duprow` observed `TARGET_MET` — so the C1 claim as frozen fails its own instrument contract ... The landed pair measures 19/19 as a *new predicate*; a re-registration ruling is routed to the non-author closure."* I corroborate with tree evidence: `git diff 58e55ec 859d0cf -- quality/counters/c1-r38-event-ground.py` = exactly the clause-c uniqueness change (5 insertions/2 deletions, lines 202–206); `git log --oneline -- .ufo/waves/round-38/registration.md` = freeze commit only (registration not amended). My runs above measure the *landed* (new) predicate — 2/2 and 19/19 — matching the errata's framing.

**[ANOMALY] A1 — first gate invocation crashed `NameError: 'shutil'`** (transient; file was mid-edit by concurrent siblings during the session; worktree sha `c4bad89d…`→`581bf2ed…`; `import shutil` at line 31 in the settled file). Not reproducible; the settled gate passes 19/19. Recorded for audit completeness.

## Residual risk & verification gaps
- **Declared residual confirmed operational**: fully fabricated self-consistent artifacts still pass (a receipt whose bytes match the pin digest and contain the quote; invented lineage phrases; invented pin-matching gate lines). The v3 repairs raise the crib's cost from trivial to fabrication; nothing in the code proves live truth from committed bytes. F1/F2 give two cheaper-than-declared vectors (one-token id-phrase; body-only citations).
- **Not re-run**: the frozen-pair 18/19 gate score — accepted from the recorded errata (recorded observations are ground truth).
- **Not verified**: whether any *other* knowledge entry at rev contains `S1024`-class ids that would exercise F1 (corpus-wide id scan shows none — `git grep -E "S10(2[4-9]|...)" b6c1d31 -- corpus/knowledge` → none).
- **Gaps**: multi-Registry duplicate rows (F3), 4-space-indented rows, and body-cited ids (F2) are untested by the manifest controls; the `c1-duprow` control inserts *inside* the single Registry section, so it cannot expose F3.
