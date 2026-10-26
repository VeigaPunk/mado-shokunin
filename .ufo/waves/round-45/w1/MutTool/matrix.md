# MutTool matrix — round 45 w1 (mado C1 reference tool)

Seat MutTool, 2026-10-26. Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py` (selftest 33/33). Mutants are single string edits applied to a scratch copy (`gen-*`/`mut-*` under /fast/scratch/hyaku/mado-r45/MutTool/mut/); the frozen reference was never written (sha256 before == after, below).


## Harness and baseline

- Detector A: `python3 -I <mutant> --selftest` (the tool's own 33-case selftest + 3 setup cases).
- Detector B: frozen counter `quality/counters/c1-r45-monitors.py --repo <clone> --rev HEAD --work /fast/scratch/hyaku/mado-r45/MutTool/w` (default seed 45; clause s re-runs the mutant's selftest, clause f runs the 49 seeded fixtures, clause r the PATH marker).
- Clone: `git clone -q --shared --no-checkout` of the lane, `checkout --detach 22a8dedd02f507689c567777e0f20b5e645c8ce0`, one commit per mutant (`git rev-parse --show-toplevel` asserted = clone before every commit).
- Baseline control (pristine reference committed, before any mutant): `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET` exit 0 — `receipts/ref-baseline.log`; agrees with frozen `receipts/ctl-c1.txt` REF row.
- 54 mutants attempted, 0 design errors (every old-string matched exactly once). Runtime ~30 s total.


## Summary

| Verdict | n | meaning |
|---|---|---|
| KILLED_SELFTEST | 18 | detector A fails; counter not run |
| KILLED_FIXTURES (fixtures only) | 14 | selftest 33/33 ok, counter TARGET_MISSED — missing selftest assertion |
| SURVIVED (killed by neither) | 22 | 19 coverage gaps with demonstrated input; 2 dead mutants; 1 equivalent-by-tolerance |

## Matrix A — all 54 mutants

| id | area | line | selftest | counter | verdict |
|---|---|---|---|---|---|
| mode-default-rate-59 | parse_mode | 202 | 33/33 ok | fixtures=47/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=17c58ea1872fa8401f92398385be968152dd8302 seed=45 | KILLED_FIXTURES |
| mode-pref-ci | parse_mode | 187 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=1e34928b64f1b55b1edae40613f3457f17064298 seed=45 | SURVIVED |
| mode-modeline-case | parse_mode | 193 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=95d93b483b86e5aacaee2f0de1fb6d0b2837f40a seed=45 | SURVIVED |
| mode-kw-drop-highres | parse_mode | 189 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=4aa9030e080470a76f97431f174448914dd865ed seed=45 | KILLED_FIXTURES |
| mode-kw-ci | parse_mode | 190 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=107a7ee07f54ba844351b7d72ed4f73c8b23f3f9 seed=45 | SURVIVED |
| mode-wh-swap | parse_mode | 201 | fail | not run | KILLED_SELFTEST |
| mode-explicit-label | parse_mode | 200 | fail | not run | KILLED_SELFTEST |
| pos-swap | parse_pos | 211 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=a5e1d26a08965ae68e880e50bf973453064b74f6 seed=45 | KILLED_FIXTURES |
| pos-auto-eq | parse_pos | 206 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=866e9962eb9cc1d29dede658bc6ee3cd99dcb9b5 seed=45 | KILLED_FIXTURES |
| pos-re-no-minus | POS_RE | 102 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=5a4ad09018eebb4fcf9b1e57684b12cfe898a79c seed=45 | KILLED_FIXTURES |
| scale-bound-02 | parse_scale | 220 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=00fa9e6083becb48688c228a1d8db74607f3ce7c seed=45 | KILLED_FIXTURES |
| scale-bound-le | parse_scale | 220 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=6ffe19f194cb6058a5549b8c4e358b0a95690b61 seed=45 | SURVIVED |
| scale-no-f32 | parse_scale | 219 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=303472abc96fce9cb910a7df3ff8719441a3c406 seed=45 | SURVIVED |
| transform-drop-7 | transform_value | 224 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=fc4aea41be73919db29e3cb30eb81908955a297c seed=45 | SURVIVED |
| add-no-erase | add | 181 | fail | not run | KILLED_SELFTEST |
| add-prepend | add | 182 | fail | not run | KILLED_SELFTEST |
| eff-first-wins | effective | 347 | fail | not run | KILLED_SELFTEST |
| eff-desc-substr | effective | 352 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=aef0c5141f8c1425ada9c64834216de84d673973 seed=45 | KILLED_FIXTURES |
| eff-desc-nostrip | effective | 352 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=ce50d48215dcfa2efcb178edd60733d65a76e3c9 seed=45 | SURVIVED |
| eff-empty-last | effective | 356 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=209e3f52bde0d51d3d887a9c264d524a3a1bdcbb seed=45 | SURVIVED |
| eff-no-empty-fallback | effective | 357 | fail | not run | KILLED_SELFTEST |
| cmp-rate-tol-05 | compare | 373 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=aef26a2274b4fd6931c68631b99a5084e5ada912 seed=45 | SURVIVED |
| cmp-rate-tol-le | compare | 373 | fail | not run | KILLED_SELFTEST |
| cmp-scale-tol | compare | 385 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=8f25bfb66dc43c3212738ccedfc93166ade75bca seed=45 | SURVIVED |
| es-no-correction | expected_scale | 330 | fail | not run | KILLED_SELFTEST |
| es-range-44 | expected_scale | 334 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=d55814b22981426cba20e69f73715645ff3f8b59 seed=45 | SURVIVED |
| es-floor-not-round | expected_scale | 330 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=eab101b676e73b884a056c2df1017d4d3ac20683 seed=45 | SURVIVED |
| es-up-only | expected_scale | 335 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=803bcc8f0b1752b222b3799b83374ad43c5d43ab seed=45 | SURVIVED |
| cmp-transform-no-int | compare | 388 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=f85f5e23c23c0748d7174a94999d0b05fd47b736 seed=45 | SURVIVED |
| cmp-mirror-by-name | compare | 393 | fail | not run | KILLED_SELFTEST |
| cmp-mirror-none-any | compare | 395 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=1867ae4fd5035c1402cd8ffd9b9c210ca0ba9ba7 seed=45 | SURVIVED |
| cmp-pos-type-only | compare | 377 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=0988062dba0f621c18293c3a4e82efc5645f8725 seed=45 | SURVIVED |
| vrd-order-swap | verdict order | 436 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=464985fdcee873190dd1f08af6bc61ebf5f88244 seed=45 | SURVIVED |
| vrd-and-or | verdict order | 432 | fail | not run | KILLED_SELFTEST |
| vrc-differ-2 | verdict order | 437 | fail | not run | KILLED_SELFTEST |
| vrd-notcompared-4 | verdict order | 435 | fail | not run | KILLED_SELFTEST |
| fmt-rule-rate-1dp | output formats | 403 | 33/33 ok | fixtures=15/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=3f0bcfea5710396a520fc5caf41eefe8cc79c9f4 seed=45 | KILLED_FIXTURES |
| fmt-scale-2dp | output formats | 405 | 33/33 ok | fixtures=15/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=85125d3f18d84b5eadee70fb0a3dfcdf08b46eb5 seed=45 | KILLED_FIXTURES |
| fmt-mirror-no-dash | output formats | 408 | 33/33 ok | fixtures=11/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=5cc425461fbbed41974a353c4547199353138168 seed=45 | KILLED_FIXTURES |
| fmt-out-label | output formats | 429 | fail | not run | KILLED_SELFTEST |
| fmt-sum-label | output formats | 442 | 33/33 ok | fixtures=4/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=78dab0c0bdaa7480dfaab5a848da388da4b86200 seed=45 | KILLED_FIXTURES |
| pl-keep-dollar | parse_line | 230 | fail | not run | KILLED_SELFTEST |
| pl-keep-backslash | parse_line | 230 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=a747487e02c645d195cf4e4f570cfadb327d8a6a seed=45 | SURVIVED |
| pl-rsplit | parse_line | 233 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=5af041c1fa825dfa736166cc23d8018f7ea8cabe seed=45 | SURVIVED |
| keys-drop-bitdepth | parse_line keys | 105 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=4e69d9698665c02d2638177acfd82f7766d93cfe seed=45 | KILLED_FIXTURES |
| keys-add-sdr-eotf | parse_line keys | 105 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=e884cf7944b74e36f8002142aa2878357ae044da seed=45 | KILLED_FIXTURES |
| badkey-break | parse_line | 274 | fail | not run | KILLED_SELFTEST |
| disable-single | parse_line | 241 | 33/33 ok | fixtures=48/49 selftest=ok readonly=ok tool=present TARGET_MISSED rev=69184fba785d3d9a9720ec9a1da8266aa8407a6e seed=45 | KILLED_FIXTURES |
| pc-strip-all | parse_config | 294 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=25c62e33e243c5ab56b702a414d83b77380f64b0 seed=45 | SURVIVED |
| v2-re-loose | V2_RE | 100 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=c52c72d137c04c6c3e93cb691cd8d3617c3a9e4d seed=45 | SURVIVED |
| max-bytes-x10 | read_regular | 98 | 33/33 ok | fixtures=49/49 selftest=ok readonly=ok tool=present TARGET_MET rev=c239a5e4ffc5e6ae96543444def9d1207237840d seed=45 | SURVIVED |
| new-default-transform-1 | new_rule | 177 | fail | not run | KILLED_SELFTEST |
| disabled-verdict-swap | compare | 365 | fail | not run | KILLED_SELFTEST |
| pl-fields-nostrip | parse_line | 234 | fail | not run | KILLED_SELFTEST |

Line = first line of the edited statement in the reference (computed by the driver, `text[:index].count(chr(10)) + 1`). Per-mutant full counter output: `receipts/mut-<id>.log`.


## Matrix B — killed by NEITHER (survivors): missing fixtures

Each entry: the contract sentence attacked, a demonstrated input, the reference output (= contract-expected) and the mutant output. Evidence: `receipts/demo-evidence.json` (both stdout captures, generated this session).

### mode-pref-ci (parse_mode, line 187)

- Edit: `if value == "" or value.startswith("pref"):
        return` -> `if value == "" or low.startswith("pref"):
        return`
- Contract attacked: MODE: "" or starting `pref` is preferred
- Missing fixture input: config `monitor = DP-1, PREF, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### mode-modeline-case (parse_mode, line 193)

