import json
import os

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecC1ExtraMutants"

C = {}

C["N01-stdin-read-plus2"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `--clients -` is the only stdin read, and its bytes are consumed only by "
    "`if len(data) > MAX_BYTES` (`run()`, reference line 255). A single `read(n)` on a pipe returns "
    "`min(available, n)` bytes, so `read(MAX_BYTES + 2) > MAX_BYTES` iff `read(MAX_BYTES + 1) > MAX_BYTES` "
    "iff the stream holds at least MAX_BYTES+1 bytes; the tool then either raises `too_large` or parses the bytes "
    "it holds and never reads stdin again, so no leftover byte is observable. stdout, stderr and the exit code "
    "coincide on every input. **Evidence:** `witness.txt` section C — stdin of 2, MAX-1, MAX, MAX+1, MAX+2 and "
    "2*MAX bytes: identical rc and stdout in all six."))

C["N08-matchfield-star"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** MATCH_FIELD is applied with `.fullmatch` to `fields[1]`, already stripped of spaces and tabs at "
    "both ends, and the line was split on `\"\\n\"` before that, so the field cannot end in whitespace of any kind. "
    "`match:class[ \\t]+(.*)` accepts a field only as `match:class` + at least one space/tab + a tail; `(.+)` "
    "additionally demands a non-empty tail, which would mean the field ends in a space or tab — impossible. "
    "Both patterns accept the same fields with the same capture (and an empty capture would be rejected by "
    "`regex_ok(\"\")` anyway). **Evidence:** `equiv.txt` section A — 2546 inputs, 0 differences."))

C["N09-split-maxsplit"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** The two splits differ only when the body holds a second comma AND field 0's first token is "
    "`size`/`float` (any other effect takes the `other` branch first, in both). Then the mutant's field 1 is the "
    "whole remainder, which contains at least one `,`; MATCH_FIELD may capture it, but `,` is neither in SAFE's "
    "alphabet nor an admissible escape, so `regex_ok` is False and the line counts as `unsupported` — exactly what "
    "the reference's `len(fields) == 2` test produces. Same rule list, same `other`/`unsupported` counters, same "
    "stdout/rc. **Evidence:** `equiv.txt` section A, 2546 inputs including `windowrule = size 1 2,, match:class a` "
    "and `windowrule = size 1 2, match:class a, match:title b`; 0 differences."))

C["N19-rule-line-caret"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** RULE_LINE is only used as `RULE_LINE.fullmatch(line)`; `.fullmatch` already requires the match to "
    "start at position 0, and the pattern carries no `re.MULTILINE`, so the added `^` asserts exactly what "
    "`.fullmatch` already asserts. The accepted line set is unchanged."))

C["N22-size-gt-minus1"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `v` reaches this test only from a `size` array decoded by `json.loads` with the default integer "
    "hook, so once `isinstance(v, int)` and `not isinstance(v, bool)` have passed, `v` is an exact `int`; on ints "
    "`v >= 0` and `v > -1` are the same predicate. No other Python type reaches the comparison."))

C["N23-size-type-is-int"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `client_size` is called only on elements of `parse_clients`' `json.loads` result (`doc = "
    "json.loads(data.decode(\"utf-8\"))`, reference line 164, no `parse_*` hooks), so a `size` element is exactly an "
    "`int`, `bool`, `float`, `str`, `None`, `list` or `dict`. On that domain "
    "`isinstance(v, int) and not isinstance(v, bool)` and `type(v) is int` agree (bool is the only int subclass "
    "JSON can produce, and both spellings exclude it). Same `size` / `size is None` decision for every contract "
    "input. **Evidence:** `equiv.txt` section A, 2546 inputs incl. `[true,2]`, `[1,false]`, `[1.0,2]`; 0 differences."))

C["N34-differ-and-matched"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `tally[\"differ\"]` is incremented only for a client that already ran `tally[\"matched\"] += 1` in the "
    "same iteration (reference lines 205-216), so `differ > 0` implies `matched > 0` on every input; the added "
    "conjunct is a tautology inside the ladder and cannot change any verdict or exit code. **Evidence:** "
    "`equiv.txt` section A, 2546 inputs, 0 differences."))

C["N46-doc-tuple"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `doc` is only ever the return value of `parse_clients`, i.e. `json.loads(...)`; `json.loads` "
    "decodes a JSON array to a `list` and never to a `tuple`, so `isinstance(doc, (list, tuple))` adds no reachable "
    "branch. **Evidence:** `equiv.txt` section A, 2546 inputs incl. the `RAWEDGE` set, 0 differences."))

