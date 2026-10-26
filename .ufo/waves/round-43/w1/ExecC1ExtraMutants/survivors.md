# C1 mutation population — 68 new single-defect mutants of the reference tool

Reference: `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (`ref.py` here; `diff` against `tools/mado-geometry.py` at HEAD is empty).
Each mutant is one text replacement asserted to match the reference exactly once (`mutants.json` records the pair; `diff -u ref.py mutants/<name>.py` is one hunk, one removed line, one added line — section B of `equiv.txt`); every mutant file compiles.

Scoring command per mutant (private nonce `exm43NNNN`, `C1R42_TMP` under `/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants/run/<name>`):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && C1R42_TMP=<scratch>/<name> \
  python3 -I quality/counters/c1-r42-geometry.py --repo . \
    --rev b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 \
    --base a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f \
    --tool .ufo/waves/round-43/w1/ExecC1ExtraMutants/mutants/<name>.py --nonce <nonce>
```

`verdict` is the counter's own final-line verdict; a mutant that reaches `TARGET_MET` is a survivor the predicate does not kill.
Raw per-run data: `results.json` (final line, clauses line, every failing fixture line).

| # | mutant | category | edit (reference -> mutant) | verdict | failing fixtures / clauses |
|---|---|---|---|---|---|
| 1 | `N01-stdin-read-plus2` | value-domain | `data = stdin.read(MAX_BYTES + 1) -> data = stdin.read(MAX_BYTES + 2)` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 2 | `N02-read-tail-ge` | boundary-shift | `    if len(data) > MAX_BYTES:\n        raise Setup("too_large")\n    return data ->     if len(data) >= MAX_BYTES:\n        raise Setup("too_large"...` | TARGET_MISSED (killed) | fixtures: boundary0 |
| 3 | `N03-maxbytes-minus1` | wrong-constant | `MAX_BYTES = 1048576 -> MAX_BYTES = 1048575` | TARGET_MISSED (killed) | fixtures: stdinok0, boundary0 |
| 4 | `N04-num-1-4` | value-domain | `NUM = re.compile(r"[0-9]{1,5}") -> NUM = re.compile(r"[0-9]{1,4}")` | TARGET_MISSED (killed) | fixtures: size0 |
| 5 | `N05-num-1-6` | value-domain | `NUM = re.compile(r"[0-9]{1,5}") -> NUM = re.compile(r"[0-9]{1,6}")` | TARGET_MISSED (killed) | fixtures: size0; clauses: b=0, b2=0, b3=0 |
| 6 | `N06-safe-1-199` | value-domain | `){1,200}") -> ){1,199}")` | TARGET_MISSED (killed) | fixtures: regex0; clauses: b=0, b2=0, b3=0 |
| 7 | `N07-safe-2-200` | value-domain | `){1,200}") -> ){2,200}")` | TARGET_MISSED (killed) | fixtures: gen8, stdinok0, filecl0, multi0(+14); clauses: b=0, b2=0, b3=0 |
| 8 | `N08-matchfield-star` | value-domain | `MATCH_FIELD = re.compile(r"match:class[ \t]+(.+)") -> MATCH_FIELD = re.compile(r"match:class[ \t]+(.*)")` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 9 | `N09-split-maxsplit` | value-domain | `fields = [f.strip(" \t") for f in body.split(",")] -> fields = [f.strip(" \t") for f in body.split(",", 1)]` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 10 | `N10-fields-eq3` | wrong-constant | `good = len(fields) == 2 -> good = len(fields) == 3` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+27); clauses: b=0, b2=0, b3=0 |
| 11 | `N11-float-lower` | value-domain | `good = len(args) == 1 and args[0] in ("on", "off") -> good = len(args) == 1 and args[0].lower() in ("on", "off")` | TARGET_MISSED (killed) | fixtures: float0 |
| 12 | `N12-float-two-args` | boundary-shift | `good = len(args) == 1 and args[0] in ("on", "off") -> good = len(args) <= 2 and args[0] in ("on", "off")` | TARGET_MISSED (killed) | fixtures: gen1, gen7, float0, other0 |
| 13 | `N13-size-first-arg-only` | dropped-check | `good = len(args) == 2 and all(NUM.fullmatch(a) for a in args) -> good = len(args) == 2 and NUM.fullmatch(args[0])` | TARGET_MISSED (killed) | fixtures: size0 |
| 14 | `N14-effect-no-default` | dropped-branch | `effect = toks[0] if toks else "" -> effect = toks[0]` | TARGET_MISSED (killed) | fixtures: gen4, gen5, space0, other0 |
| 15 | `N15-effect-add-center` | value-domain | `if effect not in ("size", "float"): -> if effect not in ("size", "float", "center"):` | TARGET_MISSED (killed) | fixtures: other0; clauses: b=0, b2=0, b3=0 |
| 16 | `N16-line-rstrip-only` | dropped-branch | `line = raw.strip(" \t") -> line = raw.rstrip(" \t")` | TARGET_MISSED (killed) | fixtures: space0; clauses: b=0, b2=0, b3=0 |
| 17 | `N17-line-strip-cr` | value-domain | `line = raw.strip(" \t") -> line = raw.strip(" \t\r")` | TARGET_MISSED (killed) | fixtures: space0; clauses: b=0, b2=0, b3=0 |
| 18 | `N18-rule-line-plus` | value-domain | `RULE_LINE = re.compile(r"windowrule[ \t]*=(.*)") -> RULE_LINE = re.compile(r"windowrule[ \t]*=(.+)")` | TARGET_MISSED (killed) | fixtures: other0 |
| 19 | `N19-rule-line-caret` | value-domain | `RULE_LINE = re.compile(r"windowrule[ \t]*=(.*)") -> RULE_LINE = re.compile(r"^windowrule[ \t]*=(.*)")` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 20 | `N20-mapped-eq` | operator-swap | `if c.get("mapped") is False: -> if c.get("mapped") == False:` | TARGET_MISSED (killed) | fixtures: mapped0; clauses: b=0, b2=0, b3=0 |
| 21 | `N21-floating-eq` | operator-swap | `floating = c.get("floating") is True -> floating = c.get("floating") == True` | TARGET_MISSED (killed) | fixtures: gen1, gen6, gen7, client0; clauses: b=0, b2=0, b3=0 |
| 22 | `N22-size-gt-minus1` | boundary-shift | `isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s): -> isinstance(v, int) and not isinstance(v, bool) and v > -1 for v in s):` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 23 | `N23-size-type-is-int` | value-domain | `isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s): -> type(v) is int and v >= 0 for v in s):` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 24 | `N24-size-len3` | wrong-constant | `if isinstance(s, list) and len(s) == 2 and all( -> if isinstance(s, list) and len(s) == 3 and all(` | TARGET_MISSED (killed) | fixtures: gen1, gen2, gen3, gen4(+21); clauses: b=0, b2=0, b3=0 |
| 25 | `N25-ctl-below-1f` | value-domain | `if any(ord(ch) < 0x20 for ch in cls): -> if any(ord(ch) < 0x1f for ch in cls):` | TARGET_MISSED (killed) | fixtures: ctlclass0 |
| 26 | `N26-ctl-below-7f` | value-domain | `if any(ord(ch) < 0x20 for ch in cls): -> if any(ord(ch) < 0x7f for ch in cls):` | TARGET_MISSED (killed) | fixtures: gen2, gen3, gen4, gen9(+19); clauses: b=0, b2=0, b3=0 |
| 27 | `N27-selftest-prefix` | dropped-check | `if argv == ["--selftest"]: -> if argv and argv[0] == "--selftest":` | TARGET_MISSED (killed) | fixtures: usage0; clauses: b=0, b2=0, b3=0 |
| 28 | `N28-double-clients` | dropped-check | `if flag == "--clients" and clients is None: -> if flag == "--clients":` | TARGET_MISSED (killed) | fixtures: usage0; clauses: b=0, b2=0, b3=0 |
| 29 | `N29-rules-optional` | dropped-check | `if clients is None or not rules: -> if clients is None:` | TARGET_MISSED (killed) | fixtures: usage0; clauses: b=0, b2=0, b3=0 |
| 30 | `N30-ok-exit3` | exit-code | `verdict, rc = "OK", 0 -> verdict, rc = "OK", 3` | TARGET_MISSED (killed) | fixtures: gen5, gen6, gen9, stdin0(+13); clauses: b=0, b2=0, b3=0 |
| 31 | `N31-nosize-exit3` | exit-code | `verdict, rc = "NO_SIZE_RULES", 4 -> verdict, rc = "NO_SIZE_RULES", 3` | TARGET_MISSED (killed) | fixtures: gen4, gen6, size0, space0(+1); clauses: b=0, b2=0, b3=0 |
| 32 | `N32-differ-exit2` | exit-code | `verdict, rc = "DIFFER", 1 -> verdict, rc = "DIFFER", 2` | TARGET_MISSED (killed) | fixtures: gen1, gen3, gen5, gen6(+6); clauses: b=0, b2=0, b3=0 |
| 33 | `N33-nomatch-exit4` | exit-code | `verdict, rc = "NO_MATCHING_CLIENT", 3 -> verdict, rc = "NO_MATCHING_CLIENT", 4` | TARGET_MISSED (killed) | fixtures: gen1, gen3, gen5, gen7(+2); clauses: b=0, b2=0, b3=0 |
| 34 | `N34-differ-and-matched` | reordered-check | `elif t["differ"] > 0: -> elif t["differ"] > 0 and t["matched"] > 0:` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 35 | `N35-summary-floatcount` | swapped-field | `len(rules) - size_rules, -> len(rules),` | TARGET_MISSED (killed) | fixtures: gen0, gen2, gen3, gen4(+26); clauses: b=0, b2=0, b3=0 |
| 36 | `N36-summary-size-sums-float` | wrong-constant | `size_rules = sum(1 for r in rules if r["effect"] == "size") -> size_rules = sum(1 for r in rules if r["effect"] == "float")` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+25); clauses: b=0, b2=0, b3=0 |
| 37 | `N37-client-addr-class-swap` | swapped-output-field | `json.dumps(addr), json.dumps(cls), "true" if floating else "false", -> json.dumps(cls), json.dumps(addr), "true" if floating else "false",` | TARGET_MISSED (killed) | fixtures: gen0, gen2, gen4, gen6(+21); clauses: b=0, b2=0, b3=0 |
| 38 | `N38-addr-default-empty` | value-domain | `addr = c.get("address") if isinstance(c.get("address"), str) else "-" -> addr = c.get("address") if isinstance(c.get("address"), str) else ""` | TARGET_MISSED (killed) | fixtures: stdin0, filecl0, multi0, boundary0(+15) |
| 39 | `N39-class-default-dash` | value-domain | `cls = c.get("class") if isinstance(c.get("class"), str) else "" -> cls = c.get("class") if isinstance(c.get("class"), str) else "-"` | TARGET_MISSED (killed) | fixtures: gen2, client0 |
| 40 | `N40-file-index-from-2` | off-by-one | `for k, text in enumerate(rule_texts, 1): -> for k, text in enumerate(rule_texts, 2):` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+27); clauses: b=0, b2=0, b3=0 |
| 41 | `N41-rule-number-from-0` | off-by-one | `for n, r in enumerate(rules, 1)] -> for n, r in enumerate(rules, 0)]` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen4(+26); clauses: b=0, b2=0, b3=0 |
| 42 | `N42-first-size-wins` | reordered-check | `            if matches(r["rx"], cls): ->             if matches(r["rx"], cls) and want is None:` | TARGET_MISSED (killed) | fixtures: gen4, gen7, regex0, float0(+3); clauses: b=0, b2=0, b3=0 |
| 43 | `N43-size-resets-frule` | dropped-state | `                    want = r["want"] ->                     want, frule = r["want"], "-"` | TARGET_MISSED (killed) | fixtures: multi0, order0; clauses: b=0, b2=0, b3=0 |
| 44 | `N44-tally-assign` | dropped-accumulation | `        tally[verdict.lower()] += 1 ->         tally[verdict.lower()] = 1` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen5, gen7(+14) |
| 45 | `N45-unmapped-counts-clients` | swapped-field | `            tally["unmapped"] += 1 ->             tally["clients"] += 1` | TARGET_MISSED (killed) | fixtures: gen0, gen6, gen8, mapped0; clauses: b=0, b2=0, b3=0 |
| 46 | `N46-doc-tuple` | value-domain | `if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc): -> if not isinstance(doc, (list, tuple)) or not all(isinstance(c, dict) ...` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 47 | `N47-doc-any-not-all` | operator-swap | `if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc): -> if not isinstance(doc, list) or not any(isinstance(c, dict) for c in ...` | TARGET_MISSED (killed) | fixtures: gen0, stdinok0, badjson0, empty0; clauses: b=0, b2=0, b3=0 |
| 48 | `N48-rules-decode-ignore` | value-domain | `texts = [read_regular(p).decode("utf-8", "replace") for p in rules] -> texts = [read_regular(p).decode("utf-8", "ignore") for p in rules]` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 49 | `N49-json-decode-strict` | value-domain | `doc = json.loads(data.decode("utf-8")) -> doc = json.loads(data.decode("utf-8", "strict"))` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 50 | `N50-summary-other-swap` | swapped-field | `counts["other"], counts["unsupported"], -> counts["unsupported"], counts["other"],` | TARGET_MISSED (killed) | fixtures: gen0, gen2, gen3, gen4(+8); clauses: b=0, b2=0, b3=0 |
| 51 | `N51-close-fd-pass` | dropped-branch | `        os.close(fd) ->         pass` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 52 | `N52-size-truthiness` | value-domain | `"%dx%d" % size if size else "-" -> "%dx%d" % size if size is not None else "-"` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 53 | `N53-fullmatch-dotall` | value-domain | `return re.fullmatch(rx, cls) is not None -> return re.fullmatch(rx, cls, re.DOTALL) is not None` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 54 | `N54-read-chunk-cap` | value-domain | `chunk = os.read(fd, MAX_BYTES + 1 - len(data)) -> chunk = os.read(fd, MAX_BYTES)` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |
| 55 | `N55-client-order-reversed` | dropped-stability | `lines += clines -> lines += list(reversed(clines))` | TARGET_MISSED (killed) | fixtures: gen0, gen4, gen5, gen6(+14); clauses: b=0, b2=0, b3=0 |
| 56 | `N56-ctl-guard-dropped` | dropped-branch | `if any(ord(ch) < 0x20 for ch in cls): -> if False:` | TARGET_MISSED (killed) | fixtures: ctlclass0 |
| 57 | `N57-reverse-client-order` | dropped-stability | `    for c in clients: ->     for c in reversed(clients):` | TARGET_MISSED (killed) | fixtures: gen0, gen5, gen8, stdin0(+11); clauses: b=0, b2=0, b3=0 |
| 58 | `N58-size-key-index` | dropped-branch | `    s = c.get("size") ->     s = c["size"]` | TARGET_MISSED (killed) | fixtures: client0 |
| 59 | `N59-size-tuple-swap` | swapped-output-field | `        return (s[0], s[1]) ->         return (s[1], s[0])` | TARGET_MISSED (killed) | fixtures: gen2, gen5, gen7, stdin0(+17); clauses: b=0, b2=0, b3=0 |
| 60 | `N60-safe-prefix-match` | operator-swap | `    if not SAFE.fullmatch(rx): ->     if not SAFE.match(rx):` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen5, gen6(+2); clauses: b=0, b2=0, b3=0 |
| 61 | `N61-regexok-call-dropped` | dropped-check | `        if not mm or not regex_ok(mm.group(1)): ->         if not mm:` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen3, gen8(+3); clauses: b=0, b2=0, b3=0 |
| 62 | `N62-parse-step-1` | off-by-one | `        i += 2 ->         i += 1` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+32); clauses: b=0, b2=0, b3=0 |
| 63 | `N63-parse-loop-le` | boundary-shift | `    while i < len(argv): ->     while i <= len(argv):` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+32); clauses: b=0, b2=0, b3=0 |
| 64 | `N64-nosize-inverted` | reordered-check | `    if size_rules == 0: ->     if size_rules != 0:` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+27); clauses: b=0, b2=0, b3=0 |
| 65 | `N65-badsize-key-rename` | wrong-constant | `"tiled": 0, "badsize": 0} -> "tiled": 0, "bad_size": 0}` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+27); clauses: b=0, b2=0, b3=0 |
| 66 | `N66-summary-clients-key` | swapped-output-field | `unsupported=%d clients=%d " -> unsupported=%d client=%d "` | TARGET_MISSED (killed) | fixtures: gen0, gen1, gen2, gen3(+27); clauses: b=0, b2=0, b3=0 |
| 67 | `N67-unreadable-as-toolarge` | wrong-constant | `raise Setup("unreadable")\n        data = b"" -> raise Setup("too_large")\n        data = b""` | TARGET_MISSED (killed) | fixtures: unreadable0, fifo0; clauses: b=0, b2=0, b3=0 |
| 68 | `N68-stdout-print` | value-domain | `    sys.stdout.write("\n".join(lines) + "\n") ->     print("\n".join(lines))` | TARGET_MET (survivor) | none — 37/37 fixtures, clauses a,b,b2,b3,g all 1 |

