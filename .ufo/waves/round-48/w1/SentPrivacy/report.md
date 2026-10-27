# SentPrivacy — privacy of the round-48 receipts

Seat `SentPrivacy` (sentinel, leaf), mado round 48 / wave w1, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`, lane tip at
scan time `5ff167423ee410251da0ef0c82f8e6fa25875665`. Assignment: name the classes of host material the round's receipts could
carry (device names, keymap text with user paths, home paths inside the cache hash input, cache files with `HOME` paths), decide
whether `quality/check-session-material.py` catches each class, and list the classes it misses.

Everything below is measured. Fixtures are **synthetic** (`syntheticuser`, `example-host`, `synthetic-*`); no host value is
committed, and no receipt of mine prints one. Reinstalled/upgraded tools: **none** (no package or tool transaction was run).

---

## 0. Verdict

- The gate catches the four legacy shapes round 45 designed it for (JSON client dump with `class`+`title`, `ss -p` rows, monitor
  `serial`+identity, and a plainly formatted home listing of more than ten entries).
- It **misses 16 of 19** synthetic receipt shapes drawn from this round's own write surfaces, including every shape that carries
  a *user path* in the form this round actually produces them (`xkbcli --verbose` include paths, `ls -LRl` of a flat application
  directory, cache text, `grep` of a config file with an absolute prefix).
- The round's own receipts **already** carry real host paths: 33 receipt files, 75 `/home/...` lines, 37 distinct home paths, and
  116 occurrences of the account name in `ls -l` owner/group columns across 35 files — the gate reports **zero** findings on
  all of them (`receipts/round48-home-aggregate.txt`, `receipts/round48-home-line-shapes.txt`).
- Two structural defects matter more than any single class: the gate scans **only `.ufo/`** (`quality/check-session-material.py:256`)
  while this round's claims commit to `corpus/knowledge/`, `quality/counters/` and `tools/`; and it is **already red at base**
  (128 findings at both `579f694b` and `5ff16742`), so "the gate passes" is not an available signal for the freeze.

Severity: **S2** for the instrument (a published predicate, `corpus/QUALITY.md:418`, whose coverage is narrower than its own
wording — counterexamples below); **S3** per missed class (the lane already commits absolute `/home/<user>` paths in prose status
quo: 68 tracked files under `corpus/` at scan time, 73 across `corpus quality tools docs`), **S2** for the two classes that publish a *listing* rather than an isolated path
(application-inventory `ls -LRl`, cache text with entry path + `--title`).

---

## 1. Method

1. Read the gate (`quality/check-session-material.py`, 682 lines) and its declaration (`corpus/QUALITY.md:418`,
   `SKILL.md:770`); ran its selftest: `SELFTEST: passed=22/22 failed=0`.
2. Built a throwaway git repo of **synthetic** receipt shapes (`receipts/shapes.py`, `git init` in scratch, toplevel asserted)
   and scored it with the gate itself: `receipts/gate-on-shapes.txt`, `receipts/class-verdicts.txt` (per-shape JSON).
3. Probed nine further shapes (process tables, plain-text window data, env dumps, encodings, cache text) and the 16 MiB cap
   directly through the gate's own `scan_blob()`: `receipts/extra-shape-probes.txt`.
4. Scanned the **whole live round-48 tree** (untracked, read-only) with the gate's four rules and characterized every home-path
   line by shape (masked to `/home/U`): `receipts/round48-home-line-shapes.txt`, `receipts/round48-and-xkb-census.txt`.
5. Measured what the two live receipt producers in this round put on disk: `xkbcli compile-keymap` (plain and `--verbose`,
   stdout only, no compositor), and the two round-48 executor probe scripts that produce receipts.

---

## 2. Class table — what the round can carry × what the gate sees

`CAUGHT`/`MISSED` are the gate's verdict on a synthetic file of that shape (`receipts/class-verdicts.txt`).

| id | class (no values) | round-48 carrier | verdict |
|----|-------------------|------------------|---------|
| PR-01 | window-title strings outside a JSON object (`--title=` in cache text, `jq -r` projections, plain-text window dump) | C1 cache fixtures / `explain` captures; any `hyprctl activewindow` text | **MISSED** |
| PR-02 | input-device names and addresses (`devices -j` elements projected to `name`/`address`/`layout`) | C2 live receipt (this host's keyboard list is the held ground for the fallback row) | **MISSED** |
| PR-03 | instance signature and `/run/user/<uid>/hypr/<sig>` socket paths | any `instances -j` / `HYPRLAND_INSTANCE_SIGNATURE` shape check | **MISSED** |
| PR-04 | home paths inside the **cache hash input**: `ls -LRl` of a *flat* application directory (one bare header + data rows) | C1 warm-cache receipts that reproduce the md5 input | **MISSED** (3 headers tested) |
| PR-05 | listing rooted **outside `/home`** (`$ROOT` sandbox, `/fast/scratch`, `/run/user`, `/srv`) | every C1 counter run: `HOME=<root>/home`, `XDG_CACHE_HOME=<root>/.rw/cache` (`quality/counters/c1-r47-terminal.py:222-224`) | **MISSED** |
| PR-06 | listing spelled `$HOME/...` or `~/...` | `w1/ExecXkbLive/probe.sh:23` masks `$HOME` on purpose — the masked form then becomes invisible to the gate | **MISSED** |
| PR-07 | listing encoded or embedded in structure (base64, JSON array, markdown table, quoted strings) | a receipt pasting a dump into JSON/table form | **MISSED** |
| PR-08 | any material past 16 MiB of a receipt | large concatenated receipt logs | **MISSED** — all four rules stop at the cap (see D-C) |
| PR-09 | binary / UTF-16 receipts (NUL in first 8 KiB) | screenshots, `xxd`/UTF-16 captures | **MISSED** (declared limit) |
| PR-10 | cache text as such: cached entry path, `--dir`, `--title`, exec line | C1 fixtures (`"cache": "<literal>"`) and any primed-cache receipt | **MISSED** |
| PR-11 | process table in a non-`ss` dialect (`ps aux`, `pgrep -a`, resolver debug trace) | C1 "no process started" proofs | **MISSED** |
| PR-12 | secret-shaped values (token, cloud key, private-key block) | env dumps in fixtures/probes | **MISSED** (no rule at all) |
| PR-13 | material committed **outside `.ufo/`** (`corpus/knowledge/` = C2 entry, `quality/counters/` = C1 fixtures, `tools/`) | C1 + C2 deliverables themselves | **MISSED** (scope) |
| PR-14 | user config content with an absolute path prefix (`grep -n /home/<u>/.config/...`) | measured live: `w1/ScrEntry/receipts/xkbcli-compile-keymap-r48.txt` (16 such lines) | **MISSED** |
| PR-15 | user paths in tool diagnostics (`xkbcommon: INFO: Include path failed: "<home>/…"`) | measured live: `w1/ScrRows/receipts/verbose-include-paths.err` (2 lines), `w1/ScrSkill/receipts/xkbcli-matrix.txt` (3 lines) | **MISSED** |
| PR-16 | keymap symbols text of a user-supplied `$HOME/.xkb` tree (content, no paths) | C2 keymap capture if a user tree existed | **MISSED** |
| PR-19 | owner/group **account name** in `ls -l`/`stat` columns — no `/home` prefix at all | measured live: `w1/ScrCacheDoc/receipts/ls-listing.txt` (22), `w1/ScrEntry/receipts/xkbcli-compile-keymap-r48.txt` (15), `w1/CritPremiseC1/receipts/ls-{before,after}.txt` (6 each) | **MISSED** |
| PR-17 | `>10` distinct bare absolute `/home/...` lines, or ≥11 `ls -LRl` directory headers | a recursive dump of `~/.config` | CAUGHT |
| PR-18 | JSON client dump with `class` + non-empty `title`/`initialTitle` | any `hyprctl clients -j` paste | CAUGHT |
| — | `ss -p`/`ss -xpa` rows; monitor object with `serial` + `description`/`make`/`model` | round-45..47 residue | CAUGHT |

Measured totals: of 19 synthetic shapes, **3 caught / 16 missed** (`GATE rc=1 missed=16 caught=3 files=19`); of 9 further
probe shapes, **9 missed**; the two `.ufo`-external copies were invisible (`files=19` counted only the `.ufo` blobs).
Live measurement over the round's own tree: 33 receipts with `/home/` paths (75 lines, 37 distinct) and 35 files with 116
account-name occurrences → **0** findings. Both numbers grow while seats write; the receipts record the snapshot time.

---

## 3. The discriminating line (why PR-04/PR-06/PR-14/PR-15/PR-19 are the real exposure)

R4 counts *distinct whole lines that are nothing but an absolute `/home/<user>/…` path*, above a threshold of ten
(`quality/check-session-material.py:29-31`, regex at `:75`). It does fire on deep dumps: at the tip the only two R4 findings are
`.ufo/waves/round-35/scratch-evidence/SentProvenance/S203.scope.txt` (12 distinct) and
`.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt` (40 distinct) — so the rule works, it is the *shallow/flat* form of the same
material that it cannot see. Everything this round produces fails one of those three clauses:

- `ls -LRl` prints **one header per directory**, so the cache hash input of a *flat* application directory is 1 bare line plus
  data rows that carry a mode string → below threshold, rows with whitespace skipped (measured: 3 headers → MISSED; 12 headers
  → CAUGHT). The hash input is therefore invisible exactly where it is most sensitive: the user's own desktop-entry inventory.
- The absolute prefix form (`path:line: text`) is a *content* receipt, not a listing → MISSED, and it is the form two round-48
  seats already used.
- `$HOME`-masked output — the lane's own privacy practice (`probe.sh:23`) — is *guaranteed* MISSED, so the gate rewards a
  masking style it cannot verify.
- The account name also appears where **no path exists**: `ls -l` owner/group columns. R4 regexes for `/home/...`, so the
  `-rw-r--r-- 1 <user> <user> …` row of any listing is invisible even when the listing itself is long. The C1 byte-identity
  artifact is the worst case: `w1/ScrCacheDoc/receipts/warm-cache.txt` prints "the ls stdout that is hashed" — owner columns
  plus a `…/applications/:` header — and the cache bytes as an `od -c` dump, i.e. PR-04 + PR-10 + PR-19 in one receipt that the
  gate calls clean (`gate=[]` in `receipts/round48-home-aggregate.txt`).

---

## 4. Instrument defects (beyond single classes)

**D-A scope ≠ declared scope.** The scan reads `git ls-tree … -- .ufo` (`quality/check-session-material.py:256`), but
`corpus/QUALITY.md:418` claims the property "for the files the round adds", and this round's adds are `tools/mado-terminal.py`,
`quality/counters/c1-r48-*.py`, `corpus/knowledge/xkb-keymap-compile-r48.md`, `SOURCES`, `corpus/README.md`. Measured: a client
dump and a cache text committed under `corpus/` and `quality/counters/` in the same fixture repo produced **no** finding.

**D-B R4 shape/threshold/root coupling.** One rule carries three independent blind spots (line shape, `/home` anchor, fixed
threshold of 10), so "no home-directory listing" is not what it measures; it measures "a deep tree dumped as bare lines".

**D-C 16 MiB cap is stricter than declared.** The docstring says large files are "scanned for R2/R4 only"
(`quality/check-session-material.py:53-55`), but `decode()` truncates to `MAX_TEXT` (`:188`), so R2/R4 also see only the first
16 MiB. Measured with one tail of [40-line listing + `ss` row + client object]: at file start → `R2=1 R4=40 R1=1`; after 17 MiB
of filler → **no finding**.

**D-D the gate is red at base and at tip.** `SESSION_MATERIAL: files=19969 findings=128 rev=579f694b…` and
`files=19975 findings=128 rev=5ff16742…`, same per-rule tally (`R1=33 R2=36 R3=57 R4=2`); no synthetic marker exists
(`SKILL.md:770` says a red exit is expected). Consequence for the freeze: a *new* true positive is indistinguishable from the
128, so the usable predicate is a **delta between revisions**, not exit 0.

**D-E R2 is one dialect.** `users:(("<prog>",pid=<n>` only; `ps`, `pgrep -a`, resolver debug traces and `htop`-style rows are
invisible (PR-11).

**D-F no secret rule.** `SKILL.md:343` keeps session material shape-only and the standing rules keep secrets shape-only, but no
rule matches a secret-shaped value; an env dump is scanned only for `/home` lines (PR-12).

---

## 5. What is already correct (no false alarm raised)

- `w1/ExecXkbLive/probe.sh` masks `$HOME`/scratch (`:23`), replaces keyboard names with `kbd1..n` (`:176-184`) and keeps counts
  only; its receipt `receipts/xkb-live.txt` has **0** home-path lines (4 `$HOME` tokens, 4 include-path lines, all masked).
- Note the asymmetry the round discovered by itself: receipts produced **inside** the counter's `bwrap` sandbox show numeric
  ids and scratch roots (PR-05 still misses them), while receipts produced **outside** it (`ls -l` byte-identity demos) resolve
  the account name and are the ones that publish it (PR-19). Both forms are gate-clean.
- The round-47 counter's sandbox pins `HOME` and `XDG_CACHE_HOME` into the case root
  (`quality/counters/c1-r47-terminal.py:222-224`) and runs with `--clearenv`, so C1 receipts carry scratch paths by
  construction — which is precisely why PR-05 exists and why it must be enumerated rather than assumed.
- `xkbcli compile-keymap` **without** `--verbose` leaks nothing: 73,079 bytes of keymap, 0 home-path lines, 0 include lines.
  The leak appears only with `--verbose` (2 home-path lines, 4 include-path lines, 2 distinct paths) — the flag the C2 claim
  needs to document include order. Round-48 already used it twice, once masked, once not.

---

## 6. Exploit path (ordered, all read-only; no host value used)

1. C1 seat primes the pin over the host's *real* application dirs (the guard forbids writing the host cache, not reading
   `~/.local/share/applications`) with `XDG_CACHE_HOME` in scratch; the primed cache line 3 is the user's own `.desktop` path
   and line 8 is the recorded `--title` argument.
2. Seat pastes either the cache text or the `ls -LRl` hash input into a receipt to prove byte-exactness → PR-04 + PR-10 +
   PR-01: an inventory of the user's installed entries and a title string.
3. The gate reports nothing: the listing is one bare header plus data rows (PR-04), the paths are under `/home` but inline
   (PR-14), and if the seat masked `$HOME` it is PR-06.
4. Same file committed under `quality/counters/` (fixture) or `corpus/knowledge/` (C2 entry) → PR-13, not even read.

Impact: a committed, publishable list of the user's local desktop entries (application inventory), the last terminal title the
resolver cached, keyboard/model identity strings, and instance names — while the gate's exit status says clean.

---

## 7. Smallest remediation (ranked; each is checkable)

1. **Make the predicate a delta, not an exit status.** Freeze it as `findings(rev) \ findings(base)` with a recorded synthetic
   marker for the 128 known lines (D-D). One-line wrapper around `run()`; the round then has a signal it can actually cite.
2. **Widen R4 to the shapes this round emits** (PR-04/06/14/15): count *distinct absolute path matches anywhere in the file*
   (bare or inline, `/home`, `$HOME`, `~`, and the scratch root) with a per-file limit of 3, and treat a line that is a
   directory header (`<abs path>:`) as a listing entry. Fixture: the 3-header `ls -LRl` must go red. Each missed class above
   gets one negative selftest case: the current 22 cases exercise only the four legacy shapes, so the gaps are not even
   representable in the gate's own suite.
3. **Scope**: add `--pathspec` (default `.ufo corpus quality tools`) or scan the whole tree; the ~70 existing corpus
   `/home/<user>` files become baseline lines folded into (1).
4. **R5/R6/R7 classes**: object with `name`+`address`+(`layout`|`scrollFactor`) → device identity; `instance` matching
   `<host>_<pid>_<start>` or any `/run/user/<uid>/hypr/` path; `--title=`/`title=` with a non-empty value outside JSON.
5. **Encoding/secret carriers**: reject (not decode) receipts whose content is base64/gzip/UTF-16-shaped, and add one
   secret-shape regex (`ghp_`, `AKIA`, `xox[bap]-`, `-----BEGIN … PRIVATE KEY-----`, `*_TOKEN=`, `*_SECRET=`).
6. **Fix D-C wording or the cap**: scan the file in windows so no rule depends on the 16 MiB prefix.
7. **Seat-side, free**: require the `probe.sh:23` `hide()` step in the C1/C2 seat specs and forbid `--verbose` captures without
   it; that removes PR-14/PR-15 at the producer, where the gate cannot help.
8. **Account name is not a path** (PR-19): mask it in receipts, or produce `ls -ln`/`stat -c` output with numeric ids — the
   counter's own sandbox already yields numeric ids, because it runs `ls` inside `bwrap --clearenv` with no `/etc`
   (`quality/counters/c1-r47-terminal.py:139-151`). A rule, if wanted, is one regex on `^[-dlbcps][rwxsStT-]{9}[+.]?\s+\d+\s+(\S+)`
   comparing the owner column against the account name from `pwd`.

---

## 8. Receipts (all under `.ufo/waves/round-48/w1/SentPrivacy/receipts/`)

| file | what it shows |
|------|---------------|
| `shapes.py`, `verdict.py`, `scan_tree.py` | the synthetic fixture builder, the per-class scorer, the tree scanner |
| `gate-on-shapes.txt`, `class-verdicts.txt` | gate output and per-shape JSON verdicts: 19 shapes, 3 caught, 16 missed |
| `extra-shape-probes.txt` | 9 further missed shapes + the 16 MiB truncation experiment |
| `round48-home-line-shapes.txt` | masked shape + distinct-path count + gate verdict for four representative round-48 receipts |
| `round48-home-aggregate.txt` | the whole round-48 receipt census: files/lines/distinct home paths, account-name occurrences, gate verdict, masked warm-cache shape |
| `round48-and-xkb-census.txt` | whole round-48 tree scan under R1-R4 (only the R3 marker draft's own synthetic fixtures and this seat's fixture builder appear), plain vs `--verbose` xkbcli measurements, per-receipt leak census |
| `baseline-and-selftest.txt` | gate tally at base and tip (128 findings each) and `SELFTEST: passed=22/22` |
| `verify-quotes.sh`, `verify-quotes.txt` | every locator in this report verified against the working tree (exit 0) |

Reproduce (lane root):

```
python3 -I quality/check-session-material.py --selftest
TMPDIR=<scratch> python3 -I .ufo/waves/round-48/w1/SentPrivacy/receipts/shapes.py <scratch>/fit quality/check-session-material.py
TMPDIR=<scratch> python3 -I .ufo/waves/round-48/w1/SentPrivacy/receipts/verdict.py <scratch>/fit quality/check-session-material.py
/usr/bin/xkbcli compile-keymap --layout br --options compose:caps --verbose 2>&1 | grep -c '/home/'
```

Boundary note: no compositor verb at all (no `hyprctl` call); `xkbcli` only with `compile-keymap`; `xdg-terminal-exec` **not
run** (this seat needed no cache); the host cache was never read or written; no package or tool transaction; work done in
`<scratch>/hyaku/mado-r48/SentPrivacy/` and removed on exit.
