# w2 · CritC2Pin — registry source-row anchors, pins, S346 evdev chain, S350 receipt (round 48)

**Verdict on the as-submitted data: NO MISS.** All eleven rows S340–S350 survive the attack: every URL is a real
tag ref whose peeled commit equals the commit the row records, every pin digest equals the committed fetch copy and
(in eleven of eleven upstream-comparable cases) the upstream tag bytes, every anchor range is in-range and points at
the code it claims, and the S350 "own-work" receipt is a live capture that replays to its recorded digest. The frozen
counter `PRED-C2-r48` admits on a scratch mirror of BASE + the draft bytes:
`admitted=1/1 verdict=TARGET_MET`, exit 0 (`c2-score.txt`).

The attack did not come back empty: seven findings (F1–F7) below, none of them a predicate break on the submitted
bytes, and four probe-proven *predicate* holes that would admit rows the prose claims are stronger than.

## 1. Method and bounds

- Lane freeze `3e6c848a` (base `579f694b`); draft bytes read from `.ufo/waves/round-48/l1-draft/` and compared to the
  freeze commit (`rows-c2.md` sha256 `951b9f93…`, equal committed == worktree; fetch pin digests equal at `3e6c848a`).
- Scratch root `/fast/scratch/hyaku/mado-r48/CritC2Pin/`, `ulimit -f 2048` on every writer shell; **the lane tree is
  44 MB in scratch, largest file 952,083 B** (a tracked round-47 fixture brought in by the checkpoint, not an output);
  my largest own output is `row-audit.txt`, 7,610 B. Total 44 MB ≪ 2 GB. Scratch removed after the evidence copies.
- Replay tree: `git clone --shared --no-checkout` + `index.sparse` + cone sparse checkout, because the lane's base
  contains a 4,207,542 B and a 2,753,317 B tracked file and a normal checkout dies under the 1 MiB/file writer cap
  (`build-mirror.sh`). Mirror commit `0bc9d557` = base + draft entry, rows, README row, 13 fetch pins, receipt, generator.