Totals: 68 mutants, 53 killed, 15 survivors.

## Survivors

### `N01-stdin-read-plus2` — EQUIVALENT

* edit: `data = stdin.read(MAX_BYTES + 1)` -> `data = stdin.read(MAX_BYTES + 2)`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430000`
* **Proof.** `--clients -` is the only stdin read, and its bytes are consumed only by `if len(data) > MAX_BYTES` (`run()`, reference line 255). A single `read(n)` on a pipe returns `min(available, n)` bytes, so `read(MAX_BYTES + 2) > MAX_BYTES` iff `read(MAX_BYTES + 1) > MAX_BYTES` iff the stream holds at least MAX_BYTES+1 bytes; the tool then either raises `too_large` or parses the bytes it holds and never reads stdin again, so no leftover byte is observable. stdout, stderr and the exit code coincide on every input. **Evidence:** `witness.txt` section C — stdin of 2, MAX-1, MAX, MAX+1, MAX+2 and 2*MAX bytes: identical rc and stdout in all six.

### `N08-matchfield-star` — EQUIVALENT

* edit: `MATCH_FIELD = re.compile(r"match:class[ \t]+(.+)")` -> `MATCH_FIELD = re.compile(r"match:class[ \t]+(.*)")`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430007`
* **Proof.** MATCH_FIELD is applied with `.fullmatch` to `fields[1]`, already stripped of spaces and tabs at both ends, and the line was split on `"\n"` before that, so the field cannot end in whitespace of any kind. `match:class[ \t]+(.*)` accepts a field only as `match:class` + at least one space/tab + a tail; `(.+)` additionally demands a non-empty tail, which would mean the field ends in a space or tab — impossible. Both patterns accept the same fields with the same capture (and an empty capture would be rejected by `regex_ok("")` anyway). **Evidence:** `equiv.txt` section A — 2546 inputs, 0 differences.

