# R54W2Seat24 — C2 source-range parsing: does `source: S375–S377` cite literal S376 under a reproducible parser?

**Verdict: NO — falsified under the lane's reproducible parser.** The house extractor
(`quality/counters/c2-r51-dispatch-entry.py`, `clause_b`) reduces the en-dash range
`S375–S377` to `['S375', 'S377']`; literal `S376` is never extracted, although all three
rows sit inside the parser's own row window (364–379). The pinned C2 counter is absent,
so the frozen command itself is **NOT RUN / absent**. One behavior-bearing mutation probe
(the citation token) flips the detector RED→GREEN→RED with hash-equal restoration.

Axes: (1) predicate satisfiability of PRED-C2-r54 clause (a) on the frozen citation form,
(2) detector coverage of the C2-CTL control set for the citation leg, (3) record
integrity (no lane/predicate edits; scratch-only mutation).

## 1. Availability — pinned command NOT RUN / absent

Frozen command (`claims-frozen.md:55`, `registration.md:89`):

```sh
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a
python3: can't open file '/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r54-uwsm-entry.py': [Errno 2] No such file or directory
exit=2
```

- `ls quality/counters | grep -c r54` → `0` (exit 1); `test -e quality/counters/c2-r54-uwsm-entry.py` → ABSENT.
- Entry `corpus/knowledge/uwsm-app-environment-r54.md`: `test -e` → exit 1 (absent now);
  `git status --porcelain | grep -c uwsm` → `0`. The w1-observed working-tree bytes are gone;
  the citation line survives only as w1-recorded transcription (see §3).
- Lane HEAD observed: `350d30e4ec5531f65ce99a57efeb8216f38e678a` (`round-54: freeze claims,
  registration, source pins and wave one dispatch`), which differs from the assigned base
  `e25149fe…` by the freeze commit itself. No git/jj mutation performed by this seat.
- Working-tree `corpus/SOURCES.md:325-327` does carry rows S375–S377 (uncommitted, w1-landed),
  so the citation targets exist; the citing entry does not.

## 2. Frozen contract lines attacked

- `claims-frozen.md:55-60` — PRED-C2-r54: exits 0 only if "(a) … opens with the provenance
  trio (`source:`, `verified-at:`, `recheck:`) **citing rows S375, S376 and S377** of
  `corpus/SOURCES.md`".
- `claims-frozen.md:82-84` — C2 read-set includes "rows S375–S377 of `corpus/SOURCES.md`"
  (range written with the same en dash).
- `registration.md:72` — the trio line is frozen as "`source:` citing **S375–S377**" (en dash,
  U+2013): the range form is the contract's own citation shape, not a scribe accident.
- `registration.md:61-65` — exact pin spans: S375 `uwsm-0.27.1-README.md:117-118`;
  S376 `uwsm-0.27.1-uwsm-app.1.scd:60`; S377 `uwsm-0.27.1-main.py:3714`.
