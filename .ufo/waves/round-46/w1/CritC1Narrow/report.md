# CritC1Narrow — narrowing attack on PRED-C1-r46 (round 46, w1)

Seat: `CritC1Narrow` (attack, C1 only). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, claims frozen at
`.ufo/waves/round-46/registration.md` (freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base `b22ea56b`).

## 0. Verdict

**PRED-C1-r46 is MET by 18 tools that each break exactly one rule of its own contract.** Each of the 18 was scored
by the frozen counter at three nonces — `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present
verdict=TARGET_MET` in every run (54 runs, `counter-runs.txt`) — while its output differs from the pinned reference
on a hand-built input that the contract names explicitly. Nothing in the reference, the fixtures file or the counter
was modified; the holes are in what the corpus *pins*, not in what the contract *says*.

The three that matter most, in order:

1. **A `source =` line is counted as unmodelled** (`P02`) — the tool then prints `NOT_COMPARED` (exit 5) on this
   host's real top-level config. Contract `:19` — "It is a join, not a blame"; contract `:48-50` lists the only
   keys that are relevant. Demonstrated on the real file (`host-config-demo.txt`):
   ```
   reference                  rc=0 ... unsupported=0 verdict=OK
   P02-source-unsupported     rc=5 ... unsupported=18 verdict=NOT_COMPARED
   ```
   (`~/.config/hypr/hyprland.conf` holds 18 lines matching `^[[:space:]]*source` — count only, no content.)
2. **A config that is not valid UTF-8 crashes the tool** (`P08`) — contract `:37` "decoded as UTF-8 with errors
   replaced"; one stray byte (a latin-1 comment) gives exit 1, empty stdout, a traceback on stderr.
3. **`kb_options = a, b` is compared after normalisation** (`P04`) — contract `:66` "Every other value is the RHS
   string". Against a dump that prints `a,b` the reference reports `differ=options verdict=DIFFER` (exit 1) and the
   variant reports `differ=- verdict=AGREE` (exit 0): the difference the tool exists to surface is masked. With a dump
   that keeps the space the same variant reports a *false* DIFFER — it is wrong in both directions.

Blast radius: C1 (operability, capability acquisition) is the axis; the object under attack is C1's own contract,
not the entry. The C2 entry and the round-45 data are untouched (separability in §4).

## 1. Method

- Reference read at `.ufo/waves/round-46/l1-draft/mado-devices.py` (sha256 `b229efd0…`, the counter's `MODEL_SHA256`
  and `FIXTURES_SHA256 = 027ed508…` both verified before use).
- For each docstring rule a one-anchor textual variant was cut from the reference (patch asserted to apply exactly
  once), then triaged against the counter's own clause-f and clause-g code (`triage.py`, which imports the frozen
  counter and replaces only `sandbox()` with a direct exec; four nonces: 4646, 12345, 987654, 271828).
- Every survivor was then scored by the **frozen counter itself**, under bubblewrap, on its own scratch clone of
  `8c5434c6` with the variant committed as `tools/mado-devices.py`:
  `python3 -I quality/counters/c1-r46-devices.py --repo <clone> --rev HEAD --work <scratch>/w --nonce {4646,12345,987654}`.
  Result file `counter-runs.txt` (54/54 `TARGET_MET`; every variant 3/3).