### `N09-split-maxsplit` — EQUIVALENT

* edit: `fields = [f.strip(" \t") for f in body.split(",")]` -> `fields = [f.strip(" \t") for f in body.split(",", 1)]`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430008`
* **Proof.** The two splits differ only when the body holds a second comma AND field 0's first token is `size`/`float` (any other effect takes the `other` branch first, in both). Then the mutant's field 1 is the whole remainder, which contains at least one `,`; MATCH_FIELD may capture it, but `,` is neither in SAFE's alphabet nor an admissible escape, so `regex_ok` is False and the line counts as `unsupported` — exactly what the reference's `len(fields) == 2` test produces. Same rule list, same `other`/`unsupported` counters, same stdout/rc. **Evidence:** `equiv.txt` section A, 2546 inputs including `windowrule = size 1 2,, match:class a` and `windowrule = size 1 2, match:class a, match:title b`; 0 differences.

### `N19-rule-line-caret` — EQUIVALENT

* edit: `RULE_LINE = re.compile(r"windowrule[ \t]*=(.*)")` -> `RULE_LINE = re.compile(r"^windowrule[ \t]*=(.*)")`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430018`
* **Proof.** RULE_LINE is only used as `RULE_LINE.fullmatch(line)`; `.fullmatch` already requires the match to start at position 0, and the pattern carries no `re.MULTILINE`, so the added `^` asserts exactly what `.fullmatch` already asserts. The accepted line set is unchanged.

