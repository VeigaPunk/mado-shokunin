# Read-only pinned evidence commands

Executed via Python subprocess.run(argv, capture_output=True, text=True), concurrently in a ThreadPoolExecutor. No counter or harness executed. Line projections below are Python enumerate(stdout.splitlines(), 1), selected inclusive ranges; not additional shell commands.

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/registration-v2.md
exit=0 sha256=44d7bc31366d775e011b35c94f4824056b7093c673c25d772d3360e0d8459f9a

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/registration-v2-errata.md
exit=0 sha256=800c6540da0ec257a600fd33227307876b70be1981baf12ec1cb19d891ad54e2

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:quality/counters/c1-r56-autoreload-entry.py
exit=0 sha256=2b2ef41b3329edde1b30a88ab13f9430b3522d052186b4eb00ebb154a0301fea

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:quality/counters/c3-r56-used-by.py
exit=0 sha256=68b34e3c7c1d61e7f5f3da36a0f8ab36ebe3c54b1b756cb18c740e0aa7c1635b

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:quality/r56_ctl_c2.py
exit=0 sha256=080d772037608a9c2fe2ee033a463d681575e0a220df1f8e5bc8c1489062923e

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:QUALITY.md
exit=128 sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/knowledge/hyprland-config-autoreload-r56.md
exit=0 sha256=4f5f9863786cb7df8772cc313f178dcea35f6d726224a3a27e4c28ab40c7788f

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2CritC1Forge.md
exit=0 sha256=602d7300b775b77da613cc382d8654f46300a29142b9de1e77269549b6349ff2

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2CritC2Cheat.md
exit=0 sha256=a96f8024cc1215b05822ed6e0b1147e1109aa433dfa548bce172b61461ecf189

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2RevUsedByB.md
exit=0 sha256=20ae6409a07b24f08c469a074cabc08bd3cd62c5ea92ec00f499fc1268727040

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2CritScopeFix.md
exit=0 sha256=5dcf95d747e4e3d78cde79f9c475745919ca4cf4caa6d6abae8561d52c9def6f

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2MutC2ToolA.md
exit=0 sha256=858d9dc19e90cf213ee23c2cd62a4d58b9feb23650b5af03708fe73cdcd16a1b

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2MutC2ToolB.md
exit=0 sha256=c7d977d79eef81d91c179ef95e96e19aa55e34e56a1f9f91ccb121d10c171557

$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/QUALITY.md
exit=0 sha256=1a5c4cc900986f05144aaa41125f1cc6baf5ca8bdbaba8bc150f1dfa1887e2ee

The QUALITY.md request exited 128 (no root QUALITY.md at the named revision); discovery located corpus/QUALITY.md and that request succeeded.

## .ufo/waves/round-56/registration-v2.md
```text
80: ## What v2 does not repair (declared limits, carried into the report)
81: 
82: C1: `TARGET_MET` proves quote identity, registry binding, anchor scope and lexical grounding; a forged proposition that shares a
83: quote identifier, keeps to the quote's numbers and does not echo the quote passes (R56RevC1Contract §2); entailment is the wave-2
84: sentence-to-pin audit (reported, not counted) and the non-author closure. C2: a tool that fingerprints the tree and replays the
85: committed table scores 18/18 committed and fails the hold-out only (the hold-out is the guard); a tool that reads the lane's
86: revealed hold-out by absolute path passes (non-adversarial harness). C3: `CITE` reads literal tokens only (ranges such as
87: `S175–S177` hide `S176`, five pairs; entries without a `source:` line are invisible to `dangling`, 20 entries); the
88: allowlist is two readers' judgment, frozen, disclosed and open to the non-author closure; the 41 pairs that remain are filled and were judged
89: reliance (or leaning reliance) by BOTH readers (R56RevC3Contract `REAL`/`BORD`, R56CritCiteDef `U`/`M-U`); six carry an `M-U` or `BORD` hedge.
```