- Edit: `toks = low.split()
    if toks and toks[0] == "modeline":` -> `toks = value.split()
    if toks and toks[0] == "modeline":`
- Contract attacked: a first token `modeline` (any case) is modeline
- Missing fixture input: config `monitor = DP-1, MODELINE 1920x, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=modeline pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```

### mode-kw-ci (parse_mode, line 190)

- Edit: `if value.startswith(kw):` -> `if low.startswith(kw):`
- Contract attacked: starting `highrr`, `highres`, `maxwidth` is that keyword (exact-case token)
- Missing fixture input: config `monitor = DP-1, HIGHRES, auto, auto\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=highres pos=auto scale=auto transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### scale-bound-le (parse_scale, line 220)

- Edit: `rule["scale"] = 1.0 if s < 0.25 else s` -> `rule["scale"] = 1.0 if s <= 0.25 else s`
- Contract attacked: S < 0.25 becomes 1.0 (boundary S = 0.25 stays S)
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 0.25\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 0.25, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=0.2500 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=scale verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```

### scale-no-f32 (parse_scale, line 219)

- Edit: `s = f32(float(value))` -> `s = float(value)`
- Contract attacked: else `[0-9]{1,2}(\.[0-9]{1,6})?` gives S (a 32-bit float ...)
- Class: **equivalent-by-tolerance (clause unobservable through tool I/O)**.
- Class rationale: the 32-bit-float clause differs from float64 by <=6e-8 relative, while the tool only prints scale with 4 decimals and compares with |scale-E| < 0.0001; rate uses < 1.0. The clause cannot change any output byte for any accepted input.
- Evidence: 27/27 input pairs (S x live-scale grid incl. 1.3-vs-4/3 correction, 1.6, 0.3, 2.25) byte-identical between reference and mutant.
- Not a fixture ask: contract observation — the float32 clause is unobservable through the tool's declared output; only a contract re-wording (or a printed-precision change) can make it testable.