### `N22-size-gt-minus1` — EQUIVALENT

* edit: `isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s):` -> `isinstance(v, int) and not isinstance(v, bool) and v > -1 for v in s):`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430021`
* **Proof.** `v` reaches this test only from a `size` array decoded by `json.loads` with the default integer hook, so once `isinstance(v, int)` and `not isinstance(v, bool)` have passed, `v` is an exact `int`; on ints `v >= 0` and `v > -1` are the same predicate. No other Python type reaches the comparison.

### `N23-size-type-is-int` — EQUIVALENT

* edit: `isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in s):` -> `type(v) is int and v >= 0 for v in s):`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430022`
* **Proof.** `client_size` is called only on elements of `parse_clients`' `json.loads` result (`doc = json.loads(data.decode("utf-8"))`, reference line 164, no `parse_*` hooks), so a `size` element is exactly an `int`, `bool`, `float`, `str`, `None`, `list` or `dict`. On that domain `isinstance(v, int) and not isinstance(v, bool)` and `type(v) is int` agree (bool is the only int subclass JSON can produce, and both spellings exclude it). Same `size` / `size is None` decision for every contract input. **Evidence:** `equiv.txt` section A, 2546 inputs incl. `[true,2]`, `[1,false]`, `[1.0,2]`; 0 differences.