- `registration.md:78-87` — six frozen C2 controls; C2-CTL-2 ("entry `source:` cites S999 →
  registry leg fails") presumes the counter parses row ids **off the `source:` line**.

The claimed invariant: the range citation resolves to {S375, S376, S377}. The plausible
defect: the only reproducible parser in the lane tokenizes `S<digits>` ids and has no
range expansion, so the middle row is silently dropped from the citation leg.

## 3. Reproducible parser and fixture

Parser (pristine lane bytes, never modified): `quality/counters/c2-r51-dispatch-entry.py`,
sha256 `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`.
- `:64` `ROW_MIN, ROW_MAX = 364, 379` (S375/S376/S377 all in-window).
- `:77` `SRC_RE = re.compile(r"^\s*source\s*(?:\([^)]*\))?\s*:\s*(.+)$", re.I)`.
- `clause_b` (read at `:383-390`): `for k in re.findall(r"\bS(\d{3,})\b", m.group(1))` —
  endpoints-only id extraction, no range expansion (same site R54Seat32 §S5 names, line 386).

Fixture (rule-compliant): `D=$(mktemp -d /fast/scratch/hyaku/mado-r54/R54W2Seat24/fix-XXXXXXXX)`
→ `/fast/scratch/hyaku/mado-r54/R54W2Seat24/fix-dXLK6fpn`. No git commands, no commits
(detector drives the parser module directly; nothing to verify a toplevel for).
Entry fixture bytes are the w1-recorded transcription of the landed provenance line
(R54Seat07:267 for the text; R54Seat08:287-290 `cat -A` for the en-dash bytes
`S375M-bM-^@M-^SS377`); the tail after `0727985c` is elided in the w1 record and is
extraction-irrelevant (SRC_RE captures the whole line; only S-tokens are read):

```text
$ cat -A entry-pristine.md
source: S375M-bM-^@M-^SS377 M-bM-^@M-^T uwsm v0.27.1 README, uwsm-app manual, and app-daemon source at commit 0727985c$
```

Detector (`det.py`, scratch): imports the parser module (has `if __name__` guard at `:665`),
matches `mod.SRC_RE`, extracts the findall pattern **from the module's own `clause_b`
source via `inspect.getsource`** (no hand-copied regex), applies the module's
`ROW_MIN/ROW_MAX` window and dedup — exactly `clause_b`'s extraction semantics.
Question asked: is `S376` cited, and is `{S375,S376,S377} ⊆ extracted`?

## 4. Mutation probe — runs, outputs, hashes

Mutant = smallest behavior-bearing point for the claim: the citation token itself,
`S375–S377` → `S375, S376, S377`, in the scratch copy only.

```text
parser-before  ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd
entryP-before  184659acea898b4e3e5b440e51e88e9b12a9927f80974a5b57ca2ee40da37317
R1-pristine:  CITE_PROBE: pattern=\bS(\d{3,})\b extracted=['S375', 'S377'] S376_cited=False trio_cited=False
R1-exit=0
R2-mutant:    CITE_PROBE: pattern=\bS(\d{3,})\b extracted=['S375', 'S376', 'S377'] S376_cited=True trio_cited=True
R2-exit=0
R3-restored:  CITE_PROBE: pattern=\bS(\d{3,})\b extracted=['S375', 'S377'] S376_cited=False trio_cited=False
R3-exit=0
parser-after  ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd
entryP-after  184659acea898b4e3e5b440e51e88e9b12a9927f80974a5b57ca2ee40da37317
```

- **Expected detector**: clause-(a) citation leg semantics under the house parser
  (SRC_RE match → `\bS(\d{3,})\b` → row-window filter).
- **Output**: R1 RED (S376 not cited, trio not covered), R2 GREEN, R3 RED.
- **Verdict**: baseline failure on pristine bytes → per mutation protocol this is
  **inconclusive as a kill/survive test**, and it is a positive falsification of the item:
  under the reproducible parser, `source: S375–S377` does **not** cite literal S376.
  R2 shows the detector is behavior-sensitive to exactly that token (no vacuous pass);
  R3 + hash equality shows determinism and exact restoration. The drop occurs at
  tokenization, before the window test — `ROW_MIN ≤ 375,376,377 ≤ ROW_MAX` would have
  admitted all three.

## 5. Consequence for the frozen predicate (coverage finding, no edits made)

1. If the w2 C2 counter parses row ids off the `source:` line (the design C2-CTL-2
   presumes), the frozen citation form yields `rows cited = 2` → clause (a) fails on the
   honest entry — a false TARGET_MISSED baked into the landing form that `registration.md:72`
   itself freezes.
2. If instead the counter hardcodes the trio {S375, S376, S377} from the frozen table and
   never parses the line, clause (a)'s citation check is vacuous and C2-CTL-2 cannot fail
   via the citation leg — a non-discriminating control.
Either branch is a freeze-completeness defect: the contract freezes the range form
(`registration.md:72`, `claims-frozen.md:84`) but no expansion rule, and the only
reproducible parser precedent does not expand ranges.

Smallest safe correction (pre-data; belongs in a landing-form fix or a v2 re-registration,
not an edit to frozen files — none made here): enumerate `source: S375, S376, S377 — …`
(R2 shows clause (a) then holds under the unchanged house parser), or freeze an explicit
range-expansion rule plus an en-dash selftest case for the counter.

## 6. W1 linkage

My w1 report `w1/R54Seat24.md` attacked the C1 counter (INCONCLUSIVE, counter absent) — a
different item. W1 seats that recorded this range-tokenization ground without executing the
house parser: R54Seat08 T-F (:287-290), R54Seat09 F7 (:172), R54Seat14 F4 (:65-66),
R54Seat27 (:208-211, D7 at :139), R54Seat29 B29-7 (:307-308), R54Seat30 (:388-397),
R54Seat32 S5 (:379-387). This probe re-derives the finding by executing the parser's own
code objects; no predicate, control, registration, lane or source file was changed.

## Trailer

Exact commands / outputs / exits (lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`):

- `git rev-parse HEAD` → `350d30e4ec5531f65ce99a57efeb8216f38e678a`, exit 0 (≠ base; freeze commit; observed only).
- `ls quality/counters | grep -c r54` → `0`, exit 1.
- `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev 350d30e4…` → `[Errno 2] No such file or directory`, exit 2 — **NOT RUN / absent**.
- `test -e corpus/knowledge/uwsm-app-environment-r54.md` → exit 1 (absent); `git status --porcelain | grep -c uwsm` → `0`, exit 1.
- `sha256sum quality/counters/c2-r51-dispatch-entry.py` → `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`, exit 0 (before == after probe).
- Probe runs R1/R2/R3 with outputs and exits as in §4; fixture `…/R54W2Seat24/fix-dXLK6fpn`, no git commands, no commits.
- Attacked finding: range citation `S375–S377` does not cite literal S376 under the reproducible parser (clause (a) leg falsified; control-set consequence §5).
- Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat24` created explicitly, then `rm -rf`;
  `ls /fast/scratch/hyaku/mado-r54/ | grep -c R54W2Seat24` → `0` (exit 1); `test -e` → exit 1 — none remaining.
- Disk: `df -h /fast` → 579G available; no ENOSPC; no failed disk checks retried.
- Tooling installed/updated: none. Lane edits: this report only. No subagents, no background producers, no host/config/compositor reads or writes.