### transform-drop-7 (transform_value, line 224)

- Edit: `if len(value) == 1 and value in "01234567":` -> `if len(value) == 1 and value in "0123456":`
- Contract attacked: field 2 must be one digit 0-7 / `transform` VALUE must be one digit 0-7
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1, transform, 7\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 7, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=7 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```

### eff-desc-nostrip (effective, line 352)

- Edit: `if desc.startswith(sel[5:].strip(" \t")):` -> `if desc.startswith(sel[5:]):`
- Contract attacked: description starts with TEXT stripped of spaces and tabs
- Missing fixture input: config `monitor = desc: DP-1 , 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "DP-1 34in", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="desc: DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=3:
```
MADO_MON_RULE: n=1 sel="desc: DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR
```

### eff-empty-last (effective, line 356)

- Edit: `for n, r in enumerate(rules, 1):
        if r["sel"] == "":
            return n` -> `for n, r in reversed(list(enumerate(rules, 1))):
        if r["sel"] == "":
            return n`
- Contract attacked: else the first rule with an empty selector
- Class: **dead mutant (unreachable state)**.
- Deadness: `add()` erases every earlier rule with the same selector, so at most one empty-selector rule can ever exist; "the first rule whose selector is empty" is always the only one. Demo (two empty-selector rules — the second erases the first): ref and mutant byte-identical, rc=1.
- Input tried: cfg `monitor = , 3440x1440@100, 0x0, 1\nmonitor = , 1920x1080@60, 0x0, 1\n`
- No fixture can distinguish: state unreachable. Not a coverage ask; recorded as a contract note (the word "first" is untestable given add() semantics).