- For each survivor a catching fixture was built and the reference run on it: `proposed-fixtures.json` (15 entries;
  `expect` computed by the pinned reference, and the variant's output checked to differ). `genprop.py` produced it.
- Tooling: none installed this round (`python3` 3.14.8, `git`, `bwrap` already present). No package transaction.

## 2. The 18 holes

Contract locators are lines of the reference docstring; code locators are lines of the same file.

| # | contract rule | code | variant | what the variant does | MET |
|---|---|---|---|---|---|
| 1 | `:38` continuation joins "the next raw line" — repeatedly, until no backslash | `:185` `while line.endswith` | `P01-single-continuation` | joins only **one** continuation; a 3-line `kb_options` list keeps a trailing `\` → counted unsupported → `NOT_COMPARED` | 3/3 |
| 2 | `:19`, `:48-50` non-relevant lines are ignored (join, not blame) | `:273` | `P02-source-unsupported` | counts a `source = …` line as unsupported → `NOT_COMPARED` on real configs | 3/3 |
| 3 | `:39-40` a stripped line starting with `#` may be a directive | `:246`, `:248` | `P03-indented-directive` | directive recognised only in column 0; an indented `# hyprlang …` is not counted → `OK` instead of `NOT_COMPARED` | 3/3 |
| 4 | `:66` every other value is the RHS string | `:239` | `P04-comma-space-trim` | normalises spaces around commas in `kb_*` values → false `AGREE` | 3/3 |
| 5 | `:51` `input:kb_X` sets the global "a bracket name does not change that" | `:277` | `P05-bracket-input-ignored` | drops the line when a bracket name was cut → false default layout | 3/3 |
| 6 | `:82` `reported=<F|?>` | `:402` | `P07-nonfinite-reported` | prints `%.2f` for a non-finite `scrollFactor` → `reported=nan` instead of `?` | 3/3 |
| 7 | `:37` configs "decoded as UTF-8 with errors replaced" | `:552` | `P08-strict-utf8-config` | strict decode → traceback, exit 1, empty stdout | 3/3 |
| 8 | `:75` `scrollFactor` AGREEs when "a finite number (not a boolean)" | `:356` | `P09-int-not-number` | accepts only `float`; an integer factor in the dump → false `DIFFER` | 3/3 |
| 9 | `:31` "a FIFO or any non-regular file is unreadable" | `:130` `S_ISREG` | `P10-regular-check-dropped` | reads a FIFO as an empty config → `OK` on no input at all | 3/3 |
| 10 | `:31` "larger than 1048576 bytes is too_large" (exactly 1048576 is not) | `:142` | `P11-size-boundary` | `>=` → a 1 MiB config is rejected | 3/3 |
| 11 | `:28` "`--devices V` exactly once" | `:167` | `P12-devices-twice` | later `--devices` silently re-targets instead of `SETUP usage` | 3/3 |
| 12 | `:37` "the category stack starts empty in each file" | `:243` | `P13-stack-shared` | one stack for all files (the current device stays per file): a block left open in file 1 turns file 2's next key into a device key with no current device → counted unsupported → `NOT_COMPARED` instead of `OK` | 3/3 |
| 13 | `:63-66` special prefix `[+-]?(inf|nan|0x)`, any case | `:106` | `P15-case-sensitive-special` | case-sensitive → `NaN`/`0X10` read as unset, not unsupported | 3/3 |
| 14 | `:71` VIRTUAL when the name **starts with** `hl-virtual-keyboard` | `:373` | `P16-virtual-contains` | `in` instead of `startswith` → false VIRTUAL hides a real keymap failure | 3/3 |
| 15 | `:44` "a line ending in `{` pushes its text before the `{`" | `:261` | `P19-brace-needs-space` | requires `" {"`; `input{` opens nothing → whole block silently dropped | 3/3 |
| 16 | `:39` stripped "of spaces, tabs and carriage returns" before the comment test | `:246` | `P21-no-cr-strip` | a leading CR hides a directive → `OK` instead of `NOT_COMPARED` | 3/3 |
| 17 | `:43` "stripped of ASCII whitespace" (a BOM is not ASCII whitespace) | `:246` | `P22-bom-stripped` | strips a leading BOM → a BOM config's first key applies where the contract ignores it | 3/3 |
| 18 | `:77` block MATCHED by a name in "any top-level list of the dump" | `:334` | `P23-switch-name-ignored` | only keyboards/mice/tablets/touch → a `switches` name is `NO_SUCH_DEVICE` → false `STALE_BLOCK` | 3/3 |

Two further variants were built and are **correctly MISSED**, which is worth recording because it bounds the
corpus's real coverage: `P06` (`kb_file=set` for `[[EMPTY]]`) is caught by clause g in 3 of 4 triage nonces
(`gen=141/150`, `146/150`, `144/150`), `P14` (underflow rule `:66` dropped) in 4 of 4; `P18` (`=` without spaces)
and `P20` (hash-pair resume) are caught by fixtures (`device-empty-rhs`, `isspace-trim`; `comment-triple-hash`).
So the corpus is not vacuous — it is narrow exactly where the generator's grammar and the fixture list stop:
raw bytes, argv shapes, non-regular files, size boundaries, cross-file stack, line-start characters, and
`kb_*` values that are not bare tokens.

## 3. Catching fixtures (15, all pass on the pinned reference)

`proposed-fixtures.json` in this directory is the candidate list in the frozen fixture schema; each entry's `expect`
was produced by running the pinned reference, and each was verified to make its variant fail (`genprop.py` output:
`catches=True` for all 15). Labels:

`continuation-three-lines` (0), `source-line-not-unsupported` (0), `directive-indented` (5),
`kb-options-space-after-comma` (0), `bracket-input-sets-global` (0), `mouse-nan-reported-token` (1),
`mouse-int-scrollfactor` (0), `config-exactly-max-bytes` (0), `stack-reset-per-file` (0),
`mouse-special-uppercase` (5), `virtual-prefix-not-substring` (1), `block-opener-no-space` (0),
`leading-cr-directive` (5), `config-bom-before-first-key` (1), `matched-switch` (0).

**Three holes cannot be expressed in the frozen fixture schema at all** — clause f is structurally blind to them:

| hole | why the schema cannot say it | smallest harness addition |
|---|---|---|
| `P08` raw-byte config | `run_fixture` writes each config with `open(cp, "w", newline="", encoding="utf-8")` from a `str`, so no invalid UTF-8 can be authored | a `config_bytes` list, mirroring the existing `dump_bytes` + `latin-1` path already used for dumps |
| `P10` FIFO config | `configs: null` already means "a directory"; there is no non-regular-file case | a `"configs": "fifo"` sentinel (`os.mkfifo`) |
| `P12` duplicate `--devices` | arguments are assembled by the harness; the only argv fixture is `configs: "usage"` | an optional `argv` override per fixture |
| (`P11` exact size) | expressible only as a 1 MiB literal, which would bloat the sha-pinned file | a `"@MAX"` sentinel next to `"@BIG"` |

Clause g does not cover any of the 18 either: `gen_case` emits no `source`, no `input[`, no `input{`, no
`=`-without-spaces, no 3-line continuation, no indented directive, no BOM, no leading CR, no non-device key inside a
`device` block, no `switches` name, no integer or non-finite `scrollFactor`, no non-UTF-8 bytes, no FIFO, no size
boundary, no duplicate `--devices`, and no block left open at end of file.

## 4. Impacted axes

- **C1 operability — direct.** The claim is "a new read-only tool … joins the input/device lines … with one
  `hyprctl devices -j` dump". PRED-C1-r46 accepts a tool that (a) refuses to compare on any real `hyprland.conf`
  (18 `source` lines here), (b) crashes on a non-UTF-8 byte, (c) reports `OK` after reading nothing from a FIFO,
  and (d) reports `AGREE` where the dump and the config differ only by a space after a comma. Those are wrong
  verdicts, not style: three of them are *false AGREE/OK*, the direction that matters for an operability tool.
- **C2 coverage — not touched.** No entry, registry row, lesson or pin was read for a claim; my evidence is the
  counter, the fixtures file and the reference only, so the separability statement in the registration still holds.
- **Closure D1 / round-45 data — untouched.** I did not run the round-45 w2 falsification; nothing here changes
  those counters or their receipts.

## 5. Smallest safe correction

The reference needs no change: it passes all 15 proposed fixtures and every divergence above is the variant's.
Under the registration's kill rule ("A hole wave `w1` finds before any data commit may re-register as v2 with a new
freeze and new controls") the correction is corpus-only:

1. Re-freeze as **v2** and add the 15 fixtures of `proposed-fixtures.json` to
   `quality/counters/c1-r46-fixtures.json`, then update `FIXTURES_SHA256` (90 → 105).
2. Add the four harness shapes of §3 (`config_bytes`, `"fifo"`, `argv`, `"@MAX"`) so `P08`, `P10`, `P11`, `P12`
   become expressible; without them clause f cannot reach those semantics at any fixture count.
3. Register the 18 variants as controls (V21–V38, patches in `triage.py`) that must all be **MISSED**, in the same
   shape as V01–V20. Controls V01–V20 were built against the *monitors* semantics; none of the 18 above is covered.
4. Optional, cheaper than 18 controls and stronger for unforeseen nonces: extend `gen_case` with the same grammar
   (`source`, `input[`, `input{`, `k=v`, 3-line continuation, indented directive, BOM/CR prefixes, non-device block
   keys, `switches` names, integer/NaN factors) so clause g pins the class, not the instances.

### 5.1 Status against the in-flight v2 draft (read-only, another seat's file)

`.ufo/waves/round-46/v2/gen-fixtures.py` (111 cases, 20 of them `v2-*`) already pins **two** of the 18:
`P02` (`v2-source-top-ignored`, `v2-source-in-block`) and `P15` (`v2-hex-fraction` uses `0X`, `v2-inf-clamps-high`
uses `Infinity`). The other **16 remain open** there, checked label by label: `P01` (only 2-line and final-line
continuations exist), `P03` (`v2-vt-before-directive` pins that a VT is *not* stripped — a different direction; an
indented directive is `2` spaces and stays unpinned), `P04`, `P05`, `P07`, `P08`, `P09`, `P10`, `P11`, `P12`,
`P13`, `P16`, `P19`, `P21`, `P22`, `P23`. Its fixture schema is the same one, so `P08`/`P10`/`P12` are still
inexpressible there, and its expectations come from the same model-oracle design, so a contract error shared by
reference and tool stays invisible (the registration's declared residual).

If the round cannot re-freeze, the honest alternative is to weaken C1's claim text — but that is a scope cut the
registration's kill rule exists to avoid.

## 6. Residuals (what this seat did not establish)

- I attacked per-rule semantics only. I did not test environment detection, clause i's hidden paths beyond use, or
  the isolation of `--work`; those are other seats' ground.
- `P21`/`P22`/`P16`/`P23` are contract-pinning holes with no trigger on *this* host today: `grep -c $'\xef\xbb\xbf'`
  and `grep -c $'\r'` are 0 for all 13 `~/.config/hypr/*.conf` files; the live `hyprctl devices -j` (shape only, read
  allowed by the seat spec) has 10 keyboards, 1 of which starts with the virtual prefix and 0 of which merely contains
  it, and the `switches` list carries no named entry (top-level lists: keyboards, mice, switches, tablets, touch).
  They are real only as unconstrained semantics, and `P22` is the one where the variant is arguably closer to
  Hyprland than the contract.
- Scratch deviation: `/fast/scratch/hyaku/mado-r46/CritC1Narrow` peaked at 6.0 GB (18 variant clones + 54 counter
  work dirs + the triage's per-case directories), above the 2 GB seat guidance; it was removed in full at the end and
  everything cited here was copied into this directory first.
- The 4-nonce triage used the counter's functions minus bubblewrap; the 3-nonce confirmation used the frozen counter
  as shipped. Where they disagree, only the latter counts, and they did not disagree.
- Scope bound on my "correctly MISSED" note (§2): that `P06`/`P14` are caught says the corpus pins the *reference's*
  `read_float` rules, not that those rules match Hyprland. Seat `ConnCrossClaim-3` reports (pin-cited, not verified by
  me) that libstdc++ `std::stof` accepts `inf`/`nan`/hex where the contract calls them unsupported; if that holds it
  is a contract error shared by reference and tool - the residual the registration declares - and it is orthogonal to
  the 18 narrowing holes above, which hold whatever the model says.
- Same class may apply to the round-45 counters (`c1-r45-monitors-v2.py`); I did not test that (routed, not mine).
- Routed, not my evidence: seat `SentTool-3` reports clause-r and AF_UNIX holes in the same harness (its
  `w1/SentTool/findings.md` F1/F2). I did not verify them; they are a different axis from this seat's. They do
  interact with §5: the `config_bytes` / `"fifo"` / `argv` / `"@MAX"` fixture shapes run inside the same `sandbox()`,
  so a v2 that adds them must carry those sandbox and `hidden_paths()` fixes at the same time, or the added shapes
  inherit the same unsound isolation.

## 7. Receipts (this directory)

- `counter-runs.txt` — 54 lines of `PRED-C1-r46: … verdict=TARGET_MET rev=… seeds=…`, 3 nonces × 18 variants.
- `proposed-fixtures.json` — 15 catching fixtures with reference-computed `expect`.
- `host-config-demo.txt` — reference vs `P02` on the host's real `hyprland.conf` with a synthetic dump.
- `triage.py`, `probe.py`, `probe2.py`, `genprop.py`, `demo_host.py`, `runreal.sh` — the exact variant patches,
  the in-process triage, the file/argv probes and the fixture builder (paths inside them point at the scratch dir,
  which is deleted; patches are in `triage.py:VARIANTS`).
