# CritOracleClaim — findings against the oracle observation cited by entry §4

Seat: w2 critic, round 43 (hyaku run 8, 2026-10-26). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Item attacked: `corpus/knowledge/hyprland-gkeep-geometry-r43.md:62` (entry §4, the **INF** sentence, at
data commit `1959770657f1f8665097c1aed4be6c1cbb07139f`, base `a35cfdf`) and the apparatus it cites,
`.ufo/waves/round-43/w1/ExecOracleGkeep/` (`ExecOracleGkeep.md`, `20-observation.txt`, `10-cases.txt`,
`receipts/`). Registration v1 and v2 were read first; v2 does not touch this item.

Entry text is byte-identical at the data commit and in the worktree (`sha256 4d16b3fb…`), so the
sentence below is the scored one. I did not run a compositor, took no host write verb, ran no package
transaction, and wrote nothing outside `.ufo/waves/round-43/w2/CritOracleClaim/`.

## 1. Clause-by-clause verdict

| # | clause of entry §4 (line 62) | verdict | receipt |
|---|---|---|---|
| 1 | "In the isolated round-27 oracle" | **OVERSTATED** (apparatus named is not the one that ran) | §2.1 |
| 2 | "(a Hyprland 0.56.2 nested under tinywl in bubblewrap, never the host session)" | **SUPPORTED** | §2.2 |
| 3 | "a client with that app id" | **SUPPORTED literally, UNDER-DISCLOSED** (a purpose-built shm surrogate, not the app) | §2.3 |
| 4 | reported `"size": [420, 500]`, `"floating": true` "under the host's three rules" | **SUPPORTED exactly** | §2.4 |
| 5 | "with the size line removed the same client reported its own 200x200 buffer" | size **SUPPORTED**; "the same client" **OVERSTATED** (different client sha) | §2.5 |
| 6 | "with `size 300 300` it reported 300x300" | **SUPPORTED** | §2.6 |
| 7 | "with the `float on` line removed it was tiled" | **SUPPORTED** | §2.7 |
| 8 | "In that oracle, the rule, not the client, is the origin of 420x500" | **SUPPORTED as scoped; does not resolve the host ambiguity the same paragraph raises** | §2.8 |

Answer to "was the host's rule file used byte-identically": **yes**, exactly — `rules-host.conf`,
`.ufo/waves/round-43/fetch/host-gkeep.conf` and the live `~/.config/hypr/gkeep.conf` are one sha
(`3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949`), the receipt records that sha
(`receipts/receipt-headlesshost.json:439`), and `diff` is empty (`receipts/identity.txt`). The rule
file has no `exec` line, so the runner's `strip_exec()` is a no-op on it.

Answer to "which binary, sha": the compositor is `/usr/bin/Hyprland`, read-only (`--ro-bind /usr /usr`;
tinywl boots `exec Hyprland -c …` with `PATH=/usr/bin`). **No sha256 of that binary is recorded** —
the receipt's hash fields are only `client_sha`, `libwlroots_sha`, `rules_sha`, `sandbox_log_sha`,
`tinywl_sha` (`receipts/binary-and-negatives.txt`). Its identity rests on the nested server's own
`hyprctl version -j`: `version 0.56.2`, `tag v0.56.2`, `commit efb5099…`, `abiHash efb5099…_aq_0.15…`
(`receipt-headlesshost.json:481-501`) and on the instance signature (`:207`), which differs from the
host session's live signature (`…_1792986098_301483618` vs the nested `…_1792999739_542277837`,
`receipts/identity.txt`). Today's host binary hashes `55da553be71222566ee73b973d2f56dbb9939044d8f22f81aa54b66c83f2f6d1`
and reports the same commit — corroboration after the fact, not an observation-time pin.

## 2. Evidence per clause

### 2.1 "the isolated round-27 oracle" — OVERSTATED

Three concrete mismatches, all in receipts:

