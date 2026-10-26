# RevC2Counter — C2 counter delta review (round 45 w1) — COMPLETE

Verdict: **no admission-granting defect, no always-failing check**. The r45 delta is faithful to its
docstring; two LOW hardening notes on the clause-h prose net, three INFO notes.

Scope: every changed line of `quality/counters/c2-r45-monitor-entry.py` (blob `61bd4bee…`, verified
frozen-identical) vs parent `quality/counters/c2-r44-gkeep-size-request-v2.py`. Full findings with repros and
computed locators: `.ufo/waves/round-45/w1/RevC2Counter/review.md`.

## Findings
- **F1 LOW** — h prose check `:589` rstrip set `.,;:)` + backtick misses `" ] } * '`; decorated-but-true
  values (`**scale_search=89**,`, `[default_refresh=60](#x)`, `"line_keys=8".`, `scale_search=[89]`) are read
  as contradictions → honest entry rejected. Fail-closed; control P uses plain forms and passes.
- **F2 LOW** — h prose check `:588` new leading `\b` (absent in parent): `x_scale_search=0` evades the
  contradiction net (word-char prefix kills the boundary); `rule-scale_search=0` is still caught. Fail-open
  for that net only; admission unaffected (exact census line still required exactly once).
- **F3 INFO** — clause e scope equality (:550, idx 4 = scope per `corpus/SOURCES.md:11` header — index right;
  cell edges stripped) is free-prose exact-string: any internal rewording counts as "different scope". Bounded
  in effect to pin URLs (new ids forced to pin URLs by clause d + T2), i.e. exactly the disclosed W04 shape;
  fail-closed only.
- **F4 INFO** — census `line_keys=8` counts the late extension keys of the pinned legacy handleMonitor
  (mirror/bitdepth/cm/sdrbrightness/sdrsaturation/transform/vrr/icc, legacy:1293-1387), not the grammar keys —
  the pinned handler delegates to `CMonitorRuleParser` at legacy:1297. Docstring defines it operationally; the
  entry prose must not call it "the eight syntax keys".
- **F5 INFO** — inherited nits, not regressions: `import json` unused (also in parent), `host_census`
  unused params, dead `loc_ok` (:603), mode 100755 both.

## Verified clean (independent, against the frozen pins)
9/9 pins byte-match PINS and the freeze blobs; 17/17 SURFACES anchors exactly-once (Parser 110/145/193,
legacy 1293/1378, MRM 38/96, hpp 46, Monitor 1201/837/1001, HyprCtl 242/320, MPC 27, String 50, wiki 11/253);
census regexes exactly-once each (60/1/120/5), scale-search loop N=90 is the first such loop after the
searchScale line (Monitor.cpp:1001→+9), handleMonitor body 1293-1387 ends at a true `}` with 0 leaking
`ARGS[argno] == "` after it, nkeys=8; computed census line byte-equals the registration's frozen census line;
census exemption only for the byte-exact line; clause j width bound = docstring (JWIDTH 30, :404); clause i
simplification leaves no dangling ADMIT/REFUSE refs; docstring vs code consistent clause-by-clause; in-vivo
run at the freeze rev → `admitted=0/1 verdict=TARGET_MISSED`, exit 1; controls receipt ctl-c2.txt consistent
with the code (P a:1…j:1; each rejection fails the clause its name attacks).

## Notes
- No lane writes outside the seat dir (`w1/RevC2Counter/` + this Report); counters/registration/pins untouched;
  git usage read-only (`ls-tree`, `hash-object` without `-w`, `status`, `show`).
- Tooling: system python3 and git only; nothing installed (no pacman, no uv/pip/npx); scratch
  /fast/scratch/hyaku/mado-r45/RevC2Counter held no artifacts and was removed.
