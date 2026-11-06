# R90MExecMako — D3: add selftest kills for the three round-89 mako survivors (RS01, RS05, RS12)

Seat `R90MExecMako` (executor, leaf). Lane `mado-shokunin`, round 90, wave `w1`, round shape v1. Base revision
`5041acf99e27263872bf0441ad5f9d4316152605` (master). Scratch `$S = /fast/scratch/hyaku/mado-r90/R90MExecMako`.

Scope: exactly the routed defect D3 of the round-90 declaration — "killing cases for RS01/RS05/RS12 added to
`tools/mado-mako.py --selftest`". The tool's resolution code is untouched; the candidate is a copy of the working-tree
tool with **added selftest checks only**.

## 1. Files written

| path | sha256 | note |
|---|---|---|
| `.ufo/waves/round-90/build/mado-mako.d3.py` | `fe8c8344ed6ce1fb1da7dd0f0118cb1434240dea4760590e6cd6d20b52cef324` | 855 lines (base 841); `diff -u` shows **14 added, 0 removed** lines |
| `.ufo/waves/round-90/w1/R90MExecMako.md` | — | this report |

Nothing else in the lane was written. `tools/mado-mako.py` is byte-identical to the base (`sha256
6b4bc409750f493469ce789b6b6c0c072d6ab638ff7e90dc9b31d642ae673a98`, unchanged after all runs). No git/jj mutation was run
anywhere; no installs (no pacman transaction attempted).

## 2. The three added checks (one per survivor) and their grounding

Each check lives inside `selftest()` and asserts the candidate's current behaviour; the citation is mako **v1.11.0**
`criteria.c` from `https://codeload.github.com/emersion/mako/tar.gz/refs/tags/v1.11.0` (downloaded tarball sha256
`72d11d3fca20a3dfbca0107ff875eace479751be0cf2ddd1dd5bafa131ac7282` = the task pin; file `criteria.c`, 573 lines), plus
the host manual `/usr/share/man/man5/mako.5.gz` lines already used by the tool header.

1. `regex-body-earlier-invalid` — kills **RS01**.
   `[body~=a(b body~=x]` with `--body x` → refusal containing `regcomp`, `width` stays `300` (section not applied).
   Ground: `criteria.c:209-212` (a token is applied when a space ends it) and `241-246` (the last token is applied at
   end-of-string) — every occurrence is applied in order; `344-350` compiles `body~` with
   `regcomp(REG_EXTENDED|REG_NOSUB)` on each application, so the earlier invalid `a(b` rejects the section even though the
   later occurrence is valid.
2. `bare-quoted-token` — kills **RS05**.
   `["x"]` → refusal containing `has no '=value'`, `width` stays `300`.
   Ground: `criteria.c:199-206` — in `MAKO_PARSE_STATE_NORMAL` a `"` switches to `MAKO_PARSE_STATE_QUOTE` without
   flushing the token buffer; `241-246` applies the resulting token at end-of-string, so a quote does not end or erase a
   token. The tool then refuses the unmodelled bare key (its declared stance, manual L510-516).