1. **Pins.** `.ufo/waves/round-27/harness/oracle.py:26-29` pins `TINYWL_SHA = 227a74af…` and
   `LIBWLR_SHA = 1f3d7036…`; `check_build()` (`:48-56`) raises `SetupError` on any mismatch. The seat's
   receipts record `tinywl_sha 273151bd…` (`receipt-headlesshost.json:480`) and
   `libwlroots_sha e6dfde74…` (`:209`). The pinned round-27 harness would **refuse** this build
   (`receipts/client-and-apparatus.txt`). The w1 report says so (§5); the entry does not.
2. **The pinned layout maps nothing.** `receipt-mwatch.json` `monitor_timeline` is
   `[{"names": [], "t": 0.0}]` and `receipt-host.json` `clients_raw_at_fail` is `[]` — in the plain
   layout the nested Hyprland keeps no output. The seat repaired it by creating a headless output on
   the nested instance and forcing the client to `WAYLAND_DISPLAY=wayland-1` (w1 §3;
   `receipts/binary-and-negatives.txt`). So the pinned apparatus cannot produce this observation at all.
3. **Config tree.** The round-27 oracle's semantics include the host's config roots
   (`.config/hypr`, the omarchy theme/default hypr dirs, the toggles dir: `oracle.py:34-35`, copied at
   `:65`). The adaptation writes a bare `hyprland.conf` that only `source`s the rule file plus the
   ecosystem/debug blocks (`oracle-gkeep.py:78-84`). The observation therefore tests the three rule
   lines alone — which the clause "under the host's three rules" correctly states — but not under an
   apparatus whose defining property is the host config tree.

Impact: the *numbers* are unaffected; the *label* invites a reader to treat the observation as the
pinned harness's result and as host-config-wide. Both are not what ran.

### 2.2 Nested Hyprland, never the host session — SUPPORTED

`receipt-headlesshost.json:481-501` (server-reported `version/tag/commit/abiHash`), `:207`
(instance signature), and the sandbox command (`--unshare-all`, `--clearenv`, private
`XDG_RUNTIME_DIR`, `--tmpfs /run`) in the same receipt. Nested signatures differ from the host's live
one (`receipts/identity.txt`).

### 2.3 "a client with that app id" — literal SUPPORTED, under-disclosed

`"class": "org.omarchy.gkeep"` and `"initialClass": "org.omarchy.gkeep"`
(`receipt-headlesshost.json:19` and `:29`). But the client is `gkeep-shm.c`, a minimal xdg-shell shm client:
one 200x200 buffer (defaults at `gkeep-shm.c:116`, created at `:135-141`), `set_app_id`/`set_title` (`:150-151`), and **no size request**
(`:152-159`). The entry's §4 is about whether the rule or the *app* sets 420x500, and the app calls
`set_default_size(420, 500)` (`gkeep-ui-excerpt.py:33-34`). A reader who takes "a client with that app
id" for the app will over-read clause 8 (§2.8).

### 2.4 The observation itself — SUPPORTED exactly

- `"floating": true` — `receipt-headlesshost.json:21`; `"size": [420, 500]` — `:36-39`;
  `"class": "org.omarchy.gkeep"` — `:19`; `"at": [270, 20]`.
- The single-line quote in `20-observation.txt` parses to exactly the receipt's `clients[0]`
  (byte-for-byte value equality; `receipts/observation.txt`).
- `rules_sha` `3726e488…` — `:439`, equal to the pinned and live host rule file (`receipts/identity.txt`).
- Hyprland's own map line `window size: [420.00000, 500.00000]` is present inside
  `receipt-headlesshost.json:sandbox_log_tail` (`receipts/observation.txt`), and the client was
  configured `w=420 h=500` (`client_log`, `:7`).
- Repeatability: four sandboxes (`headlesshost`, `host-r1..r3`) with four distinct instance
  signatures, four distinct run dirs, all `[420, 500]`, `floating=True`, `at=[270, 20]`
  (`receipts/observation.txt`). The `at` values are the centring arithmetic on the 1920x1080@2
  (960x540 logical) headless output: `(960-420)/2=270`, `(540-500)/2=20`; the controls' `at` values
  match the same formula (`size300` `[330,120]`, `floatonly` `[380,170]`).
- `20-observation.txt` and `10-cases.txt` agree with the receipts field for field.

### 2.5 "the same client" — OVERSTATED

