# ReopenFoot: round 23 wave 2 (falsify), C2 source re-open, foot rows S140-S149 and S152

Seat: MadoR23.ReopenFoot (leaf; read-only on the lane; this file is the only lane write).
Lane tip checked: `2f1134f38930fc8b067d2d7f5bba126338faabdd` (commit dated 2026-10-22T08:49:48-03:00, "round-23: C3 PROVINCE refinement accounts for every tracked lane tool").
All fetches were made 2026-10-22.

## 1. Bounds and inputs

- Rows: `corpus/SOURCES.md` at the tip. Blob sha256 `ed4c561f0c35ecf8c9da6468ddeccd5df98d99d538f7df0aa3d248769f69f1dc`, 136,607 B. Each of S140-S149 and S152 occurs once (tip lines 152-161 and 164), with 11 cells, `mined`, opened `2026-10-22`, recheck `on-release`, used-by `corpus/knowledge/terminal-trees-r23.md`.
- Anchor and quote source: `.ufo/waves/round-23/w1/reports/SrcFoot.md`. It is **not committed at the tip**: `git show 2f1134f...:.ufo/waves/round-23/w1/reports/SrcFoot.md` returns "exists on disk, but not in 2f1134f". I read the working-tree copy, sha256 `ad1dd025818d4b8185e2da39f372fadad1d464d9e9b2049f74cb86bd81b3c57c`, 42,089 B.
- Access: ordinary HTTPS GET (curl 8.23.0) and git protocol (git 2.56.0: `ls-remote`, `clone`). No headless browser, no challenge page, no captcha, no bypass. Every response was a direct 200, 303 or 404 with the expected bytes.
- Raw downloads and clones were written only under `/fast/scratch/hyaku/mado-r23/w2/ReopenFoot/`.
- Installs and upgrades: none. Tools used were already present: git 2.56.0, curl 8.23.0, python3 3.14.8.

## 2. Verdicts

"Assigned" = re-open the URL, recompute the pinned sha256 and byte count, check the anchor line ranges, and check the located quote in the bytes. "Teaches" = the row's own prose where the same pinned bytes bear on it; this is beyond the assigned check.

| Row | Assigned checks | Teaches / scope | Verdict |
|---|---|---|---|
| S140 | confirmed | ok | **confirmed** (3 SrcFoot supporting quotes need marker removal, see D4) |
| S141 | confirmed | scope "complete set of signals foot handles" and teaches "the only signals are SIGUSR1 and SIGUSR2" are contradicted (F1) | **confirmed on assigned checks; mismatch (detail) on teaches/scope** |
| S142 | confirmed | scope "only reacts to the theme-switch signals" is contradicted by footclient SIGINT/SIGTERM handling (F1) | **confirmed on assigned checks; mismatch (detail) on scope** |
| S143 | confirmed | ok | **confirmed** |
| S144 | confirmed (includes `meson.build:393`, fetched as an extra) | ok (no uncommented option line in the template) | **confirmed** |
| S145 | confirmed | ok (first-hit search, include recursion, explicit `conf_path` bypass all verified in code) | **confirmed** (2 SrcFoot supporting quotes defective, D1 and D2; see F5) |
| S146 | confirmed | teaches "SIGUSR1 and SIGUSR2 are the only handled signals" is contradicted by `main.c:664-665` in its own pinned file (F1) | **confirmed on assigned checks; mismatch (detail) on teaches** |
| S147 | confirmed (anchors and quote) | precision: `--config` is passed only when the instance was started with `--config` (F3); `BIND_ACTION_SPAWN_TERMINAL` is not located in `terminal.c` (F4) | **confirmed; precision notes** |
| S148 | confirmed (anchors and quote) | teaches "clones it per client" is conditional (F2) | **confirmed on assigned checks; mismatch (detail) on teaches** |
| S149 | confirmed (repo, commit ancestry, blob) | ok; wiki routes behave as the row says | **confirmed** |
| S152 | confirmed | ok | **confirmed** |

Totals: 11 of 11 rows confirmed on the assigned checks. 0 unopened. 0 pin mismatches. 0 rows in which an anchor range fails to contain its cited item. Four rows carry a teaches/scope sentence the pinned bytes contradict (S141, S142, S146, S148). S147 needs a precision edit.

## 3. Per-row evidence (assigned checks)

Every URL in the tip rows matched the fetched URL exactly (programmatic check, 11 of 11). Every pin in the tip row's anchor cell matched the recomputed sha256 and byte count (11 of 11).