### `N34-differ-and-matched` — EQUIVALENT

* edit: `elif t["differ"] > 0:` -> `elif t["differ"] > 0 and t["matched"] > 0:`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430033`
* **Proof.** `tally["differ"]` is incremented only for a client that already ran `tally["matched"] += 1` in the same iteration (reference lines 205-216), so `differ > 0` implies `matched > 0` on every input; the added conjunct is a tautology inside the ladder and cannot change any verdict or exit code. **Evidence:** `equiv.txt` section A, 2546 inputs, 0 differences.

### `N46-doc-tuple` — EQUIVALENT

* edit: `if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc):` -> `if not isinstance(doc, (list, tuple)) or not all(isinstance(c, dict) for c in doc):`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430045`
* **Proof.** `doc` is only ever the return value of `parse_clients`, i.e. `json.loads(...)`; `json.loads` decodes a JSON array to a `list` and never to a `tuple`, so `isinstance(doc, (list, tuple))` adds no reachable branch. **Evidence:** `equiv.txt` section A, 2546 inputs incl. the `RAWEDGE` set, 0 differences.

### `N48-rules-decode-ignore` — MISSING CHECK

* edit: `texts = [read_regular(p).decode("utf-8", "replace") for p in rules]` -> `texts = [read_regular(p).decode("utf-8", "ignore") for p in rules]`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430047`
* **Fixture that would kill it.** One rules file holding the bytes `b'windowrule = size 1 2, match:class a\xff\n'`, clients `[{"class":"a","size":[1,2],"floating":true}]`. Expected (model: `.decode("utf-8","replace")` gives the regex `a\ufffd`, outside SAFE's alphabet):

```
MADO_GEOMETRY: rules=0 float_rules=0 other=0 unsupported=1 clients=1 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_SIZE_RULES
```

on stdout, exit 4. The mutant instead prints `MADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a`, a `verdict=AGREE` client line and `verdict=OK`, exit 0 (`witness.txt` section E). The predicate has no such fixture: `put()` writes every rules text as already-valid UTF-8 (`str.encode` with `surrogateescape`, and no fixture passes a lone surrogate), so the `errors=` handler is never exercised — the `replace` in the contract sentence and the reference is untested by the whole 37-fixture population.

### `N49-json-decode-strict` — EQUIVALENT

* edit: `doc = json.loads(data.decode("utf-8"))` -> `doc = json.loads(data.decode("utf-8", "strict"))`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430048`
* **Proof.** `bytes.decode(encoding, errors)` defaults to `errors='strict'`; naming the default handler changes no behaviour, so the same `UnicodeDecodeError` reaches `except (UnicodeDecodeError, ValueError)` and yields the same `bad_json` Setup. **Evidence:** `equiv.txt` section A, 2546 inputs including `b'\xff'`, `b'[{"class":"a\xffb",...}]'`, `b'\xef\xbb\xbf[]'` and lone surrogates; 0 differences.