The isolating control that licenses "the rule is the origin" did **not** run the same client binary as
the headline case:

- `receipt-headlesshost.json:8` `client_sha = 227cf419…` (also `host-r1..r3`, `nofloat`, `size300`);
- `receipt-floatonly.json:8` `client_sha = a3319a74…` (also `nomatch`, `minsize`);
- rebuilding the seat's kept `gkeep-shm.c` with the seat's own command reproduces **`a3319a74…`**
  (`receipts/client-and-apparatus.txt`), i.e. the kept source is the *control* build.

The headline build's source is not kept, and the seat's claim that the only delta is the optional
`--min-size` flag cannot be verified: deleting that block from the kept source (two variants) yields
`b06f3510…` and `5482381a…`, neither equal to `227cf419…` (`receipts/controls-lines.txt`). The two
builds behave identically in the flag-less cases (both log `buffer=200x200`, no `CLIENT_MIN_SIZE`), so
the sizes and the conclusion stand; the word "same" does not.

Size claim itself: `receipt-floatonly.json:36-39` = `[200, 200]`, `:21` `floating: true`, `:7`
`TOPLEVEL_CONFIGURE w=200 h=200` — supported.

### 2.6 `size 300 300` — SUPPORTED

`receipt-size300.json:36-39` = `[300, 300]`, `:21` `floating: true`, `:431` `rules_sha 450d3917…`
(the size line changed to `300 300`), `client_log` `TOPLEVEL_CONFIGURE w=300 h=300`.

### 2.7 `float on` removed — SUPPORTED

`receipt-nofloat.json:21` `floating: false`, `:36-39` `[918, 498]`, `:431` `rules_sha 12ee0172…`.
The w1 table's gloss "the size rule is never read for a tiled window" is a source inference
(`Hyprland-DefaultFloatingAlgorithm.cpp:56`, `Hyprland-WindowTarget.cpp:70-71`, entry §2) rather than
something this case observes; the observation only shows the rule was inert.

### 2.8 "the rule, not the client, is the origin of 420x500" — SUPPORTED as scoped, not transportable

Within the oracle: the client requests nothing and the rule-less control reports the client's own
200x200, so the 420x500 cannot come from the client. True as written.

But the sentence follows the entry's own statement that "a 420x500 report alone cannot say which of
the two set it", and the oracle cannot repair that for the app: the app *does* request 420x500, and
`floatonly` shows that with no size rule the client's own size is what the report carries. A client
whose own default were 420x500 would therefore report 420x500 with no rule; the oracle's result cannot
separate rule from app default. The `minsize` control does not close this either: `set_min_size` is a
minimum, not the app's default; its log shows `CLIENT_MIN_SIZE 800x700` then
`TOPLEVEL_CONFIGURE w=420 h=500` with the client still on its 200x200 buffer
(`receipt-minsize.json:7`). The host-side question stays UNK, as entry §5 says.

## 3. Defects in the receipts and seat prose (not overstatements of the observation)

- **D1 `clients_repeat_equal: false` is a broken comparison.** It is `false` on every positive receipt
  (`receipt-headlesshost.json:55`) while the parsed `clients` and `clients_second` are equal in every
  case (`receipts/observation.txt`). Cause: `oracle-gkeep.py` sets `rec["clients_repeat_equal"] = out == prev`
  where `prev` is `json.dumps(filtered_array, sort_keys=True)` and `out` is the raw `clients -j` text.
  Nobody should read the flag as instability (the entry does not); fix by comparing parsed objects.
- **D2 wrong client locator in the seat's own prose.** `20-observation.txt:24` cites
  `gkeep-shm.c:156-164` for "sets app_id and title, attaches a 200x200 shm buffer and commits", but
  `set_app_id`/`set_title` are at 150-151, attach/commit at 157/159, and 156 is the min-size block's
  closing brace; `.ufo/waves/round-43/w1/ExecOracleGkeep.md:46` cites `152-164` for the same sentence.
  Correct range: 150-159 (locators saved in `receipts/locators.txt`).
