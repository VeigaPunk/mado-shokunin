# ReopenKitty — wave 2 C2 source re-open (SOURCES rows S123–S133 at lane tip 2f1134f3)

Reviewer seat `MadoR23.ReopenKitty`, 2026-10-22. Scope: for each `corpus/SOURCES.md` row
S123–S133 at commit `2f1134f38930fc8b067d2d7f5bba126338faabdd`, re-open the URL by ordinary
means, recompute the recorded sha256, and confirm the anchor lines and the located quotes in
`.ufo/waves/round-23/w1/reports/SrcKitty.md` against the fetched bytes. No lane file was
edited except this report; no subagents were used.

## Verdict

**C2 kitty sourcing: confirmed.** 11/11 rows re-opened, 0 unopened, 0 substantive mismatch.
Every row-recorded sha256 and byte size reproduces exactly; every anchor line range is correct
in the fetched bytes; the tag pin and the tag-tarball-equality claim reproduce. Four findings,
all prose-level in `SrcKitty.md`, none touching the landed rows or C2's counting (details below).

## What I ran

All artifacts under `/fast/scratch/hyaku/mado-r23/w2/ReopenKitty/` (raw downloads in `raw/`,
checker `check.py`, machine receipt `reopen-receipt.json`, landed-row extract
`SOURCES-S123-S133-at-tip.md`). Nothing outside that directory and this report was written.

```
git -C <lane> show 2f1134f38930fc8b067d2d7f5bba126338faabdd:corpus/SOURCES.md   # rows S123-S133 extracted (11)
curl -fsSL <url> -o raw/<name>            # 11 URLs, one at a time, ordinary means only
python3 check.py                          # sha256 + anchor/quote verification -> reopen-receipt.json
git ls-remote https://github.com/kovidgoyal/kitty refs/tags/v0.49.2 refs/tags/v0.49.2^{}
curl -fsSL -o kitty-v0.49.2.tar.gz https://codeload.github.com/kovidgoyal/kitty/tar.gz/refs/tags/v0.49.2
tar xzf kitty-v0.49.2.tar.gz -C tarsrc    # per-path sha256 comparison raw/ vs tarball
curl -fsS -o conf.html.now https://sw.kovidgoyal.net/kitty/conf.html   # redirect-stub characterization (GET)
```

No install or upgrade was needed (tooling directive: nothing to record). No captcha or bot
challenge was encountered; every URL opened on the first try. The one `curl -fsSI` (HEAD)
probe of `conf.html` returned 200 with no `Location`; that is a probe artifact — the GET body
is the 325-byte redirect stub (see S132).

## Per-row verdicts

| row | URL (fetched) | sha256 recomputed | bytes | verdict |
|---|---|---|---|---|
| S123 | raw.githubusercontent.com/kovidgoyal/kitty/b2cb8712…/docs/conf.rst | `da42c340321755a25718b5c9a467f0a6bba33f88342d7c4a35e87a6795d4f498` ✔ | 3901 | **confirmed** (finding F2: quotes are RST-role-stripped renderings) |
| S124 | …/kitty/simple_cli_definitions.py | `228f36b35e5e82419b8b4127742efdc5a17387763e62a1b26a73f6802a5452e3` ✔ | 30246 | **confirmed** (findings F2/F3 detail below) |
| S125 | …/kitty/launcher/utils.h | `32a5c10e67efe0e10b9b30d211e1e193d8bd80faaf1f2845a1a3d35188e81cfc` ✔ | 9097 | **confirmed** (all quotes verbatim, all 5 anchors exact) |
| S126 | …/kitty/conf/utils.py | `5af002918cbf199f2bd250527322b1b49af33fda66d255434d5efb8256eca295` ✔ | 17984 | **confirmed** (verbatim; `key_pat` regex byte-exact at :24; missing-file log found at :355 window; `resolve_config` :439) |
| S127 | …/kitty/options/definition.py | `1ff05cd3a58612c0bd12de7a15d9f645ca3f6ebcdbbb5d0a380740730ef22cc5` ✔ | 165097 | **confirmed** (finding F4: one prose anchor off by one) |
| S128 | …/kitty/child-monitor.c | `a4fbe5472c50249c30002919d6454aa97a7fda38d384023472af0bffedd14ae7` ✔ | 100305 | **confirmed** (verbatim: `case SIGUSR1:` :1708, relay token :1851–1854, `reload_config_called` :558–566, `call_boss(load_config_file` :640) |
| S129 | …/kitty/rc/load_config.py | `89ccc155ef6eadcc72cc81aebf22496b31dfe7ece107cb1fbbd49e66f119dc04` ✔ | 2747 | **confirmed** (desc quote verbatim on :33; finding F5 note) |
| S130 | …/kitty/cli.py | `696d04198a48d0d8f05023755efce79f52a53e0e2e3e8abb90a2afa6010c5456` ✔ | 22988 | **confirmed** (`SYSTEM_CONF = f'/etc/xdg/{appname}/{appname}.conf'` byte-exact at :716) |
| S131 | …/docs/changelog.rst | `cd2046f7fb8dbe7cdbf92cda2410e862cf68cd1514380da5e0a3f9c070aa5fae` ✔ | 243954 | **confirmed** (`0.49.2 [2026-10-01]` byte-exact at :202) |
| S132 | sw.kovidgoyal.net/kitty/conf/ | `08e6411024fdfc444e47750dadc28b7d87e0bd768695cc635690916e08a9703d` ✔ | 577387 | **confirmed** (finding F1: one prose statistic wrong; row itself unaffected) |
| S133 | …/kitty/constants.py | `8a0ee5204417ff90747a2965f8b4594a2d3a02d35f7b3728301350892663bde8` ✔ | 10477 | **confirmed** (`defconf = os.path.join(config_dir, 'kitty.conf')` byte-exact at :130; `_get_config_dir` in :109–126) |

