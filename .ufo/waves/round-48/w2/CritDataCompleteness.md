# w2 / CritDataCompleteness — data-completeness falsification of the frozen C1/C2 registration

Seat target: find omissions among the 204 warm fixture classes and the 11 source rows, comparing each
requested axis-move and routed item to the actual frozen data. Method: independently enumerated the
fixture-class space from the pinned resolver's cache decision tree (`read_cache`/`save_cache`/option
processing, pin lines 179–1499) and the source-row space from the contract's coverage topics; then ran
five live probes against the pin inside the counter's own sandbox (read-only import of
`l1-draft/c1-r48-terminal-cache.py`, `--work` in my seat scratch) plus one independent read-only `xkbcli`
replay. No lane file was modified; no tool was installed (pacman paused; nothing needed).

Result: **3 confirmed C1 fixture-class omissions** (each is an in-contract resolver behavior with no
fixture, so a tool can pass 204/204 while being wrong), **1 C2 evidence-completeness gap**, and a short
"verified complete" list so the L1 can tell covered surface from holes. All other requested axis-moves and
routed items are present in the data.

---

## C1 — confirmed fixture-class omissions

### C1-A `default_cache` warm/hit is not covered (only the absent case exists)

- The `CACHE-DEFAULT` class has exactly **one** fixture, `v2-wd-38-default-cache-absent`, recorded
  `state=absent`. Its own `meta.note` says it was cold-probed because the w1 harness "cannot observe" a
  prime to the default path. No fixture primes the default location, and `gen_warm_case()` never sets
  `default_cache`, so the 80 generated warm cases do not touch it either.
- That reason is now stale. The L1 counter mounts `.rw/cache` onto `<root>/home/.cache` **writable** for
  `default_cache` cases (`prefix()`, lines 281–283), and `cache_inside()` resolves the default path for
  both prime and score. I confirmed live with the counter's own `Box`:
  - `P1` (`default_cache:true`, `prime.args:["--print-cmd"]`) → `state=hit`, rc 0, stdout `foot\n--a\n`.
  - `P2` (same, then a same-size entry edit `foot`→`feot`) → `state=hit`, warm stdout `foot\n--a\n` while
    the cold twin answers `feot` — a genuine, buildable `WARM-DIFFERS` at the default location.
- Why the existing clauses don't catch it: a tool that resolves the cache only under `$XDG_CACHE_HOME`
  (and treats an unset `XDG_CACHE_HOME` as "no cache possible") answers `absent` on `v2-wd-38` — correct —
  and never meets a default-location cache in any of the other 203 fixtures, because every one of them
  pins `XDG_CACHE_HOME=$ROOT/.rw/cache`. It scores 204/204 while contradicting the resolver's documented
  default path (`XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}`, pin line 172).
- Smallest correction (measure with `l1-draft/add-fixtures.py`, same recipe as `L1-04/05`):
  - `{"id":"L1-11-default-cache-hit","class":"WARM-SAME","default_cache":true,"prime":{"args":["--print-cmd"]}, ...}` (tree = the `add-fixtures.py` `FILES` block; expect measured `state=hit`).
  - `{"id":"L1-12-default-cache-differs","class":"WARM-DIFFERS","default_cache":true,"prime":{"args":["--print-cmd"]},"after":{"files":{APP+"foot.desktop": entry("feot --a","Actions=srv;\n[Desktop Action srv]\nExec=footclient\n")},"mtime":MT}, ...}`.

### C1-B `XTE_CACHE_ENABLED=""` (empty string) resolves to `disabled` and is not covered

- `check_bool("")` falls through to `*)` → `error "Assuming '' means no"` → returns 1 → cache disabled.
  Confirmed live: `P4` (`after.env.XTE_CACHE_ENABLED=""` over a well-formed cache) → `state=disabled`, rc 0.
- Fixtures cover `garbage` (`M-14`) and, in generated cases, `false/0/no/garbage`; `v2-ws-15/16` cover the
  truthy forms `true` and `1`. **Empty is uncovered**, and it is the one value that lands in a different
  branch than both "truthy" and "explicitly false".
- Why not caught: a tool that normalizes empty to "unset → default true" reads the cache and reports `hit`;
  the resolver reports `disabled`. No fixture sets the empty value, so the divergence is invisible.