- **D3 the evidence is cited from a commit that does not contain it.** Entry §4 landed at data commit
  `1959770` and cites `.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt` and `10-cases.txt`,
  but that commit's round-43 tree has 96 files (66 `ctl/`, 10 `fetch/`, 13 `receipts/`, the two
  registrations and the w1 spec/dispatch files) and exactly one file under `w1/`
  (`w1/swarm-registry.json`); `git cat-file -e 1959770:.ufo/waves/round-43/w1/ExecOracleGkeep.md`
  fails. The 48 seat files arrive at HEAD `2a3707c` ("w1 evidence"); the report there equals disk
  (`c3c87c4a…`). The evidence is real and unmodified, but a reader resolving entry citations at the
  scored revision sees nothing.

## 4. Strongest counterexample (one line)

The single control that is supposed to prove "the rule, not the client, is the origin" was run with a
different client binary than the case it explains — `floatonly` `a3319a74…` vs `headlesshost`
`227cf419…` (`receipt-headlesshost.json:8`, `receipt-floatonly.json:8`), the kept source rebuilds to
the former (`receipts/client-and-apparatus.txt`), and the latter's source is not kept and is not the
kept source minus the `--min-size` block (`receipts/controls-lines.txt`). Everything else the seat
reports reproduces.

## 5. Impacted axes and the smallest safe correction

- Axis **coverage** (C2): the entry's §4 INF prose and the lesson's mistake ledger. Not the C2
  predicate — `c2-r43-gkeep-entry-v2.py` contains no reference to this seat (`receipts/client-and-apparatus.txt`),
  and v2's residual already says the oracle is "reported, not scored".
- Axis **operability** (C1): untouched. `tools/mado-geometry.py`, its counter and the live
  `NO_MATCHING_CLIENT` receipt are not involved.
- No axis is harmed. This finding is a prose/provenance correction, not grounds to re-score C2.

Smallest safe correction (replace the last part of entry §4, keeping the numbers):

> In an *adaptation* of the round-27 bubblewrap oracle (round-26 tinywl patch; wlroots 0.20.2 rebuilt —
> tinywl `273151bd…`, libwlroots `e6dfde74…`, so not the round-27 pins; a headless output created on
> the nested instance; the client forced to the nested `WAYLAND_DISPLAY`), a purpose-built shm client
> carrying that app id **that requests no size** (one 200x200 buffer) reported `"size": [420, 500]`,
> `"floating": true` under the host's three rules; without the size rule it reported 200x200, with
> `size 300 300` it reported 300x300, and without `float on` it was tiled. That shows the rule acting
> on a client that requests nothing; it does not separate the rule from gkeep's own
> `set_default_size(420, 500)`, so a 420x500 report from a real gkeep window remains unobserved (UNK).

Plus three mechanical fixes: name the client sha per case (or rerun the controls with one binary);
repair `clients_repeat_equal`; correct the `gkeep-shm.c` locator to 150-159 and date the w1-evidence
citation to commit `2a3707c`.

## 6. Evidence files in this seat

```
receipts/identity.txt            rule-file shas (pin, seat copy, live host), diff, host version,
                                 host binary sha, host signature, host rules mentioning gkeep/875
receipts/observation.txt         per-case size/floating/class/at/sha, quote==receipt, repeat flag,
                                 map line, version json, tinywl/libwlroots shas
receipts/controls-lines.txt      the exact size/class/floating lines of six receipts; rebuild of the
                                 kept client; the two minus-min-size variants and their shas
receipts/client-and-apparatus.txt  rebuild sha, round-27 pins and check_build, round-27 ROOTS,
                                 adapted config write, C2 counter's (absent) oracle references
receipts/binary-and-negatives.txt  receipt hash fields, no compositor-binary sha, boot line/PATH bind,
                                 mwatch timeline, host fail dump
receipts/locators.txt            entry §4 lines, gkeep-shm.c 148-160, seat-doc locators, receipt anchors
```

Checks used only read verbs on the host: `hyprctl version` and grepping `~/.config/hypr`. The one
build was `gcc -O2` of the seat's own client source in
`/fast/scratch/hyaku/mado-r43/CritOracleClaim/` (gcc 16.2.1, wayland-scanner 1.26.0, both
pre-existing). No tool was installed; no pacman transaction; scratch deleted at seat end.