### cmp-rate-tol-05 (compare, line 373)

- Edit: `and abs(rr - rule["rate"]) < 1.0):` -> `and abs(rr - rule["rate"]) < 0.5):`
- Contract attacked: |`refreshRate` - RATE| < 1.0 (Hyprland's own closeness test ...)
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.5, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mode verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```

### cmp-scale-tol (compare, line 385)

- Edit: `if e is not None and abs(sc - e) >= 0.0001:` -> `if e is not None and abs(sc - e) >= 0.001:`
- Contract attacked: Agree when |`scale` - E| < 0.0001
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1.0005, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=scale verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### es-range-44 (expected_scale, line 334)

- Edit: `for i in range(1, 90):` -> `for i in range(1, 45):`
- Contract attacked: searching 89 steps up and down
- Missing fixture input: config `monitor = DP-1, preferred, auto, 1.45\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3441, "height": 1441, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1.25, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=1.4500 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=scale verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=1.4500 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### es-floor-not-round (expected_scale, line 330)

- Edit: `k = math.floor(s * 120.0 + 0.5)` -> `k = math.floor(s * 120.0)`
- Contract attacked: with K = round-half-up(S*120)
- Missing fixture input: config `monitor = DP-1, preferred, auto, 0.837501\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 85, "height": 85, "refreshRate": 60.0, "x": 0, "y": 0, "scale": 0.85, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=0.8375 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=0.8375 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=scale verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```

### es-up-only (expected_scale, line 335)

- Edit: `for cand in ((k + i) / 120.0, (k - i) / 120.0):` -> `for cand in ((k + i) / 120.0,):`
- Contract attacked: the first of (K+i)/120, (K-i)/120 for i = 1..89 that divides both
- Missing fixture input: config `monitor = DP-1, preferred, auto, 1.45\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1.33333333, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=1.4500 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=preferred pos=auto scale=1.4500 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=scale verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```

### cmp-transform-no-int (compare, line 388)

- Edit: `if not (is_int(t) and t == rule["transform"]):
        bad.append("transform")` -> `if not (t == rule["transform"]):
        bad.append("transform")`
- Contract attacked: a live value ... of the wrong JSON type (integers for ... transform ...) fails its field
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": false, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=transform verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### cmp-mirror-none-any (compare, line 395)

- Edit: `elif mo != "none":
        bad.append("mirror")` -> `elif mo == "":
        bad.append("mirror")`
- Contract attacked: without one: `mirrorOf` == "none"
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "DP-9"}]`
- Reference (contract-expected), rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=mirror verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### cmp-pos-type-only (compare, line 377)

- Edit: `if not (is_int(x) and is_int(y) and (x, y) == rule["pos"]):` -> `if not ((x, y) == rule["pos"]):`
- Contract attacked: integers for width, height, x, y, transform, id
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 1x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": true, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=1:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=1x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=position verdict=DIFFER
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=1x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### vrd-order-swap (verdict order, line 436)

- Edit: `elif t["differ"] > 0:
        v, rc = "DIFFER", 1
    elif t["matched"] == 0:
        v, rc = "NO_MATCHING_MONITOR", 3` -> `elif t["matched"] == 0:
        v, rc = "NO_MATCHING_MONITOR", 3
    elif t["differ"] > 0:
        v, rc = "DIFFER", 1`
- Contract attacked: DIFFER (exit 1, differ > 0) | NO_MATCHING_MONITOR (exit 3, matched = 0) | OK ..., tested in that order
- Class: **dead mutant (unreachable state)**.
- Deadness: `t["differ"]` is incremented only inside the matched branch (the same branch as `t["matched"] += 1`), so `differ > 0` implies `matched > 0`; the DIFFER-before-NO_MATCHING_MONITOR precedence can never decide a case. Demo: identical outputs (ref rc=1 = mut rc=1).
- Not a coverage ask; the contract's tested-in-that-order list is partially unobservable.

### pl-keep-backslash (parse_line, line 230)

- Edit: `if "##" in body or "$" in body or "\\" in body:` -> `if "##" in body or "$" in body:`
- Contract attacked: if it contains `##`, `$` or a backslash the line adds one to `unsupported` and is not modelled
- Missing fixture input: config `monitor = DP-1\, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```
- Mutant output, rc=3:
```
MADO_MON_RULE: n=1 sel="DP-1\\" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NO_MATCHING_MONITOR
```