| Row | Re-opened URL (HTTP, bytes) | sha256 (computed = row) | Anchor lines checked | Located quote (SrcFoot table) |
|---|---|---|---|---|
| S140 | `https://codeberg.org/dnkl/foot/raw/tag/1.28.0/doc/foot.ini.5.scd` (200, 76,756) | `030014641676a18efff238a8954b5fb69e34dc9c80782236d3e85a824c11bc2b` | :9-33: `# DESCRIPTION` at 7. :110-121: `*include*` at 110, under `# SECTION: main` at 34. :390-393: inside the `*initial-color-theme*` entry (384-395). All present. | :14-16 "foot will search for a configuration file in the following locations, in this order:" found in window 14-16 |
| S141 | `.../doc/foot.1.scd` (200, 22,717) | `ad7d60aea563ae2f62290a83131e976948ad4384be1e4616872bab18a78f0c84` | :27-35 (`# OPTIONS` at 25). :103-135 (`--server` at 103). :700-712 (`# Signals` at 700). :624-629 (`# EXIT STATUS` at 624). All present. | :111-112 "It also saves upstart time..." found in window 111-112 |
| S142 | `.../doc/footclient.1.scd` (200, 6,929) | `a214ddafc671aa0b1f485c4aad5cb3f407fa31c871d24c2d39187c13d6eaa023` | :23-100 (`# OPTIONS` at 23). :200-213 (`# Signals` at 200). Present. | :200-202 found at line 202 |
| S143 | `.../README.md` (200, 24,450) | `874e192a7f322421e6c762c18dadd47239f7a5366bc47b966d12b516fd6f626d` | :78-86 (`## Configuration` at 78). Present. | :78-84 found in window (line-wrapped 80-81) |
| S144 | `.../foot.ini` (200, 9,158); extra `.../meson.build` (200, 14,114) | `1f3d6fa3f17292870d68bc39a2833d66300e0581684940ed0abc5e7e060763b5` | :1-5 header. :110 `[colors-dark]`. :198 `[key-bindings]`. `meson.build:393` is the exact `install_data('foot.ini', ...)` line. Present. | :3 found at line 3 |
| S145 | `.../config.c` (200, 136,321) | `bc8c134edc51e1225a583603888e3989d4f4a6acc794738bd03cd86418c3a0e1` | :421-473 (function spans 421-476, see N1). :432-434. :449-461. :909-945 (include branch spans 909-947, see N1). :921. :926-927. :944. :3501-3520. :3712-3723. All present. | :432-434 found at line 432 |
| S146 | `.../main.c` (200, 23,528) | `d50034046894cde411f7c7d4fcbd8d9c65277e2cee97ea945e163b5a673217c2` | :539-540 (`config_load(` call). :55-74 (`fdm_sigusr`). :675-676 (SIGUSR1/SIGUSR2 registration). :681-687 (SIG_IGN block). All present. | :683-684 found at line 683 |
| S147 | `.../terminal.c` (200, 148,115) | `27b3dfbf4cf953884632b1b798c876922fa2f11aaac68213ef1a42d4fb419544` | :3816-3831 (`term_spawn_new`). exe :3821 (`argv[argc++] = term->foot_exe;`). `--config` :3823. conf_path :3824. All present. | :3821-3825 found at line 3824 |
| S148 | `.../server.c` (200, 18,715) | `bf5c2993a6c3f998b6666b667424f032062892dba19d560c4aa7f23c7e2e5631` | :559-600 (`server_init` at 559). :369-392. :371. :392-393 (argument line; the `term_init(` head is at 391, see N2). Present. | :371 found at line 371 |
| S149 | `https://codeberg.org/dnkl/foot.wiki.git`: bare clone; commit `2475351ace3c8a618a3f2b8a7a486e987d125e07` is a commit and an ancestor of HEAD; `Home.md` blob 32,739 B | `78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7` | :1011-1015: `### How do I reload the configuration?` at 1011; the answer is at 1013-1015. Present. | "There is no way to dynamically reload the configuration." spans 1014-1015 (wrapped); found in window |
| S152 | `.../CHANGELOG.md` (200, 141,338) | `3d6c7d68224763e71f238234fbb50379ca7d2c6a66eb33ba66ae04c7334661f5` | :73 `## 1.28.0`. :110-118 `### Removed` at 110; the "replaced by" text is at 116-118. Present. | :73 found at line 73 |

Quote coverage: all 50 located quotes in SrcFoot.md (11 table rows plus 39 bullet quotes) were extracted mechanically from the SrcFoot text, not retyped. 44 match verbatim (11 table plus 33 bullets). 3 match only after emphasis markers are removed (D4). 3 are defective (D1-D3). Receipt: `srcfoot-quote-match.json`.