### `N51-close-fd-pass` — MISSING CHECK

* edit: `        os.close(fd)` -> `        pass`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430050`
* **Fixture that would kill it.** 300 `--rules` files (the first holding `windowrule = size 1 2, match:class a\n`, the other 299 empty), clients `[{"class":"a","size":[1,2],"floating":true}]`, the tool run under `RLIMIT_NOFILE=128`: expected

```
MADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a
MADO_GEOM_CLIENT: addr="-" class="a" floating=true size=1x2 want=1x2 float_rule=- verdict=AGREE
MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 verdict=OK
```

on stdout, exit 0. The reference prints exactly that; the mutant leaks one descriptor per file and dies with `MADO_GEOMETRY: SETUP unreadable`, exit 2 (`witness.txt` section F; the same at 64 and 32). The leak is output-invisible otherwise, and the predicate cannot see it: its own harness applies only `prlimit --nproc=1:1` (`execute()`), sets no `RLIMIT_NOFILE`, and no fixture passes more than three rule files.

### `N52-size-truthiness` — EQUIVALENT

* edit: `"%dx%d" % size if size else "-"` -> `"%dx%d" % size if size is not None else "-"`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430051`
* **Proof.** `size` is either `None` or a two-element tuple; every two-element tuple is truthy, `(0, 0)` included, so `if size` and `if size is not None` choose the same branch for every contract input. **Evidence:** `equiv.txt` section A (2546 inputs incl. `size [0,0]`), 0 differences.