Every row-recorded byte size also matches (S123 3901, S124 30246, S125 9097, S126 17984,
S127 165097, S128 100305, S129 2747, S130 22988, S131 243954, S132 577387, S133 10477).

## Pin corroboration

- `git ls-remote` today: `refs/tags/v0.49.2` → `e300597364aabb4890ebdd3a5491397f858fd714`,
  peeled → `b2cb871254fbdac19a085188813c8dfb258b95cd`. Identical to the w1 report's pin.
- Tag tarball sha256 today: `e9ca20b49d0c262af956058ceb97cfef505552dc447d8328ea96d069a04570f3`
  — identical to the w1 receipt. All ten raw-fetched files are byte-identical to the same paths
  inside the extracted tarball (`ALL_IDENTICAL: True` in the run log).

## Landed rows vs draft (drift check)

The landed `SOURCES.md` rows S123–S133 at `2f1134f3` carry anchor cells **identical** to the
`SrcKitty.md` draft table (11/11), the same URLs I fetched, `status` = `mined` for S123–S131
and S133 with S132 `queued`, `opened` = `2026-10-22`, `recheck` = `on-release`, `used-by` =
`corpus/knowledge/terminal-trees-r23.md` for all mined rows (S132 `—`). No drift between the
draft the scribe published and what landed.

## Findings (none blocks the landed rows)

- **F1 (minor, w1 prose only).** `SrcKitty.md` claims the built docs page contains
  "`kitty.conf` ×50". The actual substring count in the pinned bytes (sha-identical to the
  w1 fetch) is **31** (case-insensitive also 31). The landed S132 anchor cell records only
  bytes+sha256, which reproduce, so the row is unaffected; the prose statistic is wrong.
- **F2 (caveat, no defect in rows).** The S123 and S127 located quotes (and S123's reload
  quote in the sources table) are **RST-role-stripped renderings**, not raw-byte substrings:
  e.g. bytes `docs/conf.rst:20-22` read "You can manually reload the config by pressing
  `:sc:`reload_config_file`` (`:kbd:`⌃+⌘+,`` on macOS) or sending `|kitty|` the
  "``SIGUSR1``" signal". I verified every quoted sentence word-equal to the anchored lines
  after stripping `:sc:`/`:file:`/`:kbd:`/`:code:`/`**` markup. Anchors are correct; readers
  should know the quotes are normalized, not verbatim.
- **F3 (caveat, S124).** The S124 located quote is additionally a **template-substituted
  rendering**: the bytes carry `:file:`$XDG_CONFIG_HOME/{appname}/{conf_name}.conf`` etc.
  (placeholders, not `kitty`/`kitty.conf`), and the sentence ends "The first one that exists
  **is used as the config file**" (:369-370), which the quote truncates. `CONFIG_HELP` starts
  at :359, the search order is :366-370, and the `KITTY_CONFIG_DIRECTORY` suppression sentence
  is at :372-373 — the row's teaches content is exactly what the bytes state.
- **F4 (trivial, w1 prose only).** The w1 extra-quote list anchors "automatic reload works
  only if the kitty.conf already exists when kitty is started" at `:3099-3100`; the sentence
  actually starts at the end of **:3098** ("Note that automatic") with the remainder on :3099,
  and "Changes to this setting … ignored." is on :3100. The S127 row's own anchor cell
  (`:3090-3101`) is correct.
- **F5 (note, S129).** The literal token `load-config` does not occur anywhere in the pinned
  bytes; :31 is `short_desc = '(Re)load a config file'`. The command name is the rc framework's
  class→command convention from `class LoadConfig`. The row's anchors (:31, :33-36, :37-55)
  all verify and the desc quote is verbatim on :33; only the hyphenated spelling in the
  teaches cell rests on convention, not on a byte in this file.

## Residual risk

- S132 (`sw.kovidgoyal.net/kitty/conf/`) is a moving, unpinned build by the lane's own
  declaration; its bytes will drift and it supports no claim. Recorded posture (`queued`,
  `recheck on-release`) is the right one.
- The doc quotes' markup-stripped rendering (F2/F3) is a presentational convention; a future
  automated quote-checker doing raw substring matching would flag S123/S124/S127 prose quotes.

## Verification gaps

None material. Every row was opened; every recorded sha256 and size was recomputed from fresh
bytes; every anchor range was checked line-by-line in the fetched bytes; quotes were checked
verbatim and, where rendering applies, word-equal after markup stripping. I did not re-run the
C2 counter — that is another seat's item; nothing here changes its inputs.

Receipt: `/fast/scratch/hyaku/mado-r23/w2/ReopenKitty/reopen-receipt.json` (fetch codes, sha256
per row, per-fragment line hits, landed-row sha/size equality). Raw bytes:
`/fast/scratch/hyaku/mado-r23/w2/ReopenKitty/raw/`.