### pl-rsplit (parse_line, line 233)

- Edit: `body = body.split("#", 1)[0]` -> `body = body.rsplit("#", 1)[0]`
- Contract attacked: else it is cut at its first `#`
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1 # one # two\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```

### pc-strip-all (parse_config, line 294)

- Edit: `line = raw.strip(" \t")` -> `line = raw.strip()`
- Contract attacked: a line is stripped of spaces and tabs at both ends
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=5:
```
MADO_MON_OUTPUT: name="DP-1" rule=- differ=- verdict=UNRULED
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 outputs=1 matched=0 unruled=1 agree=0 differ=0 disabled=0 verdict=NOT_COMPARED
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

### v2-re-loose (V2_RE, line 100)

- Edit: `V2_RE = re.compile(r"monitorv2(?:[ \t={]|$)")` -> `V2_RE = re.compile(r"monitorv2")`
- Contract attacked: A line whose first token (up to a space, tab, `=` or `{`) is `monitorv2` adds one to `v2`
- Missing fixture input: config `monitorv2extra = 1\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]`
- Reference (contract-expected), rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```
- Mutant output, rc=5:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=1 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=NOT_COMPARED
```

### max-bytes-x10 (read_regular, line 98)

- Edit: `MAX_BYTES = 1048576` -> `MAX_BYTES = 10485760`
- Contract attacked: an input larger than 1048576 bytes is too_large
- Missing fixture input: config `monitor = DP-1, 3440x1440@100, 0x0, 1\n`; dump `[{"id": 0, "name": "DP-1", "description": "", "width": 3440, "height": 1440, "refreshRate": 99.997, "x": 0, "y": 0, "scale": 1, "transform": 0, "disabled": false, "mirrorOf": "none"}]                  ...(1048577 bytes)`
- Reference (contract-expected), rc=2:
```
MADO_MONITORS: SETUP too_large
```
- Mutant output, rc=0:
```
MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK
```

## Matrix C — killed by FIXTURES ONLY: missing selftest assertions

### mode-default-rate-59 (parse_mode, line 202)

- Edit: `rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 60.0` -> `rule["rate"] = f32(float(m.group(4))) if m.group(4) is not None else 59.94`
- Contract attacked: a rule without @RATE requests 60 Hz (MonitorRule.hpp m_refreshRate = 60)
- Counter: fixtures=47/49 — killed by fixture(s): no-rate-requests-60, no-rate-live-59.99
- Missing selftest assertion: selftest asserts no RULE-line text; add assertion rule line "mode=3440x1440@60.00" for the no-rate case (selftest checks only OUTPUT suffixes + final verdict).

### mode-kw-drop-highres (parse_mode, line 189)

- Edit: `for kw in ("highrr", "highres", "maxwidth"):` -> `for kw in ("highrr", "maxwidth"):`
- Contract attacked: starting `highrr`, `highres`, `maxwidth` is that keyword
- Counter: fixtures=48/49 — killed by fixture(s): highres-not-compared
- Missing selftest assertion: no selftest case uses keyword mode `highres`; add case ("highres", "monitor = DP-1, highres, auto, auto", [mon DP-1], OK, 0).

### pos-swap (parse_pos, line 211)

- Edit: `rule["pos"] = (int(m.group(1)), int(m.group(2)))` -> `rule["pos"] = (int(m.group(2)), int(m.group(1)))`
- Contract attacked: POSITION: else (-?[0-9]{1,6})x(-?[0-9]{1,6}) gives X, Y
- Counter: fixtures=48/49 — killed by fixture(s): position
- Missing selftest assertion: selftest "pos" uses 10x0 vs live (0,0): swap gives (0,10) which also differs; missing a nonzero-Y case (e.g. rule 0x50 vs live (0,0)) or a rule-line assertion "pos=10x0".

### pos-auto-eq (parse_pos, line 206)

- Edit: `if value == "" or value.startswith("auto"):
        return
    m = POS_RE.fullmatch(value)` -> `if value == "" or value == "auto":
        return
    m = POS_RE.fullmatch(value)`
- Contract attacked: POSITION: "" or starting `auto` is auto
- Counter: fixtures=48/49 — killed by fixture(s): auto-position
- Missing selftest assertion: selftest "auto-pos" uses bare "auto"; missing an auto-WORD variant (auto-left) which must stay position-auto.

### pos-re-no-minus (POS_RE, line 102)

- Edit: `POS_RE = re.compile(r"(-?[0-9]{1,6})x(-?[0-9]{1,6})")` -> `POS_RE = re.compile(r"([0-9]{1,6})x(-?[0-9]{1,6})")`
- Contract attacked: POSITION: else `(-?[0-9]{1,6})x(-?[0-9]{1,6})` gives X, Y
- Counter: fixtures=48/49 — killed by fixture(s): position
- Missing selftest assertion: selftest "pos" uses positive coordinates only; missing a negative-coordinate case (-1920x0).

### scale-bound-02 (parse_scale, line 220)

- Edit: `rule["scale"] = 1.0 if s < 0.25 else s` -> `rule["scale"] = 1.0 if s < 0.2 else s`
- Contract attacked: S < 0.25 becomes 1.0, as Hyprland's parser does
- Counter: fixtures=48/49 — killed by fixture(s): scale-tiny-is-1
- Missing selftest assertion: missing tiny-scale selftest: S=0.2 must become scale 1.0 (rule line scale=1.0000).

### eff-desc-substr (effective, line 352)

- Edit: `if desc.startswith(sel[5:].strip(" \t")):` -> `if sel[5:].strip(" \t") in desc:`
- Contract attacked: selector `desc:TEXT`: description starts with TEXT stripped of spaces and tabs
- Counter: fixtures=48/49 — killed by fixture(s): desc-not-prefix
- Missing selftest assertion: selftest desc cases (desc-later, readd-moves) all start with TEXT; missing a desc-contains-but-not-starts case (desc "X Dell ..." with rule desc:Dell must stay UNRULED).

### fmt-rule-rate-1dp (output formats, line 403)

- Edit: `mode = "%dx%d@%.2f" % (r["w"], r["h"], r["rate"])` -> `mode = "%dx%d@%.1f" % (r["w"], r["h"], r["rate"])`
- Contract attacked: mode=<WxH@R|...> ... R is printed with two decimals
- Counter: fixtures=15/49 — killed by fixture(s): host, no-rate-requests-60, no-rate-live-59.99, rate-exactly-1-off, rate-144, resolution, position, auto-position, scale-clean, scale-1.6, scale-1.3-corrected, scale-1.3-as-written, scale-tiny-is-1, transform-key, transform-unset, transform-modifier, transform-modifier-bad, same-selector-erases, desc-added-later-wins, name-added-later-wins, readd-moves-last, desc-not-prefix, fallback-first-empty-and-named, unruled-only, live-disabled, mirror-agree, mirror-missing, ignored-keys, monitorv2, comments, wrong-types, addreserved-keeps-rule, two-files-later-overrides, stdin
- Missing selftest assertion: selftest never asserts MADO_MON_RULE text; missing rule-line format assertion (R printed with two decimals).

### fmt-scale-2dp (output formats, line 405)

- Edit: `scale = "auto" if r["scale"] is None else "%.4f" % r["scale"]` -> `scale = "auto" if r["scale"] is None else "%.2f" % r["scale"]`
- Contract attacked: S with four (decimals)
- Counter: fixtures=15/49 — killed by fixture(s): host, no-rate-requests-60, no-rate-live-59.99, rate-exactly-1-off, rate-144, resolution, position, auto-position, scale-clean, scale-1.6, scale-1.3-corrected, scale-1.3-as-written, scale-tiny-is-1, transform-key, transform-unset, transform-modifier, transform-modifier-bad, same-selector-erases, desc-added-later-wins, name-added-later-wins, readd-moves-last, desc-not-prefix, fallback-first-empty-and-named, unruled-only, live-disabled, mirror-agree, mirror-missing, ignored-keys, monitorv2, comments, wrong-types, addreserved-keeps-rule, two-files-later-overrides, stdin
- Missing selftest assertion: selftest never asserts MADO_MON_RULE text; missing rule-line format assertion (S printed with four decimals).

### fmt-mirror-no-dash (output formats, line 408)

- Edit: `json.dumps(r["mirror"]) if r["mirror"] else "-", "true" if r["disabled"] else "false")` -> `json.dumps(r["mirror"]), "true" if r["disabled"] else "false")`
- Contract attacked: mirror=<json|->
- Counter: fixtures=11/49 — killed by fixture(s): host, no-rate-requests-60, no-rate-live-59.99, rate-exactly-1-off, rate-144, resolution, position, auto-position, fallback-preferred, scale-clean, scale-1.6, scale-1.3-corrected, scale-1.3-as-written, scale-tiny-is-1, transform-key, transform-unset, transform-modifier, transform-modifier-bad, same-selector-erases, desc-added-later-wins, name-added-later-wins, readd-moves-last, desc-not-prefix, fallback-first-empty-and-named, unruled-only, disabled-agree, disabled-but-live, live-disabled, mirror-agree, ignored-keys, monitorv2, comments, wrong-types, addreserved-adds-default, addreserved-keeps-rule, two-files-later-overrides, highres-not-compared, stdin
- Missing selftest assertion: selftest never asserts MADO_MON_RULE text; missing assertion that an empty mirror prints as -.

### fmt-sum-label (output formats, line 442)

- Edit: `out.append("MADO_MONITORS: lines=%d rules=%d v2=%d unsupported=%d badrules=%d outputs=%d matched=%d "` -> `out.append("MADO_MONITORS: lines=%d rules=%d v2=%d unsup=%d badrules=%d outputs=%d matched=%d "`
- Contract attacked: last MADO_MONITORS: lines=<n> ... unsupported=<n> ...
- Counter: fixtures=4/49 — killed by fixture(s): host, no-rate-requests-60, no-rate-live-59.99, rate-exactly-1-off, rate-144, resolution, position, auto-position, fallback-preferred, scale-clean, scale-1.6, scale-1.3-corrected, scale-1.3-as-written, scale-tiny-is-1, transform-key, transform-unset, transform-modifier, transform-modifier-alone, transform-modifier-bad, same-selector-erases, desc-added-later-wins, name-added-later-wins, readd-moves-last, desc-not-prefix, fallback-first-empty-and-named, unruled-only, disabled-agree, disabled-but-live, live-disabled, mirror-agree, mirror-missing, unknown-key-drops-rule, ignored-keys, sdr-eotf-drops-rule, monitorv2, variable, unsupported-rate-suffix, comments, no-rules, wrong-types, addreserved-adds-default, addreserved-keeps-rule, two-files-later-overrides, highres-not-compared, stdin
- Missing selftest assertion: selftest checks only lines[-1].endswith(verdict=V); missing summary-token assertion (unsupported= label).

### keys-drop-bitdepth (parse_line keys, line 105)

- Edit: `KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")` -> `KEYS = ("mirror", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")`
- Contract attacked: keys mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc each consume the next field
- Counter: fixtures=48/49 — killed by fixture(s): ignored-keys
- Missing selftest assertion: missing ignored-key selftest case (bitdepth 10 consumed, rule kept, AGREE).

### keys-add-sdr-eotf (parse_line keys, line 105)

- Edit: `KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")` -> `KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc", "sdr_eotf")`
- Contract attacked: any other key adds one to `badrules` and the rule is not added (Hyprland returns "invalid syntax" ...)
- Counter: fixtures=48/49 — killed by fixture(s): sdr-eotf-drops-rule
- Missing selftest assertion: missing sdr_eotf selftest case (unknown key must drop the rule: badrules=1, UNRULED).

### disable-single (parse_line, line 241)

- Edit: `if kind in ("disable", "disabled"):` -> `if kind == "disable":`
- Contract attacked: field 1 `disable` or `disabled`: add a rule (SEL, disabled)
- Counter: fixtures=48/49 — killed by fixture(s): disabled-but-live
- Missing selftest assertion: selftest disabled cases use only the `disable` spelling; missing the `disabled` spelling case.

## Matrix D — killed by SELFTEST (counter not run, per tasking)

`mode-wh-swap` (parse_mode), `mode-explicit-label` (parse_mode), `add-no-erase` (add), `add-prepend` (add), `eff-first-wins` (effective), `eff-no-empty-fallback` (effective), `cmp-rate-tol-le` (compare), `es-no-correction` (expected_scale), `cmp-mirror-by-name` (compare), `vrd-and-or` (verdict order), `vrc-differ-2` (verdict order), `vrd-notcompared-4` (verdict order), `fmt-out-label` (output formats), `pl-keep-dollar` (parse_line), `badkey-break` (parse_line), `new-default-transform-1` (new_rule), `disabled-verdict-swap` (compare), `pl-fields-nostrip` (parse_line)

## Restoration evidence

- Reference sha256 before sweep: `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be`
- Reference sha256 after sweep: `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be` (computed from a fresh read at matrix generation time; identical — the frozen file was only ever read)
- Counter sha256: `c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34` (frozen, unmodified)
- All mutants lived and died under /fast/scratch/hyaku/mado-r45/MutTool/; the lane git index was never touched (clone-only, shared objects, commits in scratch clone HEAD only).