C["N48-rules-decode-ignore"] = dict(kind="MISSING CHECK", text=(
    "**Fixture that would kill it.** One rules file holding the bytes "
    "`b'windowrule = size 1 2, match:class a\\xff\\n'`, clients `[{\"class\":\"a\",\"size\":[1,2],\"floating\":true}]`. "
    "Expected (model: `.decode(\"utf-8\",\"replace\")` gives the regex `a\\ufffd`, outside SAFE's alphabet):\n\n"
    "```\nMADO_GEOMETRY: rules=0 float_rules=0 other=0 unsupported=1 clients=1 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_SIZE_RULES\n```\n\n"
    "on stdout, exit 4. The mutant instead prints `MADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a`, a "
    "`verdict=AGREE` client line and `verdict=OK`, exit 0 (`witness.txt` section E). The predicate has no such "
    "fixture: `put()` writes every rules text as already-valid UTF-8 (`str.encode` with `surrogateescape`, and no "
    "fixture passes a lone surrogate), so the `errors=` handler is never exercised — the `replace` in the contract "
    "sentence and the reference is untested by the whole 37-fixture population."))

C["N49-json-decode-strict"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `bytes.decode(encoding, errors)` defaults to `errors='strict'`; naming the default handler changes "
    "no behaviour, so the same `UnicodeDecodeError` reaches `except (UnicodeDecodeError, ValueError)` and yields "
    "the same `bad_json` Setup. **Evidence:** `equiv.txt` section A, 2546 inputs including `b'\\xff'`, "
    "`b'[{\"class\":\"a\\xffb\",...}]'`, `b'\\xef\\xbb\\xbf[]'` and lone surrogates; 0 differences."))

C["N51-close-fd-pass"] = dict(kind="MISSING CHECK", text=(
    "**Fixture that would kill it.** 300 `--rules` files (the first holding `windowrule = size 1 2, match:class a\\n`, "
    "the other 299 empty), clients `[{\"class\":\"a\",\"size\":[1,2],\"floating\":true}]`, the tool run under "
    "`RLIMIT_NOFILE=128`: expected\n\n"
    "```\nMADO_GEOM_RULE: n=1 file=1 effect=size arg=1x2 class=a\nMADO_GEOM_CLIENT: addr=\"-\" class=\"a\" floating=true size=1x2 want=1x2 float_rule=- verdict=AGREE\nMADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 verdict=OK\n```\n\n"
    "on stdout, exit 0. The reference prints exactly that; the mutant leaks one descriptor per file and dies with "
    "`MADO_GEOMETRY: SETUP unreadable`, exit 2 (`witness.txt` section F; the same at 64 and 32). The leak is "
    "output-invisible otherwise, and the predicate cannot see it: its own harness applies only "
    "`prlimit --nproc=1:1` (`execute()`), sets no `RLIMIT_NOFILE`, and no fixture passes more than four rule files."))

C["N52-size-truthiness"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `size` is either `None` or a two-element tuple; every two-element tuple is truthy, `(0, 0)` "
    "included, so `if size` and `if size is not None` choose the same branch for every contract input. "
    "**Evidence:** `equiv.txt` section A (2546 inputs incl. `size [0,0]`), 0 differences."))

C["N53-fullmatch-dotall"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `re.DOTALL` changes only whether `.` matches a newline. Every class that reaches `re.fullmatch` has "
    "already been rejected if it holds any codepoint below U+0020 (`matches`, reference line 181), so no class "
    "contains `\\n`; and a REGEX can carry no inline flag (`(?` is banned), no bracket class, no `{`, and no literal "
    "control character (SAFE's alphabet). DOTALL is unreachable on every contract input. **Evidence:** "
    "`equiv.txt` section A, 2546 inputs incl. classes `a\\nb`, `a\\rb`, `a\\x0bb`; 0 differences."))

C["N54-read-chunk-cap"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `read_regular`'s bytes are used only as `len(data) > MAX_BYTES` and, when that is false, as the "
    "complete file content. With the unchanged loop condition `len(data) <= MAX_BYTES`, a per-read cap of "
    "`MAX_BYTES` still ends the loop at EOF or as soon as the running total exceeds `MAX_BYTES`, and the total is the "
    "file's size either way: the mutant returns the same bytes for every regular file ≤ MAX_BYTES and `too_large` "
    "for every file > MAX_BYTES (short reads change only the number of iterations). **Evidence:** `witness.txt` "
    "section D — clients and rules files at MAX-1, MAX, MAX+1 and 2*MAX: identical rc and stdout."))

C["N68-stdout-print"] = dict(kind="EQUIVALENT", text=(
    "**Proof.** `print(x)` writes `x` followed by one `\\n` to `sys.stdout`, byte-identical to "
    "`sys.stdout.write(x + \"\\n\")`, and this is the only write in `run()`. **Evidence:** `witness.txt` section G — "
    "agree / differ / no-size-rules / setup-unreadable all have byte-identical stdout, stderr and rc."))

json.dump(C, open(os.path.join(SEAT, "classify.json"), "w"), indent=1)
print("classify entries:", len(C))