## 4. Identity checks beyond the assigned set

- `git ls-remote https://codeberg.org/dnkl/foot.git 'refs/tags/1.28.0*'` returned `3d97bba53072ff90433ff75617f4a8e034529b57 refs/tags/1.28.0` (tag object) and `ab33c9a19d626f8d0ac0bd1adfdba21946ada948 refs/tags/1.28.0^{}` (commit). This matches "tag 1.28.0 = commit ab33c9a...".
- `git cat-file -p 3d97bba...` in the tag clone: tagger epoch 1788346974 +0200, which is 2026-09-02T11:02:54Z. This matches S140's "released 2026-09-02".
- `git clone -q --depth 1 --branch 1.28.0 https://codeberg.org/dnkl/foot.git`: HEAD is `ab33c9a...`. git printed `warning: refs/tags/1.28.0 3d97bba... is not a commit!`. This is a client message about the annotated tag object; HEAD resolved to the commit. Harmless here.
- Blob equality: for each of the 11 raw files, SHA-1 of `blob <len>\0<bytes>` equals the tree blob at HEAD of the tag clone (11 of 11 EQUAL). So the raw/tag bytes are the tag tree bytes.
- Tag archive `https://codeberg.org/dnkl/foot/archive/1.28.0.tar.gz`: 200, 1,201,047 B, sha256 `4296be402b5684d049534598e69db92b918f92beac9dab76b585207045f0b037`. This reproduces SrcFoot's pin.
- Wiki: `2475351...` is a commit dated 2025-12-28T12:19:14+01:00 and an ancestor of the wiki HEAD. Plain GETs: `.../foot.wiki/raw/commit/2475351.../Home.md` gives 303 to `.../foot/wiki/raw/commit/...`, which gives 404 (11 B) when followed. `.../foot.wiki/raw/branch/master/Home.md` gives the same 404. `.../foot.wiki/src/commit/2475351.../Home.md` gives 303 to `.../wiki/?action=_pages`, which gives 200 (31,112 B). This matches S149's "raw and src routes return 404 / redirect to the page index".
- Documented reload routes: grep for `reload|inotify|SIGHUP|config file changed` over `doc/`, `README.md` and `foot.ini` returned no match. S140's "no documented reload route" holds.

## 5. Findings (by severity)