### `N53-fullmatch-dotall` — EQUIVALENT

* edit: `return re.fullmatch(rx, cls) is not None` -> `return re.fullmatch(rx, cls, re.DOTALL) is not None`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430052`
* **Proof.** `re.DOTALL` changes only whether `.` matches a newline. Every class that reaches `re.fullmatch` has already been rejected if it holds any codepoint below U+0020 (`matches`, reference line 181), so no class contains `\n`; and a REGEX can carry no inline flag (`(?` is banned), no bracket class, no `{`, and no literal control character (SAFE's alphabet). DOTALL is unreachable on every contract input. **Evidence:** `equiv.txt` section A, 2546 inputs incl. classes `a\nb`, `a\rb`, `a\x0bb`; 0 differences.

### `N54-read-chunk-cap` — EQUIVALENT

* edit: `chunk = os.read(fd, MAX_BYTES + 1 - len(data))` -> `chunk = os.read(fd, MAX_BYTES)`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430053`
* **Proof.** `read_regular`'s bytes are used only as `len(data) > MAX_BYTES` and, when that is false, as the complete file content. With the unchanged loop condition `len(data) <= MAX_BYTES`, a per-read cap of `MAX_BYTES` still ends the loop at EOF or as soon as the running total exceeds `MAX_BYTES`, and the total is the file's size either way: the mutant returns the same bytes for every regular file ≤ MAX_BYTES and `too_large` for every file > MAX_BYTES (short reads change only the number of iterations). **Evidence:** `witness.txt` section D — clients and rules files at MAX-1, MAX, MAX+1 and 2*MAX: identical rc and stdout.

### `N68-stdout-print` — EQUIVALENT

* edit: `    sys.stdout.write("\n".join(lines) + "\n")` -> `    print("\n".join(lines))`
* counter: `fixtures=37/37 tool=present verdict=TARGET_MET rev=b2e2efd6e268920d31f3c32cf52dc097dd6e1d22 nonce=exm430067`
* **Proof.** `print(x)` writes `x` followed by one `\n` to `sys.stdout`, byte-identical to `sys.stdout.write(x + "\n")`, and this is the only write in `run()`. **Evidence:** `witness.txt` section G — agree / differ / no-size-rules / setup-unreadable all have byte-identical stdout, stderr and rc.