- Smallest correction: add one disabled fixture, e.g.
  `{"id":"L1-13-cache-enabled-empty","class":"WARM-INVALID","cache": "<well-formed cache text>","after":{"env":{"XTE_CACHE_ENABLED":""}}, ...}` (expect measured `state=disabled`).
  (For completeness: the truthy spellings `yes/on/True/YES` are also unexercised — `P5` shows `yes`→`hit` —
  but they share `check_bool`'s true branch with `true/1`, so they are a lower-value add than empty.)

### C1-C cache path that is a directory → `absent` is not covered

- `read_cache` guards with `[ -f "${XTE__CACHE_FILE}" ]`; a directory at the cache path fails that test →
  `no cache data` → `absent`, and the run proceeds cold. Confirmed live: `P3` (cache file replaced by a
  directory before scoring) → `state=absent`, rc 0, cold stdout.
- No fixture places a non-regular file at `.rw/cache/xdg-terminal-exec`; all 25 literal-`cache` fixtures
  and all primes write a regular file.
- Why not caught: a tool that opens the cache path without an "is a regular file" guard attempts to read a
  directory (error or garbage parse) instead of answering `absent`. Every existing fixture has a regular
  file or nothing there, so the defensive branch is never scored.
- Smallest correction: add one malformed fixture that creates a directory at the cache path:
  `{"id":"L1-14-cache-is-dir","class":"MALFORMED", ... }` with `after.files` not applicable (the cache is
  under `.rw`, not the case tree) — implement by creating `.rw/cache/xdg-terminal-exec` as a directory in
  `prepare` (analogous to `materialize`), expect measured `state=absent`.

Non-findings (checked, deliberately out of scope): `XDG_CACHE_HOME=""` is blocked by the counter's own
`check_case` (must be under `$ROOT/.rw`), so it is unreachable by design, not a gap. A primed cache that
is then deleted scores identically to never-cached (both `absent`), so it adds no observable class.

---

## C2 — evidence-completeness gap

### C2-A the public entry point `xkb_keymap_new_from_names` is unpinned; step 8's NULL claim rests on inference

- The contract names the compositor-visible behavior: a failed resolve/parse "makes the RMLVO call return
  NULL" (registration C2; entry step 8). Entry step 8 cites `xkbcommon-xkbcomp.c:157-166` (resolve) and
  `:60-64` (parse) for that NULL. But those ranges are **internal bool-returning helpers**: I read the
  pinned `xkbcommon-xkbcomp.c` — `:60-64` is `CompileKeymap(...) { ... return false; }` and `:157-166` is
  `xkb_components_from_rules_names(...) { ... return false; }`. There is **no `return NULL` anywhere in the
  pin**; the public `xkb_keymap_new_from_names` (the function Hyprland actually links and the one named in
  clause i's ground terms) appears in the round-48 pins only as a *call site* in
  `xkbcommon-tools-compile-keymap.c`, and its defining file is not pinned.
- Concretely: clause i's four ground terms are `xkb_keymap_new_from_names`, `XKB-595`, `compile-keymap`,
  `xkeyboard-config-2.48`. At BASE all four are absent (satisfies the ground-absent half); at the data
  tip **three** occur (`XKB-595`, `compile-keymap`, `xkeyboard-config-2.48`) so the `>=2` half passes —
  but `xkb_keymap_new_from_names` is the one term that never lands. The entry talks about "the RMLVO call"
  without ever naming or pinning the symbol that returns NULL.
- Why the existing clauses don't catch it: clause d verifies the *quoted spans* verbatim at their pins —
  the `xkbcomp.c` quotes are verbatim, so d passes; clause e checks each step *cites* a pin — it does.
  Neither clause tests that the pinned bytes actually exhibit the NULL return the surrounding prose
  asserts. So the counter admits an entry whose central compositor-facing claim is supported only by
  unpinned inference — precisely the "a true quote at a true locator can stand beside a claim it does not
  support" residual the counter itself declares.
- Smallest correction (either):
  1. pin the file that defines `xkb_keymap_new_from_names` in 1.13.2, open one row for it, add a located
     quote of its `return NULL` path, and extend step 8's citation to it; or
  2. soften step 8's prose to "returns `false` internally (`xkbcommon-xkbcomp.c:157-166`, `:60-64`), which
     the public wrapper `xkb_keymap_new_from_names` turns into `NULL`", and still add the wrapper pin so
     the NULL step is evidenced rather than inferred.
  Option 1 is preferred: it closes the clause-i census term that currently dangles and makes the
  compositor-facing claim directly checkable.

Note (declared, not an omission): the entry's Limits explicitly scope out the `grp:*`/`caps:escape*`/
`lv3:*` option families and per-layout variant enumeration beyond `br`; those are stated limits, so their
absence from the receipt is by design, not a data hole.

---

## Verified complete (no action needed)

- **C1 cache states:** all six recorded states exercised — `hit` (90), `stale` (47), `absent` (40),
  `invalid` (17), `disabled` (5), `-`/unreached (5).
- **Terminator boundary:** first-command-line (11/12), mid (49), the line-limit (50 total, terminator on
  50), beyond (51), and no-terminator EOF are all covered (`v2-mf-03/04`, `M-16`, `M-17`, `v2-mf-10/11`,
  `v2-mf-01/02/05/09/12/13`).
- **Cache-field mutations:** hash (`wi-26/27/28/32`, `mf-06/07/08`, `M-11`), cmd (`wi-29/30`, `M-06`,
  cached-cmd-subst), entry_path lying (`mf-22`, `L1-01/02/03` incl. `--print-content`), entry_id
  (`mf-23/24`), action (`L1-05`), execarg CRLF (`mf-25`), command-body junk/two-terminators/CRLF/empty
  (`mf-18/19/20/27/28/29/30`).
- **Arg direction:** cached-arg-vs-scored-arg is covered both ways for `dir` (`W-06` scored-dropped vs
  `v2-wd-32` cached-wins); `title/app-id/hold` exercised via prime+scored pairs (`v2-wd-07/08/09`,
  `v2-ws-06/07/13`).
- **Cache control:** env truthy (`v2-ws-15/16`) and falsy+garbage (`M-13/14`, `v2-wi-18/19/20`); the
  "first cache directive wins / env pre-configures" behavior via `v2-wd-25` (warm hit never reads the
  list). The `/disable_cache` save-side effect is correctly unobservable in the scored surface.
- **C2 rows:** every contract topic maps to a row — defaults/empty names (S344/S345), compositor
  `XKB_CONTEXT_NO_FLAGS` context (held S319), RMLVO mapping (S340/S346), comma-list alignment (S340 +
  receipt), include-path order (S342/S343), fail-vs-silent names (S346/S347/S350), host-only results
  (S350).
- **C2 receipt:** re-ran read-only on this host — positive `--layout br --options compose:caps` rc 0 with
  sha256 `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81` (byte-equal to the receipt,
  2090 lines / 73079 bytes), negatives `--layout zz` rc 1, `--variant nope` rc 1, `--options nope:nope`
  rc 0 + `XKB-595`; version triple 1.13.2 / 1.13.2-1 / 2.48-1 present. Every observational prose claim in
  the entry (rules base/xorg/xfree98/nope, model-`nope` geometry `pc(pc104)`, multi-layout runs,
  `XKB_CONFIG_ROOT`/`XKB_CONFIG_EXTRA_PATH` overrides, `--enable-environment-names`, include-path
  precedence) is backed by a receipt section.
- **C2 structure:** 9 numbered steps each cite a pin locator (>=6); README row is one 3-cell column-0
  row naming no other `knowledge/` file and covering S340–S350; held rows S318/S319 and the r46 entry are
  present; 3 of 4 clause-i ground terms land at REV.
- **Routed items present as data:** D1 HOME-unset (C1 contract clause + `HOME-UNSET` ×10 and
  `EDGE-HOMEUNSET`), D3 readdir-order (`READDIR` ×10), M47-10 schema v2 (all 204 fixtures are schema v2),
  `CritC1Explain` (clause x compares `cmd=` and `--observed` both ways), R4b/D4/D2/R3 receipts present
  under `w1/ExecErrataR45`, `w1/ScrErrataD4`, `w1/ExecD2Receipt`, `w1/ExecSessionMarker`.

## Evidence
- `w2/CritDataCompleteness/fixture-inventory.txt` — all 204 fixtures, class/id/state/args.
- `w2/CritDataCompleteness/probe-gaps.py` + `probe-output.json` — the five live pin probes (P1–P5) and
  their results, run inside the counter's own sandbox with `--work` under this seat's scratch.

Largest output file written: `fixture-inventory.txt` (≈21 KB). Total seat scratch stayed under the 2 GB
budget and was cleaned before return. One bounded deviation recorded: the counter's `Box` copies the
resolver's external commands (host binaries, `gawk` ≈1 MB) into the sandbox, which exceeds the 1 MiB/file
writer guard; that is harness setup, not seat output, and was removed with the scratch.