- Counter run: `cd <mirror> && TMPDIR=<scratch>/replay python3 -I quality/counters/c2-r48-xkb-entry.py --repo <mirror> --rev HEAD`.
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`.
- Independent provenance: `git ls-remote` for tag peels; `curl` of each cited upstream file at its tag; the gitlab tag
  archive, unpacked read-only, to regenerate `rules/evdev`.
- No install, no package transaction, no lane Git/jj mutation, no commit/push/deploy. Two `pacman -Q` version *queries*
  (no transaction) and read-only `xkbcli compile-keymap --test/--kccgst` verbs only.

## 2. Per-row audit (S340–S350)

`upstream_tag` = independently fetched bytes at the cited tag hash-equal to the pin; `row_digest` = the row records
the pin's sha256; anchor verdict = every locator in range **and** the cited lines are the construct the row's
`teaches` cell names (checked by reading the pin). Rows carry **no quoted spans** (`quotes_in_row=0` for all eleven;
the entry's 18 quoted spans are checked by clause d and I spot-verified three, below).

| id | kind/tier | URL ref | ref→commit (peeled) | pin(s) B/lines | row_digest | upstream_tag | host_file | anchor | anchor verdict |
|---|---|---|---|---|---|---|---|---|---|
| S340 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | rules.c 74,868 / 2126 | ✓ | ✓ | – | 11 ranges (520-527, 528-535, 1986-1992, 1995-2025, 2028-2036, 1257-1279, 1297, 2045-2064, 1259, 2063, 530) | align: rules file find/read, pre/main/post, component check, %l/%v expand, "unmatched … ignored" block |
| S341 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | xkbcomp.c 7,920 / 240 | ✓ | ✓ | – | 157-166, 60-64, 157, 161 | align: `xkb_components_from_rules_names` failure → NULL; `CompileKeymap` failure |
| S342 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | include.c 17,209 / 511 | ✓ | ✓ | – | 333, 353-358, 498-506, 355, 501 | align: path loop, XKB-338 + `LogIncludePaths`, XKB-661 on a missing map |
| S343 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | context.c 16,074 / 593 | ✓ | ✓ | – | 243-338, 327-337, 503, 317, 336 | align: user paths first (`XDG_CONFIG_HOME/xkb`, `$HOME/.config/xkb`), legacy-root fallback, `log_level = XKB_LOG_LEVEL_ERROR` |
| S344 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | context-priv.c 5,898 / 226 | ✓ | ✓ | – | 192-217, 129-160, 202-217, 218, 208 | align: env-first defaults, layout/variant tie, `options == NULL` replacement |
| S345 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | meson_options.txt 2,411 / 103 | ✓ | ✓ | – | 32-59, 46 | align: default-rules evdev, model pc105, layout us, empty variant/options |
| S346 | code/A | `xkeyboard-config-2.48` (rules/rules.in) | cf8d1151… ✓ | evdev 31,520 / 748; rules.in 15,768 / 426; meson.build 3,356 / 95 | ✓ ×3 | evdev n/a (generated); rules.in ✓; meson.build ✓ | evdev ✓ (byte-equal) | 55-59, 529-586, 175, 570; rules.in *whole file*; meson.build:18-39 | align: `! model = keycodes … * = evdev`, `! option = symbols` block, `* * = pc+%l%(v)`, `compose:caps = +compose(caps)`, generator `custom_target` incl. the compat branch |
| S347 | code/A | `xkeyboard-config-2.48` (symbols/br) | cf8d1151… ✓ | br 19,592 / 369 | ✓ | ✓ | ✓ (byte-equal) | 47 | align: line 47 is `xkb_symbols "nodeadkeys" {`; file has 11 `xkb_symbols` maps (count verified) |
| S348 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | compile-keymap.c 23,033 / 632 | ✓ | ✓ | – | 585-587, 587, 521 | align: `XKB_CONTEXT_NO_DEFAULT_INCLUDES` / `NO_ENVIRONMENT_NAMES`, "ERROR: Couldn't create xkb keymap" + EXIT_FAILURE |
| S349 | code/A | `xkbcommon-1.13.2` | d1442aaa… ✓ | messages-codes.h 9,554 / 215 | ✓ | ✓ | – | 116 | align: 116 = `XKB_ERROR_INCLUDED_FILE_NOT_FOUND = 338`; 595 at :150, 661 at :162 (see F4) |
| S350 | own-work/A | none (own-work) | n/a | xkbcli receipt 14,270 / 354 | ✓ | n/a | n/a | *whole file* (0 locators) | live receipt, replayed (§4) |

Tag peels (`git ls-remote`): `xkbcommon-1.13.2^{}` = `d1442aaa6b635551182e83c3b55037f4c118c962`,
`xkeyboard-config-2.48^{}` = `cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0`; both equal the rows' `@ commit` cells.
All eleven upstream pins hash-equal the tag bytes (`upstream.txt`). Line counts above are `len(split("\n"))`, the
counter's own convention (one more than `wc -l`). Digest prefixes (`sha256:04dfd934…`) are not locators; the raw
audit lists them because my regex does not apply the counter's `sha256` skip.

## 3. S346 — is the package-generated evdev provenance chain sufficient?

**Yes in fact; no as committed evidence.** Positive chain, all independently reproduced:

1. Host `/usr/share/xkeyboard-config-2/rules/evdev` sha256 `0cc48ee1…` = committed pin **byte-equal**
   (`cmp`), package `xkeyboard-config 2.48-1` (pacman local db, read-only).
2. `rules/rules.in` and `rules/meson.build` pins are the tag's bytes (`1638977600…`, `1b4ab1d4…`), tag peels to
   `cf8d1151…` as the row records.
3. Regenerating from the gitlab tag tree with the recipe the row cites —
   `python3 -m rules.generator rules --ruleset evdev --version v2 --compat rules/rules.in` — yields sha256
   **`0cc48ee1…`, 747 lines, byte-equal to the pin and to the host file**. Without `--compat` it yields
   `ab627a66…`, 557 lines: the artifact is compat-dependent, and meson's top-level default is
   `compat-rules = true` (fetched from the tag; the cited `rules/meson.build:18-39` contains the conditional).

Gaps that make the chain non-self-verifying:

- the evdev pin carries **no URL of its own**; the row's URL addresses the *template* (`rules/rules.in`);
- the generator (`rules/generator/*.py`, 7 files), the loader registries (`rules/base.xml`, `rules/base.extras.xml`)
  and the compat mappings (`rules/compat/*.lst`, 3 files) are **not pinned and not cited**, yet the artifact is a
  function of all of them;
- the load-bearing `compat-rules = true` default lives in the top-level `meson_options.txt`, which no row cites;
- `PRED-C2-r48` never compares the pin to the host file and never regenerates, so the counter admits *any* bytes whose
  digest the row records. The chain I verified is out-of-band (network + host), not instrumented.

I did not treat this as a miss: the bytes are the host's installed package file, the host package is the artifact
libxkbcommon actually loads, and the tag reproduction is exact. It is an evidence-completeness defect (F1).

## 4. S350 — is the own-work receipt citable and live?

**Yes.** `.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt` (14,270 B, sha256 `ab5fa971…`) is committed at
the freeze, absent at BASE, and byte-equal to its fetch pin (`cmp`). Replayed under an isolated `HOME`/`XDG_CONFIG_HOME`:

- positive: `xkbcli compile-keymap --layout br --options compose:caps` → rc 0, 2,090 lines / 73,079 B, empty stderr,
  sha256 **`efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81`** — exactly the digest the receipt records;
- negatives: `--layout zz` rc **1** (XKB-338, XKB-661, XKB-769, XKB-822), `--variant nope` rc **1** (XKB-661/769/822),
  `--options nope:nope` rc **0** with `[XKB-595] Unrecognized RMLVO option "nope:nope" was ignored`;
- the row's five wrong-name classes (layout, variant, rules fail; option, model compile, option with XKB-595) all
  appear in the receipt's labelled windows and match the live run.

Two defects, neither affecting the predicate: the receipt's **line 1 names its generator as
`.ufo/waves/round-48/receipts/make-xkb-receipt.sh`, which does not exist**; the generator is at
`.ufo/waves/round-48/tools/make-xkb-receipt.sh` (147 lines, `42a50468…`) and the *row* cites `tools/` correctly (F3).
The generator also writes next to itself while claiming to write "next to this script" into `receipts/`.

## 5. sources-census on the scratch registry

Mirror = base registry + S340–S350 (11 rows inserted after S339) + the entry + the README row: **exit 0**, one
`ok` line plus only pre-existing findings — **17 W04** and **1 W01 (S277)**; **zero findings for S340–S350**.

Classification of the two codes the task names:

- **W04** = *same URL across different scopes* — warning only, never changes lane status (census header and
  `W04-does-not-fail-validation` selftest). The 17 hits are pre-existing (S030, S042, S045, S097, S119–S121, S303,
  S307, S317, S318, S320, S321, S324, S326, S327, S332): each is a second row reusing a URL under a new scope.
  **None of the eleven new rows triggers it** — every new row has a distinct upstream path, and S346/S347 share only
  the gitlab host, not the URL.
- **E04** = *same URL within the same scope, neither row rejected and no `supersedes S###`* — an error. **Zero in the
  whole registry**, including the new rows.
- Malformed (E01 `NF!=13`), bad id (E02), duplicate id (E03), kind/tier/status/opened/recheck (E05–E09), community at
  A (E10), row outside `## Registry` (E12): **zero**. The 11 ids are `S340…S350`, unique and contiguous after S339.
- **E11 sequencing (the one real registry risk):** the rows' `used-by` is `corpus/knowledge/xkb-keymap-compile-r48.md`.
  Committing the rows **without** that entry yields **E11 × 11 and exit 1** (`census-rows-no-entry.txt`, branch
  `377c5be0`); the pre-data freeze is clean only because the rows still live in `l1-draft/` (the committed registry has
  zero `S34x` rows). Rows, entry and README row must land in **one** data commit.

## 6. Findings

| # | severity | finding | evidence |
|---|---|---|---|
| F1 | medium | S346 chain is not self-verifying: no URL on the evdev pin; generator, `rules/base*.xml`, `rules/compat/*.lst` unpinned; `compat-rules=true` (load-bearing: 747 vs 557 lines) uncited; the counter never checks pin-vs-host or regeneration | `s346-provenance.txt` |
| F2 | medium | `on-release` recheck cannot fire on a same-version package rebuild (2.48-1→2.48-2) that changes `rules/evdev` (S346), nor on a host `input.conf` change that invalidates S350's "this host's names" claim; the receipt already records `input.conf` sha256 `3769c92a…`, so the trigger exists but is not wired | entry:15, receipt:47-56 |
| F3 | low | S350 receipt's self-declared generator path `.ufo/waves/round-48/receipts/make-xkb-receipt.sh` does not exist at REV; the generator is under `tools/` | `s350-replay.txt` |
| F4 | low | anchor completeness: S349 teaches XKB-338/595/661 but locates only `:116` (595 at :150, 661 at :162); S347 locates one map (`:47`) while the teaches asserts "eleven" (true: 11 maps) | `row-audit.txt` |
| F5 | low | dead pin in the trust set: `.ufo/waves/round-48/fetch/xkbcommon-meson.build` (51,635 B) is cited by no row or entry (harmless: clause d refuses quotes from uncited pins) | entry pin scan |
| F6 | low (prose) | entry recheck line says "re-pull the **nine** upstream code pins"; S340–S349 carry **10** code rows and **11** upstream pins (8 libxkbcommon files + `rules.in` + `meson.build` + `symbols/br`), 12 cited fetch pins incl. the generated evdev, 13 files in `fetch/` | entry:15 |
| F7 | info | rows alone → E11 × 11 (see §5); rows+entry+README → clean | `census-*.txt` |

## 7. Predicate probes (probe-proven holes, `mutants.txt`)

Each probe mutates one cell of the mirror's registry, commits in the scratch clone, and re-scores the frozen counter.

| probe | mutation | counter result |
|---|---|---|
| dead-locator `2417c18b` | S340 anchor gains `nosuchfile-zzz.c:1-2` | **TARGET_MET** — an unresolvable locator token is silently skipped (`resolve_pin→None → continue`), so a dead locator costs nothing |
| fake-commit-ref `d1abfdf3` | S340 URL ref → `0123456789abcdef0123456789abcdef01234567` (nonexistent) | **TARGET_MET** — 40-hex refs are accepted by shape only (declared residual, now demonstrated) |
| whole-file-anchor `3555be11` | S347 anchor `:47` → `whole file` (0 locators) | **TARGET_MET** — "whole file" satisfies clause c with zero located ranges |
| control-foreign-pin `dad61c80` | S347 anchor → `xkbcommon-rules.c:47` | **TARGET_MISSED** — clause c refuses `range_other_pin`; the anchor check is not vacuous |
| receipt-drift `8942614e` | append one editorial line to `receipts/xkbcli-compile-keymap-r48.txt` | **TARGET_MET** — the receipts/ file can drift from the fetch pin; S350's "byte copy of" claim is prose-only |

All five revs exist only in the scratch clone; none touches the lane. As-submitted data is unaffected by F6's holes —
they matter for a future row that leans on a dead locator or a bare "whole file".

## 8. What I did not verify (residuals)

- I did not re-run the full 20-control C1 set or any C1 fixture (other seats own that); no C1 datapoint here.
- Upstream verification used the network (tag files + tag archive); the counter itself fetches nothing, so this
  out-of-band check is not reproducible from the freeze alone — that is F1's point.
- I did not verify the *text* of the entry's 18 quoted spans one by one; clause d passed and I spot-verified three
  (`No index provided: match only if single layout` at rules.c:1259, `expanded_value->matched = true;` at :1297,
  `xkb_symbols "nodeadkeys" {` at br:47).
- The receipt embeds `# taken:` and `uname`, so byte-for-byte regeneration is impossible by construction; replay
  equality of the *adjudicating* values (digest, rc, diagnostics) is what I checked.
- The receipt contains absolute `/home/vgpnk/...` paths (input.conf greps and `sha256sum`); this matches the lane's
  existing practice (1,478 files under `.ufo/waves/round-4*` contain the same prefix), so I record it as observation,
  not a guard breach, and did not copy any host listing into this report beyond those two config lines' hashes.

## 9. Evidence inventory (`.ufo/waves/round-48/w2/CritC2Pin/`)

| file | sha256 | shows |
|---|---|---|
| `pins.txt` | `b4198d26…` | all 14 fetch pins: sha256 + bytes |
| `upstream.txt` | `5c4ef882…` | tag-fetched bytes for the 11 upstream-comparable pins |
| `tags.txt` | `1807cbe8…` | tag → peeled commit for both tags |
| `c2-score.txt` | `df3fcdbf…` | frozen counter on mirror `0bc9d557`: clauses a–r, `admitted=1/1 TARGET_MET`, exit 0 |
| `row-audit.txt` | `a2bb764a…` | per-row URL/ref/commit/pin-digest/anchor table |
| `s346-provenance.txt` | `0a712ff6…` | host=pin=regenerated `0cc48ee1…`; compat 747 lines vs nocompat 557; `compat-rules` default |
| `s350-replay.txt` | `f2f36195…` | replay digest `efd487a3…`, rc set, receipt/fetch byte-equality, generator path defect |
| `census-validate2.txt` | `f5a3f89f…` | census exit 0, 17 W04 + 1 W01, no new-row findings |
| `census-rows-no-entry.txt` | `e0e83cbf…` | rows without entry → E11 × 11, exit 1 |
| `mutants.txt` | `ac26bc1f…` | five probe results (four predicate holes + one control) |
| `neg-zz.txt`, `neg-var.txt`, `neg-opt.txt` | see dir | raw diagnostic blocks for the three labelled negatives |
| `build-mirror.sh` | `735359c4…` | sparse-checkout mirror recipe (why: 4.2 MB tracked fixture vs 1 MiB cap) |
| `probes.sh` | `0493a0b2…` | probe recipe |