**F1 (teaches/scope, contradicted by pinned bytes; S141, S142, S146). Also landed in the C2 note and in SrcFoot F4.**
- S141 scope: "the complete set of signals foot handles". S141 teaches: "the only signals are SIGUSR1 and SIGUSR2, which switch colour theme".
- S146 teaches: "SIGUSR1 and SIGUSR2 are the only handled signals and they switch the colour theme".
- S142 scope: "only reacts to the theme-switch signals".
- Landed note `corpus/knowledge/terminal-trees-r23.md` at tip line 31 repeats it: "the only handled signals (SIGUSR1, SIGUSR2) switch the colour theme". SrcFoot F4 says "the only two signals foot handles".
- Counter-evidence:
  - `main.c:664-665` (S146's own pinned file): `fdm_signal_add(fdm, SIGINT, &fdm_sigint, ...)` and `fdm_signal_add(fdm, SIGTERM, &fdm_sigint, ...)`.
  - `reaper.c:41` (tag tree, not one of the 11 raw files): `fdm_signal_add(fdm, SIGCHLD, &fdm_reap, reaper)`.
  - `terminal.c:1988-1990` (S147's pinned file): `struct sigaction action = {.sa_handler = &sig_alarm}; ... sigaction(SIGALRM, &action, NULL);`, on a shutdown path.
  - `client.c:554-562` (footclient; tag tree): `sigint_handler` for SIGINT and SIGTERM, `sigusr_handler` for SIGUSR1/2. `client.c:577-578`: `if (aborted) break;`.
- What the bytes do support: SIGUSR1/SIGUSR2 are the two documented theme-switch signals (`doc/foot.1.scd:700-705`, `doc/footclient.1.scd:200-205`). SIGHUP and SIGPIPE are set to SIG_IGN (`main.c:681-687`). No reload route exists. The reload conclusion is unaffected; the "only" sentences are not.
- Minimal correction for the L1 to consider: "SIGUSR1/SIGUSR2 switch the colour theme; SIGHUP and SIGPIPE are ignored (main.c:681-687); foot also installs handlers for SIGINT/SIGTERM (main.c:664-665), SIGCHLD (reaper.c:41) and, on a shutdown path, SIGALRM (terminal.c:1988-1990)."

**F2 (teaches, S148): "clones it per client" is conditional.**
- `server.c:365-367`: `need_to_clone_conf = tll_length(overrides) > 0 || cdata.hold != server->conf->hold_at_exit;`
- `server.c:369-371`: the clone happens only inside that branch.
- `server.c:391-392`: `term_init(conf != NULL ? conf : server->conf, ...)`.
- Without overrides or a differing hold setting, the client uses `server->conf` directly. Neither path re-reads `foot.ini`, so the reload conclusion holds.

**F3 (precision, S147 teaches; SrcFoot F4): `--config` is passed only in some cases.**
- `config.c:3509-3510` sets `.conf_path = (conf_path ? xstrdup(conf_path) : NULL)` from the argument. `main.c:265-266` sets `conf_path = optarg` for `-c`. `terminal.c:3822-3824` passes `--config` only when `conf_path != NULL`.
- Started without `--config`, spawn-terminal passes no `--config`, and the new process runs the same search (`config.c:421-476`).
- The row is true for instances started with `--config`. It should say so.

**F4 (location, S147): `BIND_ACTION_SPAWN_TERMINAL` is not in `terminal.c`.** A grep of the downloaded `terminal.c` found no match. The symbol is in `key-binding.h:28` (enum), `config.c:168` (`"spawn-terminal"`), `config.c:3382` (default Ctrl+Shift+n), and the dispatch at `input.c:210-211` (`term_spawn_new(term)`). The claim is true, but the anchor does not locate it.

**F5 (SrcFoot.md supporting quotes; SOURCES rows unaffected).**
- D1 (S145, `config.c:909-911`): "Absolute path to configuration file to import." is not in `config.c`. The tag-tree grep finds it only at `doc/foot.ini.5.scd:111`, a man-page line.
- D2 (S145, `config.c:3501-3506`): SrcFoot quotes `config_load(struct config *conf, char *conf_path,`. The bytes at line 3501 read `config_load(struct config *conf, const char *conf_path,`.
- D3 (S148, `server.c:392-393`): the quote starts with `term_init(`, but that token is on line 391. Line 392 is the argument line.
- D4 (S140, `doc/foot.ini.5.scd:17-18`, `19-20`, `22-23`): SrcFoot's quotes are emphasis-stripped. The bytes carry scdoc `*...*` markers and line wraps. They match after marker removal (checked).
- D5 (SrcFoot.md, row 7): the located quote contains a double pipe, which splits that markdown table row into 8 cells. The quote itself matches `main.c:683`.
- D6: SrcFoot.md is not committed at the lane tip (see section 1).

**F6 (precision, S146 teaches and SrcFoot F4: "config_load is called once from main.c").** The user's `foot.ini` is parsed once in every build; `main.c:539-540` is the only runtime call. `config.c:4009` also calls `config_load("/dev/null")`, inside `UNITTEST` at `config.c:4001`. `macros.h:189-192` makes UNITTEST a startup constructor only under `_DEBUG` with constructor support; otherwise it is an unused function. So a `_DEBUG` build runs that call before `main()`, on `/dev/null`. This is read from source; nothing was built.

**Cosmetic (no verdict change).**
- N1: S145 `open_config :421-473`. The function spans 421-476; the cited range ends at `free(xdg_config_dirs_copy);` (473). The include branch spans 909-947; the cited range ends at 945.
- N2: S148 `term_init(...) :392-393`. The call head is at 391; the argument is at 392.
- N3: S147 `bound to BIND_ACTION_SPAWN_TERMINAL` is unlocated; see F4.

## 6. Residual risk and verification gaps

- No foot binary was built or run. Runtime statements are code-reading only. The `_DEBUG` reading in F6 was not compiled.
- The C2 counter (`python3 -I .ufo/waves/round-23/c2/count.py`) was not run; that is the L1's run. My checks cover URL, pins, anchors, quotes and identity, plus the row cells as printed. Row shape was observed (11 cells each), not counter-validated.
- The landed note was read only for line 31 and for its source list. Its other rows and rows S150-S151 (ghostty) and the kitty rows were not evaluated.
- Teaches checks cover only sentences where the pinned bytes bear on them. Other row prose was not audited line by line.
- The wiki `Home.md` is not pinned to a release, as S149 states. Its raw route 404 is a redirect-chain result; I followed the 303 and recorded the end state.
- SrcFoot.md was read at sha256 `ad1dd025...`. If the working copy changes, the located-quote receipt is stale.

## 7. Commands and receipts

Commands (paths are the lane and scratch paths named in section 1):
- Read-only lane git: `git -C <lane> cat-file -t 2f1134f...`; `git -C <lane> log -1 --format=%H%n%cI%n%s 2f1134f...`; `git -C <lane> show 2f1134f...:corpus/SOURCES.md`; `git -C <lane> show 2f1134f...:corpus/knowledge/terminal-trees-r23.md`; `git -C <lane> show 2f1134f...:.ufo/waves/round-23/w1/reports/SrcFoot.md` (absent).
- Raw fetch, 11 paths: `curl -sS --max-time 180 -o <scratch>/foot-1.28.0/<path> -w '%{http_code} %{size_download} %{content_type}' https://codeberg.org/dnkl/foot/raw/tag/1.28.0/<path>`.
- Tag identity: `git ls-remote https://codeberg.org/dnkl/foot.git 'refs/tags/1.28.0*'`; `git clone -q --depth 1 --branch 1.28.0 https://codeberg.org/dnkl/foot.git <scratch>/foot-clone-1.28.0`; `git -C <clone> cat-file -p 3d97bba...`; `git -C <clone> ls-tree HEAD -- <path>`.
- Archive: `curl -sSL --max-time 300 -o <scratch>/foot-1.28.0.tar.gz https://codeberg.org/dnkl/foot/archive/1.28.0.tar.gz`.
- Wiki: `git clone -q --bare https://codeberg.org/dnkl/foot.wiki.git <scratch>/wiki/foot.wiki.git`; `git -C <wiki> cat-file -t 2475351...`; `git -C <wiki> merge-base --is-ancestor 2475351... HEAD`; `git -C <wiki> show 2475351...:Home.md`; `curl` probes of `.../raw/commit/2475351.../Home.md`, `.../raw/branch/master/Home.md` and `.../src/commit/2475351.../Home.md`, with and without `-L`.
- Hashing and matching: Python `hashlib` (sha256, sha1 blob) and `re` over the bytes. Read-only; no file was modified.
- Greps (`_grep` tool) over the tag clone for signal dispositions, `BIND_ACTION_SPAWN_TERMINAL`, `conf_path`, `config_load(`, `need_to_clone_conf`, and `define UNITTEST`.

Receipts (all under `/fast/scratch/hyaku/mado-r23/w2/ReopenFoot/`):
- `SOURCES.md.tip-2f1134f`: tip SOURCES.md, 136,607 B.
- `tip-rows.json`: the 11 tip rows with line numbers and cells.
- `fetch-foot-1.28.0.json`: HTTP status, bytes and sha256 for the 11 raw files.
- `foot-1.28.0/`: raw bytes of the 11 files, plus `meson.build`.
- `foot-1.28.0.tar.gz`: tag archive.
- `foot-clone-1.28.0/`: shallow tag clone (blob cross-check).
- `wiki/foot.wiki.git`, `wiki/Home.md`, `wiki/raw-attempt-Home.md`, `wiki/route-raw-commit.bin`, `wiki/route-raw-branch-master.bin`, `wiki/route-src-commit.bin`: wiki clone, pinned blob and route probes.
- `srcfoot-quote-match.json` and `receipt-srcfoot-quotes.json`: 50 mechanically parsed SrcFoot quotes, their match status, and the SrcFoot hash.
- `terminal-trees-r23.md.tip-2f1134f`: landed note at tip, 16,085 B.

## 8. Recommendations to the L1 (advice only; the L1 decides)

1. Correct the four overbroad sentences before landing or relying on them: S141 scope and teaches, S142 scope, S146 teaches, and S148 teaches. The note's line 31 repeats the S146 sentence.
2. Add "only when started with `--config`" to S147's teaches, and cite `input.c:210-211` if the binding claim is kept.
3. Fix SrcFoot's two defective supporting quotes (D1, D2) and the S148 offset (D3) before any SrcFoot text is reused. Commit SrcFoot.md or drop the reference to it.
4. No change is needed to the pins, URLs or anchor ranges. The N1 and N2 nits are optional.

VERDICT: 11 of 11 rows confirmed on the assigned checks (URL re-opened, pinned sha256 and bytes match, anchor ranges and located quote present in the bytes); 0 unopened. Mismatch (detail) on teaches/scope for S141, S142, S146 and S148, all from the same signal and clone overclaims. S147 precision notes. SrcFoot.md has 3 defective and 3 marker-only located quotes out of 50.