3. `group-index-field` / `grouped-field` (one check, two runs) — kills **RS12**.
   `[group-index=1]` and `[grouped=1]` each → refusal naming the field, `width` stays `300`.
   Ground: `criteria.c:134-141` matches these on the **second** pass from group state; `321-327` and `385-392` parse them
   upstream; the manual L474-495 declares them second-pass fields, which the tool's model does not carry, so they stay
   refused (the declaration's named limit).

The three insertions (exact text, after existing checks, nothing modified):

```python
        r = run("regex-body-earlier-invalid", "[body~=a(b body~=x]\nwidth=9\n", inputs={"body": "x"})
        check("an earlier invalid body~ occurrence rejects the section though a later one is valid "
              "(criteria.c:209-212,241-246 apply every token; 344-350 regcomp per body~)",
              any("regcomp" in s for s in r["refusals"]) and r["effective"]["width"] == "300")

        r = run("bare-quoted-token", '["x"]\nwidth=9\n')
        check("a quote opens grouping but does not end the token, so a bare quoted key is refused "
              "(criteria.c:199-206,241-246; L510-516)",
              any("has no '=value'" in s for s in r["refusals"]) and r["effective"]["width"] == "300")

        r = run("group-index-field", "[group-index=1]\nwidth=9\n")
        r2 = run("grouped-field", "[grouped=1]\nwidth=9\n")
        check("group-index and grouped are second-pass fields, refused not applied "
              "(criteria.c:134-141,321-327,385-392; L474-495)",
              any("group-index" in s for s in r["refusals"]) and r["effective"]["width"] == "300"
              and any("grouped" in s for s in r2["refusals"]) and r2["effective"]["width"] == "300")
```

## 3. Proof

### 3.1 Unmutated candidate

```
$ TMPDIR=$S/scratchroots python3 -I .../build/mado-mako.d3.py --selftest --scratch-root $S/scratchroots
MADO_MAKO_SELFTEST: checks=62 failed=0
rc = 0
```

The base tool (`$S/tool-base.py`, bytes of `tools/mado-mako.py`) printed `checks=59 failed=0`, rc 0, on the same tree:
the copy adds exactly 3 checks.

### 3.2 The three survivors, applied to the copy

R89MResidMut (`round-89/r1/R89MResidMut.md` §4) gives each survivor's site and semantic change but not its literal
replacement text; each mutation below is the minimal replacement at the named site implementing exactly that semantic.
Fidelity is checked two ways: (a) the candidate/mutant differential on the probe (below), and (b) the reconstructed mutant
still survives the **frozen round-89 case set** 141/141, exactly like the round-89 row.

| id | site in copy | replacement (old → new) | mutant sha256 |
|---|---|---|---|
| RS01-body-earlier-invalid-ignored | `:431` | `for key, value in (fields if ordered is None else ordered):` → `for key, value in (fields if ordered is None else [t for t in ordered if t[0] != "body~"] + [t for t in fields if t[0] == "body~"]):` (only the last `body~` occurrence is compiled) | `f923544a3e8da7324bf3aa58e3c39b21f28f72be0ad416ba32ec456efc49df4c` |
| RS05-quote-start-not-started | `:289-291` | in the `if char == '"':` branch, delete `started = True` (opening a quote no longer starts the token) | `ad5a794d52c3b33af09267ec748194cde4fd961a3d48812cb0ceadb076f477aa` |
| RS12-group-index-accepted | `:396` | `if key not in MODELLED_FIELDS:` → `if key not in MODELLED_FIELDS and key not in ("group-index", "grouped"):` (second-pass fields accepted) | `a13c82ac6afd67b2b314e811d0dbf5ed8b0bdf9b26b0cd54c4bb68be875dc2ce` |

Each anchor occurs exactly once (`anchor_count=1` asserted before writing; a mismatch aborts the driver). Mutants were
written only under `$S/mutants/`, never into the lane.

**Selftest kill (the required proof).** For every mutant, `--selftest` exits 1 with `checks=62 failed=1`, and the single
FAIL line is the new check for that survivor:

| mutant | selftest rc | FAIL line (stderr) |
|---|---|---|
| RS01 | 1 | `FAIL an earlier invalid body~ occurrence rejects the section though a later one is valid (criteria.c:209-212,241-246 apply every token; 344-350 regcomp per body~)` |
| RS05 | 1 | `FAIL a quote opens grouping but does not end the token, so a bare quoted key is refused (criteria.c:199-206,241-246; L510-516)` |
| RS12 | 1 | `FAIL group-index and grouped are second-pass fields, refused not applied (criteria.c:134-141,321-327,385-392; L474-495)` |

**Behavioural separator (the reproducing input).** Same config+argv through the candidate and the mutant CLI (`rc 0` both;
JSON stdout):

| probe input | candidate | mutant |
|---|---|---|
| config `[body~=a(b body~=x]` + `width=9`, argv `--body x` | `effective.width=300`, `refusals=["...:1: body~ 'a(b' is not a valid POSIX extended regex (regcomp refused it)"]`, `applied=[]` | `effective.width=9`, `refusals=[]`, `applied=["section:[body~=a(b body~=x]"]` |
| config `["x"]` + `width=9` | `width=300`, `refusals=["...:1: criteria token 'x' has no '=value' (bare tokens other than actionable/expiring are outside the model; spaces around '=' are refused)"]`, `applied=[]` | `width=9`, `refusals=[]`, `applied=["section:[\"x\"]"]` |
| config `[group-index=1]` + `width=9` | `width=300`, `refusals=["...:1: criteria field 'group-index' is outside the model (refused)"]`, `applied=[]` | `width=9`, `refusals=[]`, `applied=["section:[group-index=1]"]` |

### 3.3 The copy is behaviourally identical on the frozen round-89 cases (DRAFT)

`$S/fidelity.py` imports `quality/counters/c1-r89-mako-regex.py` read-only and calls its own
`score(text, base_text, cases, [], $S/fidelity-scratch, 0, declared=None, range_check=False)` (base tool bytes from
`git show af998dcc...:tools/mado-mako.py`, sha256 `c374d715...92237`; cases from
`round-89/controls/mako-cases-r89.json`, sha256 `5fdca7db...15672`; both pins asserted). The `verdict` field is not used —
only the per-case lines, as R89MResidMut did.

| bytes scored | n | correct | controls naive/globals/base/python-re | FAIL cases |
|---|---|---|---|---|
| candidate copy (added selftest lines) | 141 | **141** | 34 / 35 / 78 / 127 | none |
| reconstructed RS01 | 141 | **141** | 34 / 35 / 78 / 127 | none |
| reconstructed RS05 | 141 | **141** | 34 / 35 / 78 / 127 | none |
| reconstructed RS12 | 141 | **141** | 34 / 35 / 78 / 127 | none |

So the added checks change no resolution behaviour, and the three reconstructions are the same survivors R89MResidMut
found (each 141/141 on the frozen set).

## 4. Round-89 C1/C2 counters in draft

`--help` read first. Neither counter has `--draft-tool` / `--draft-check`, and neither has any DRAFT_* verdict or exit 3:
their measured paths take `--repo`/`--rev` only.

- `c1-r89-mako-regex.py`: `--candidate-file` is accepted only with `--controls-only` (controls receipt; the candidate
  itself is not run) and with `--selftest`.
- `c2-r89-survivor-kills.py`: `--tool-file` is "selftest only".

Draft runs against the copy (labelled DRAFT; not measurements; no receipt written under `round-90/receipts/`):

| run | output | rc |
|---|---|---|
| `c1-r89-mako-regex.py --selftest --candidate-file build/mado-mako.d3.py --scratch-root …` | `SELFTEST: passed=27/27` (includes "the tool under selftest carries the libc matcher" and "each python-re forgery anchor occurs once") | 0 |
| `c2-r89-survivor-kills.py --selftest --tool-file build/mado-mako.d3.py --scratch-root …` | `SELFTEST: passed=18/18` (the tool is correct on all four fixture cases; survivor fixtures kill as designed) | 0 |

No measured C1/C2 run is possible in draft with the round-89 counters: they have no tool-override on the scoring path.
A `grep` over `quality/counters/` finds no pin of the tool's selftest check count (`checks=59` has no reader), so the
59→62 change cannot move a C1/C2 predicate; the harm-watch re-run at the final revision remains the L1's.

## 5. Commands and exit codes

| # | command | rc |
|---|---|---|
| 1 | `curl … mako-1.11.0.tar.gz` + `sha256sum` + `tar -xzf` | 0 (sha256 `72d11d3f…7282` = pin) |
| 2 | `python3 -I $S/tool-base.py --selftest --scratch-root $S/scratchroots` | 0 (`checks=59 failed=0`) |
| 3 | `cp tools/mado-mako.py build/mado-mako.d3.py` + `sha256sum` (both `6b4bc409…673a98` before edits) | 0 |
| 4 | `diff -u tools/mado-mako.py build/mado-mako.d3.py` | 1 (files differ): 14 added, 0 removed |
| 5 | `python3 -I build/mado-mako.d3.py --selftest --scratch-root $S/scratchroots` | 0 (`checks=62 failed=0`) |
| 6 | `python3 -I $S/driver.py` (writes 3 mutants under `$S/mutants`, runs each `--selftest`, runs probes) | 0 |
| 7 | each mutant `--selftest` (inside 6) | 1 (`checks=62 failed=1`, the expected FAIL) |
| 8 | `c1-r89-mako-regex.py --selftest --candidate-file …` | 0 (27/27) |
| 9 | `c2-r89-survivor-kills.py --selftest --tool-file …` | 0 (18/18) |
| 10 | `python3 -I $S/fidelity.py` (4 × frozen 141 cases) | 0 (141/141 each; controls 34/35/78/127) |
| 11 | `git -C mado-shokunin rev-parse HEAD` / `status --porcelain` / `sha256sum tools/mado-mako.py` (read-only) | 0 (`tools/` unmodified) |

## 6. Dead steps

None — every command above succeeded on its first run. One non-error note: the evidence-collection `grep -c '^-[^-]'` over
the diff printed `0` and therefore exited 1 (expected: the diff has no removed lines).

## 7. Risks / notes for the L1

- The `group-index`/`grouped` check pins the tool's declared model stance (second-pass fields refused) even though
  upstream v1.11.0 parses them; if a later revision starts modelling grouping state, this check must change with it.
- The RS01 check pins "compile every body~ occurrence in application order"; a refactor that dedupes regex occurrences
  before compiling would (correctly) fail it.
- R89MResidMut prints no literal mutant replacement text, so the three mutants above are same-site reconstructions. They
  are validated as the same survivors by the frozen 141/141 result and by the candidate/mutant probe split; the exact
  round-89 harness bytes cannot be recovered from the report.
- Mutant selftest runs used the copy as the mutation base, so a mutant's `checks=62` proves the *added* check kills it,
  not one of the 59 pre-existing checks (each FAIL line is the new check by name).

## 8. Cleanup

Scratch `$S = /fast/scratch/hyaku/mado-r90/R90MExecMako` held the source tarball, probe fixtures, mutant copies and
counter scratch. Deletion is performed at seat exit with `rm -rf -- "$S"`; the resulting verification (`test -e` returns 1,
i.e. absent) is recorded below.

Verified after the seat's last command: `rm -rf -- /fast/scratch/hyaku/mado-r90/R90MExecMako` then
`test -e /fast/scratch/hyaku/mado-r90/R90MExecMako` → rc 1 (absent). Sibling seats' scratch directories were not touched.