## .ufo/waves/round-56/registration-v2-errata.md
```text
5: **E12 — `lost` is defined over the 65 base-missing pairs.** `registration-v2.md` §C3-v2 says `lost` counts pairs of PAIRS(base) that left
6: PAIRS(rev), "its sorted `S###|path` lines ... have sha256 `c3.base_pairs_sha256`". The frozen hash `630007b0…` was computed over the 65
7: pairs the v1 `missing` count found at the base revision, not over all 381 pairs of PAIRS(base) (`frozen-tables-v2.json` c3 carries
8: `base_pair_count: 65`). The first run of the integrated counter failed closed on the hash ("base pairs hash differs from the frozen
9: value"), which is the registered behaviour; the counter was then aligned to the frozen value: `lost` = base-missing pairs (entry path not in
10: used-by at the base) that are no longer in PAIRS(rev). Deleting the 65 citations is therefore caught; deleting a citation of one of the other
11: 316 pairs is not (it cannot reduce `missing`). The integration counter is `quality/counters/c3-r56-used-by.py` (`base_pairs`).
```

## quality/counters/c1-r56-autoreload-entry.py
```text
265: def scope_covers(anchor, basename, line, nlines=None):
266:     """True when after some `<basename>:` the comma-separated N / N-M locator list holds a range with line, and (registration-v2 E3)
267:     every locator of that basename is bounded above by nlines (the pin's line count) when nlines is given."""
268:     key = basename + ":"
269:     pos = anchor.find(key)
270:     covered = False
```

## quality/counters/c3-r56-used-by.py
```text
239: def base_pairs(repo, work, t):
240:     try:
241:         B = Repo(repo, t["base_rev"], work)
242:     except SetupError:
243:         raise SetupError("base revision objects are absent: fail closed")
244:     _, _, _, pl0 = pair_data(B)
245:     _, ub0, _, _ = pair_data(B)
246:     pl = {k: v for k, v in pl0.items() if k[1] not in ub0[k[0]]}   # registration-v2 E12: the base `missing` pairs
247:     lines = sorted("%s|%s" % (s.decode("ascii"), p.decode("utf-8", "replace")) for s, p in pl)
248:     h = hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()
249:     if h != t["base_pairs_sha256"]:
250:         raise SetupError("base pairs hash differs from the frozen value")
251:     return set(pl)
```

## quality/r56_ctl_c2.py
```text
6: Exports (git archive | tar -x, symlinks preserved) the tool, fixtures/c2, the hold-out, ctl/ and frozen-tables.json at REV
7: into a scratch directory under --work, runs the tool and the four ctl stubs on every fixture as child processes
8: (`python3 -I <program> <args>`, scrubbed environment; the tool under test runs STAGED: `{FX}` = `<work>/stage/<id>` holding only the fixture's
9: `tree/`, cwd = an empty directory, the tool copied to its own directory, inside `bwrap` when available), compares stdout bytes and exit status with
10: expected.out / expected.rc, recomputes both tree commitments and prints exactly one line:
11: 
12:     MADO_R56_C2: rev=<rev> fixtures=<a>/18 holdout=<b>/8 holdout_commit=<ok|bad|absent> controls=<k>/4 verdict=<...>
13: 
14: Exit 0 on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on stderr, nothing on stdout).
15: The harness reads git objects at REV only (never the working tree); its only writes are under --work (removed before exit).
```

## corpus/QUALITY.md
```text
592: **107.** **A registry row cited by a knowledge entry's evidence row has a unique anchor that names the row's upstream file, covers the quoted line, and stays within that file's length (extends 77 and 97).**
593: 
594: Scope. Every evidence row of a knowledge entry, any row class: a table row, outside fenced code and HTML comments, whose third cell is a registry id `S` followed by three or more digits. A row of that shape whose fourth cell is not exactly `<file>:<N>` (one decimal number; no range, no list, no second file) is a violation `reason=malformed-pin`. It is never skipped.
595: 
596: For each such row, let R be the registry row whose first cell is that id in `corpus/SOURCES.md` at the checked revision:
597: 
598: (1) Uniqueness. R must be the only row with that id. Zero rows reads `reason=no-registry-row`; two or more read `reason=dup-id`, whatever their content.
599: (2) NAME. The last path component of the last `http(s)://` token in R's source cell (cell 2), with trailing `).,;` removed. If NAME contains `#` or `?`, the row reads `reason=no-name` and must be read by hand.
600: (3) Bounded occurrence. An occurrence of `NAME:` in R's anchor cell (cell 6) counts only when the character before it is absent or is not in `[A-Za-z0-9_]`. A hyphen or a slash before it is allowed; `OldConfigWatcher.cpp:` does not contain an occurrence of `ConfigWatcher.cpp:`.
601: (4) Locator list. Right after `NAME:` comes a comma-separated list of locators. Each locator is `N` or `N-M`, decimal, with N at least 1. One optional space may follow a comma. The list continues only while the next item starts with a digit. A locator with M less than N denotes no line and covers nothing.
602: (5) Cover. Some locator of some counted occurrence has N <= L <= M, where L is the quoted line. A single `N` means N = L.
603: (6) Length. If the anchor cell names its pin as `pin <path>`, the blob at that path at the checked revision is read, and every locator of the counted occurrence must have max(N, M) <= the blob's line count (the number of `\n`-separated pieces). A locator past the end of the file reads `reason=past-eof` for every row of that pin. An anchor with no named pin reads `eof=unchecked` in the output.
604: 
605: Output: one line per evidence row, `ANCHOR_COVER: row=<id> sid=<S###> line=<N> name=<NAME> locators=<list|none> eof=checked|unchecked verdict=OK|MISS [reason=...]`, then `CHECK107: rows=<n> covered=<k> miss=<m> verdict=OK|FAIL`. The requirement is `miss=0` with `rows>0`. Exit 0 on OK, 1 on FAIL, 2 on setup error with empty stdout. The check reads git objects at `<rev>` only and writes only under `--work`.
606: 
607: Shown able to fail, on the committed round-55 entry `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` at `63f48dc1`: the K rows K14 and K17 fail the round-56 counter's `scope_covers` (`.ufo/waves/round-56/receipts/scope-replay-r55.txt`; seat replay `w2/R56W2CritScopeFix/receipts/replay-r55.out`), and the round-56 draft checker over all row classes reports rows=32 covered=25 miss=7 on that entry (`w2/R56W2CritScopeFix/receipts/draft-r55.out`). Each registry mutant named in `R56W2CritScopeFix/receipts/` (widen past EOF, narrow below a K row, drop the name, reversed range, identifier-prefixed name, malformed pin cell, duplicate id) fails under this text on the row or rows it names; the EOF, boundary, reversed-range, malformed-pin and duplicate-id clauses are the ones the round-56 draft lacked.
608: 
609: Fix path (registry rows are append-only, CORPUS rule 2): a supersession row with a new id and a widened anchor, then a re-cite in the entry. Each change is logged in the round lesson.
610: 
611: Declared limits.
```

## corpus/knowledge/hyprland-config-autoreload-r56.md
```text
121: | E01 | The replace call on this line replaces the first byte (the tilde tested one line earlier) with the HOME string; absolutePath contains no user lookup, so a ~user prefix becomes HOME followed directly by user (the no-lookup half is a negative read of the function, not shown by the quoted line). | S393 | Hyprland-MiscFunctions.cpp:66 | `value.replace(0, 1, std::string(ENVHOME));` |
122: | E02 | The return value of inotify_add_watch is stored unchecked in the .wd field of the SInotifyWatch emplaced into m_watches; the function never tests it, so a failed add (for example a missing path) still leaves an entry whose .wd is -1 and that no later event can match. | S383 | Hyprland-ConfigWatcher.cpp:60 | `.wd   = inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask),` |
123: | E03 | This line copies WD->file, the path stored in the watch matched by wd, into the SConfigWatchEvent that m_watchCallback receives, so the callback is handed the stored watch path and the kernel's event name is ignored. | S392 | Hyprland-ConfigWatcher.cpp:106 | `.file = WD->file,` |
124: | E04 | This line passes COMMAND and VALUE to the legacy config manager's parseKeyword, the call a runtime hyprctl keyword request reaches through dispatchKeyword; the route exists only when the config manager is the legacy one (dispatchKeyword otherwise returns a keyword-cannot-work message). | S394 | Hyprland-HyprCtl.cpp:1190 | `std::string retval = mgr->parseKeyword(COMMAND, VALUE);` |
125: | E05 | The constructor calls resetHLConfig on this line; that function clears m_configPaths and re-adds the main path, and reload() calls the same function. | S395 | Hyprland-legacy-ConfigManager.cpp:630 | `resetHLConfig();` |
126: | E06 | On this line m_configCurrentPath becomes the nested file's own path before that file is parsed; relative source lines in it then resolve against that file's directory through absolutePath. | S395 | Hyprland-legacy-ConfigManager.cpp:1838 | `m_configCurrentPath          = value;` |
127: | E07 | On this line the legacy manager's getConfigPaths returns m_configPaths, the vector that resetHLConfig clears and handleSource appends to; ConfigWatcher reaches it through Config::mgr(), whose interface declaration is not in the pins. | S395 | Hyprland-legacy-ConfigManager.cpp:2134 | `return m_configPaths;` |
128: | E08 | The enum declares REFRESH_CONFIG_WATCHER as bit 8, the flag K02 attaches to misc:disable_autoreload and K15 tests in the refresher. | S391 | Hyprland-PropRefresher.hpp:18 | `REFRESH_CONFIG_WATCHER     = (1 << 8),` |
129: | E09 | REFRESH_ALL is the maximum of the enum's underlying type (uint16_t, declared on an earlier line of the same header), so every one of its 16 bits is set, including bit 8. | S391 | Hyprland-PropRefresher.hpp:21 | `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),` |
```

## .ufo/waves/round-56/w2/R56W2CritC1Forge.md
```text
79: **1. How many of the 33 honest propositions a lexical rewrite could falsify while keeping `content=33/33`:** 33 of 33
80: (B2). Each proposition is replaced by its negation; the counter's content leg stays 33/33 and the verdict is TARGET_MET
81: with `missed=none`. The five constraints the counter applies to a proposition, all met by a negation:
82: (a) at least 40 characters for K rows and 20 for H rows; (b) unique across the entry; (c) shares at least one identifier
83: of four or more characters with the frozen quote; (d) every digit run is in the quote, in {0,1,2,3}, or is the line of a K row
84: of the same pin; (e) when the quote has 30+ characters, the quote is not a substring of the proposition.
85: 
86: **2. Is TARGET_MET evidence of a sourced entry:** no. The counter never reads the meaning of a proposition, so the
87: content axis (does the sentence say what the pinned line says) is untested by the counter and by the harness, whose
88: controls are the same lexical class. The counter's green proves: the frozen quote is on the pinned line; each row's
89: source id maps to a registry row with the pinned URL suffix, the rev token, status `mined`, tier A/B, date 2026-10-28 and
90: the entry in `used-by`; the anchor range covers the quoted line; the source line lists the cited ids within the first 15
91: lines; and the proposition passes the five constraints above. It does not prove any proposition is true. The lane's own
92: declared limit (claims-frozen-v2 §C1) states this for a proposition that shares a quote identifier and keeps to the quote's
93: numbers; B2, T5 and B3 are exactly that class, and they are not the only ones that pass (see below).
```

## .ufo/waves/round-56/w2/R56W2CritC2Cheat.md
```text
19: | id | channel (what the tool reads) | bwrap | no bwrap |
20: |---|---|---|---|
21: | (a) | `<display-root>/expected.out` (registered control shape) | 0/18, 0/8 MISSED | 0/18, 0/8 MISSED |
22: | (b) | walk `..` upward from its path, cwd, display root, config (+ one-level glob of each ancestor) to the export's `expected.out` | 0/18, 0/8 MISSED | **18/18, 8/8 TARGET_MET** |
23: | (c) | fingerprint the staged tree + args, replay the 18 **committed** entries (embedded) | 18/18, **0/8** MISSED | 18/18, 0/8 MISSED |
24: | (d) | read the lane working tree at `/home/vgpnk/…/fixtures/c2{,-holdout}` at run time, fingerprint lookup | 0/18, 0/8 MISSED | **18/18, 8/8 TARGET_MET** |
25: | (d2) | same via `git -C <lane> cat-file blob 28fc86…:path` (read-only git) | 0/18, 0/8 MISSED | **18/18, 8/8 TARGET_MET** |
26: | (e) | `/`, `/proc/*/cmdline` `--work` paths, crawl of those and `/fast/scratch` + `/tmp` for the same fixture id with matching args | 0/18, 0/8 MISSED | **18/18, 8/8 TARGET_MET** (first hit inside sibling seat `R56W2MutC2ToolA/work/h/c2-export-…`) |
27: | (f) | partial: nine features only (usage, header, primary line, relative top-level and nested `source =`, `disable_autoreload`, DONE) | 3/18, 1/8 MISSED | 3/18, 1/8 MISSED |
28: | (g) | **embedded lookup of all 26 fixtures** (committed + revealed hold-out), fingerprint + args key; no grammar, no disk or lane read | **18/18, 8/8, controls 4/4 TARGET_MET** | 18/18, 8/8 TARGET_MET |
29: 
30: Controls were 4/4 in every run (the four ctl stubs are fixed bytes at the rev and are not the tool under test). Receipts: `receipts/<cheat>-bwrap.{out,err}` and `receipts/<cheat>-nobwrap.{out,err}`; cheat sources in `cheats/`; breadcrumb logs (the per-fixture hit list) in `receipts/crumbs-*.txt`.
42: - The E6 requirement "expected bytes live only in the harness process memory" is not met by the implementation: the harness's `pipe_tar` export writes every `expected.out`/`expected.rc` (committed and hold-out) to `<work>/c2-export-*` on disk for the whole run; bwrap is the only thing keeping them from the tool.
43: 
44: **Not closed by any layout (declared or new):**
45: - (c): committed-table replay passes 18/18 and fails the hold-out only; this is the declared `lookup-committed` class (v2 "What v2 does not repair") and the registration's stated guard.
46: - (g): the embedded all-26 lookup passes everything under bwrap. Not in the declared list. The v2 guard ("the hold-out is the guard") holds only while the hold-out is sealed; the integration revealed it (`fixtures/c2-holdout` at rev, commitment still binds it), so the guard is gone and a lookup needs no runtime access to reach 26/26.
```

## .ufo/waves/round-56/w2/R56W2RevUsedByB.md
```text
70: ## 2. Per-pair labels — the 24 ALLOWLISTED pairs (23 AGREE name-only; 1 borderline disagreement)
71: 
72: | pair | citing line (≤25 words) | verdict |
73: |------|--------------------------|---------|
74: | S005 / output-colour-boundaries-r14 | "Neither the S005 README's earlier commit nor the later S040 governance commit is substituted…" | NAME-ONLY (disclaims; entry's source is S048). AGREE |
75: | S007 / input-debugging-boundaries-r15 | "S051 supersedes queued S007's loose composite tools description and mutable anchor." | NAME-ONLY (supersession; S007 queued, used-by '—'; S051 carries the entry). AGREE |
76: | S030 / hyprland-config-era-r12 | "…read every S030 citation in this entry … as **S017**"; S017.used-by ⊇ this entry | NAME-ONLY (rejected row, redirected; reliance recorded on S017). AGREE |
77: | S040 / output-colour-boundaries-r14 | "do not apply S040's wayland-protocols governance as its authority"; "**S040 governance makes … stable.** Reject:" | NAME-ONLY (refutes/disclaims; S047/S048 carry it). AGREE |
78: | S043 / input-debugging-boundaries-r15 | "S052 adds the core input contract, distinct from S043's registry scope." | NAME-ONLY (contrast; S052 carries it). AGREE |
79: | S044 / config-drift-r12 | "S015 stays a historical omarchy-method source; round-13 S044 cites the actual gate-maintenance rule." | **BORDERLINE — leaning RELIANCE** (see F1). Disagree-leaning |
97: | S359 / hyprland-dispatcher-dispatch-r51 | "held (cited, not re-registered, registry rows only): … S359, the wiki Binds page at the 0.56.2-era revision" | NAME-ONLY (the entry never reads the Binds page — not in its pin manifest; S359's used-by = the r50 entry that does). AGREE |
98: 
99: **Count: 23/24 AGREE (name-only). 1 borderline leaning reliance (S044) — see F1.**
```

## .ufo/waves/round-56/w2/R56W2CritScopeFix.md
```text
54: | mutant | S383 / entry change | counter (full legs) | draft (K rows / total) | reading |
55: |---|---|---|---|---|
56: | base | none | TARGET_MET, scope=30/30 | K all OK; miss=6 (E01,E03–E07) | baseline |
57: | v1 widen past EOF | anchor `…,105-200` (pin = 112 lines) | scope=20/30 missed scope:K03…K12, TARGET_MISSED | K all OK; miss=5 | draft lacks EOF clause (D1) |
58: | v2 narrow below K12 | `…,69,104` | scope=29/30 missed scope:K12 | K12 MISS | both fail |
59: | v3 narrow below K08 | `54-55` | scope=29/30 missed scope:K08 | K08 MISS | both fail |
60: | v4 drop basename | `lines 33-34,…,105` | scope=20/30 (K03…K12) | K03…K12 no-name | both fail |
61: | v5 reversed range | `…,105-104` | scope=29/30 missed scope:K12 | K12 OK | reversed range: checkers disagree (D3) |
62: | v6 identifier prefix | `OldConfigWatcher.cpp:…` | TARGET_MET, scope=30/30 | K03…K12 no-name | counter lacks boundary (D2) |
63: | v7 E rows as `file:N-N` | E01,E03,E04,E05,E06,E07 cell 4 → `file:N-N` | TARGET_MET (K-only) | rows=33 covered=33 miss=0 OK | draft skips malformed pins (D4) |
64: | v8 duplicate S383 | first S383 narrowed to `1-2`, second (original) appended | TARGET_MISSED: source_cell K03…K12, scope K03…K12, new_rows 7/8 | K rows OK; miss=6 (E only) | draft last-wins on duplicate id (D5) |
```

## .ufo/waves/round-56/w2/R56W2MutC2ToolA.md
```text
18: | one-line mutants generated and run (none skipped) | 105 |
19: | killed by the frozen claim predicate (`TARGET_MET` not printed) | 62 (59.0%) |
20: | killed by the full oracle (claim predicate + `--selftest`) | 77 (73.3%) |
21: | provably equivalent (no observable behaviour change) | 9 |
22: | claim survivors that are not equivalent | **34** |
23: | full-oracle survivors that are not equivalent (no lane test catches them) | **19** |
24: 
25: Equivalent-adjusted kill rate: 64.6% (claim predicate), 80.2% (full oracle).
26: 
27: The attack lands. The frozen predicate `TARGET_MET` is satisfied by 34 mutants that break a normative rule of registration-v2 §C2. Of those, 19 also pass the tool's own `--selftest`. Every one of the 34 has a killing fixture, verified through the harness's staged bwrap layout (section 4).
```

## .ufo/waves/round-56/w2/R56W2MutC2ToolB.md
```text
7: ## 1. Verdict
8: 
9: - The wave-1 oracle kills **82 of 117** one-line mutants (70.1%); **82 of 107** non-equivalent mutants (76.6%).
10: - **25 non-equivalent behaviour changes survive** it. Each one has a verified killing input (23 as staged fixtures through the unchanged harness path; 2 — m75, m76 — only with a root-level config path the staged layout cannot express).
11: - 10 survivors are equivalent on Python 3.14.8, each with an argument (mutants.md §3.1).
12: - No pristine-tool defect was found by the mutation exercise. What it found is a coverage gap in the C2 predicate and one undeclared divergence (D2 below).
13: - Claim effect: the C2 predicate `TARGET_MET` shows the tool is operable on the 26 inputs; it does not show the watch list is right on the inputs listed in §3.2. The claim should be worded as an operability predicate, not as a discrimination test.
68: **D2 — weakens: undeclared divergence (silent exception mapping).**
69: Input: a `source` line `source = ` + `*/`×1100 + `x` (or any pattern with ~1000 wildcard components). Pristine output: `MADO_WATCH: ERROR via=… source=… reason=nomatch`, rc 0. The `RecursionError` from `glob` is swallowed in `expand()` and reported as an ordinary no-match. The E8 declared-divergence list does not mention it. Whether glibc `glob(3)` (Hyprland's call) returns a no-match for such a pattern is NOT verified here: I did not run glibc. Severity: **weakens**; add the divergence or report the exception differently.
70: 
71: **D3 — weakens: fixture commitment blocks the cheap fix.** The 20 candidate fixtures cannot be added to `fixtures/c2` without changing `c2.fixture_commit_sha256` (and the holdout commitment), which needs a new versioned freeze (v3) before scoring. Severity: **weakens** (process).
72: 
73: **D4 — weakens: the random differential probe does not support equivalence claims.** `difftest.py` reported `distinguishable=False` for m07 and m105, both killed by one fixture (K02, K15). The vocabulary lacks `**` and `=` in comments. Severity: **weakens** (any "no difference found by fuzzing" wording would be wrong). Not used as evidence.
74: 
75: **D5 — cosmetic / risk: runtime.** K18 and K19 (262k entries) take ~5–9 s per tool run here; the harness `TIMEOUT` is 30 s. On a loaded host a timeout reads as rc None, which would score the pristine as failing. Severity: **cosmetic** at present.
```
