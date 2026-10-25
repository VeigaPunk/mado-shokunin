# SKILL.md rows for `tools/mado-options.py --live` — additive draft (round 40, w1)

Seat: `ScrSkillTable`. Date: 2026-10-25. Lane: mado-shokunin at HEAD `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`
(`SKILL.md` sha256 `32edcb2e38ba56514dadd24ad62e426f613fc8a6fd541599248eca81da2adcc7`, 2006 lines,
last touched at `d40b35f90ad8bf630ad9404d25aeee1d9737f300`).

**Additive only.** Every block below is new text; no existing line of `SKILL.md` is edited,
reordered or renumbered. Insertion point: after `SKILL.md:189` (the last line of
`### Divergence vocabulary and severity taxonomy`, "…dispatcher behaviour is `[INF-docs]`
(nothing fired, MADO-R2-2 §1/§6.1)."), before the blank line `:190` and the
`## Safe-probe discipline — measure, don't mutate` heading at `:191`. Appending the two
subsections there keeps the routing/vocabulary material together; appending at end of file is
the alternative if the integrator prefers one append block.

**Precondition finding.** `grep -n 'mado-options' SKILL.md` at HEAD → **zero matches** (exit 1).
`SKILL.md` carries no `mado-options.py` row today, so the draft cannot extend an existing row
set and is written self-contained: it introduces the tool's three modes in one table (static,
`--getoption FILE`, `--live`) so the `--live` row is readable without a prior row.

---

## DRAFT — begin additive block

### Option table, static vs live — `tools/mado-options.py` (round-40 append)

The round-39 resolver (S219) answers *who declares this key*. Its `--live` mode (round 40, C1,
`PRED-C1-r40-v1`) answers *what the running compositor answers for this key*. Three modes, one
output shape: one JSON array on stdout, one row per key, sorted by `key`.

| Mode | Command (read-only) | What it prints | Use it when |
|---|---|---|---|
| static (default) | `python3 -I tools/mado-options.py --home DIR` | rows `{key, value, owner, layer, line, set}` — the last declarer per key across the `source =` graph | the claim is ownership/intent, or no compositor is reachable |
| `--getoption FILE` | `… --home DIR --getoption FILE` | the same rows + `agreement`, merged from a JSON mapping `key -> {value, custom_type, set}` captured earlier | you already hold a `getoption` dump (transcript, other host, pinned receipt) and must not touch the compositor now; the merge cannot prove the dump is current |
| `--live` | `… --home DIR --live [--hyprctl PATH] [--probe KEY]…` | the same rows + `live` (the compositor's native value as text; `null` for `config-only`) + `agreement` computed by native-form comparison | the *effective value now* is the claim and the run may query the compositor |

`--live` runs exactly one program, once per declared key: `HYPRCTL getoption -j KEY`
(`--hyprctl PATH` names the program, default `hyprctl`) — the compositor's own read verb and
nothing else: no `keyword`, `dispatch`, `reload`, `setprop`, `--batch`; the tool opens no socket
of its own and writes nothing under the config root. `--probe KEY` (repeatable) adds keys with no
declarer — `live-default` when the compositor answers, dropped when it answers `no such option`;
a probe naming a declared key is not queried twice. If `--getoption` and `--live` are both given,
`--live` computes the label last and its `live`/`agreement` fields win — prefer one mode.

| The claim you must settle | Route | Run (read-only) | Tag |
|---|---|---|---|
| Is the last declarer also the live value (shadowing proof) | live compositor | `python3 -I tools/mado-options.py --home $HOME --live`; read the `agreement`/`agreement*` rows | `[OBS]` |
| Does a key the tree never declares exist live (engine default / runtime state) | live compositor | same command + `--probe <key>` → `live-default`, `owner: null`, never attributed to a file | `[OBS]` |
| Is a captured dump still what the compositor answers | live compositor | run `--live` on the same tree and diff the `live` fields against the dump | `[OBS]` (the dump alone is a snapshot, not current) |
| Who declares this key / which layer wins in the files | file bytes | `… --home DIR` (static) | `[OBS]` |

Exit codes (full map, all modes; `--selftest` adds exit 1). Signatures are the literal stderr
prefixes the tool emits; the `--live` failure is *named by key*:

| Exit | Signature (stderr) | Meaning | The check that settles it |
|---|---|---|---|
| 0 | — (JSON array on stdout) | table produced; `--live` exits 0 only when every declared key got a valid native reply or `no such option` | `… \| python3 -c 'import json,sys; print(len(json.load(sys.stdin)))'` |
| 2 | `mado-options.py: invalid probe key ''`; argparse `error: --probe: expected one argument`; `error: --home DIR is required` | usage error — a hostile probe key (empty or starting with `-`) is refused **before any program runs**, so it never reaches argv | re-run with a plain `namespace:key`; confirm the compositor was not invoked |
| 3 | `mado-options.py: <path>: No such file or directory` (also a non-regular file, an unresolved `source =` glob, a glob match that is not a regular file) | named config-read failure — the tree, not the compositor | fix `--home` or the include chain; no compositor call is made |
| 4 | `mado-options.py: <file>: getoption JSON root must be an object` | `--getoption FILE` unreadable/malformed — not reachable from `--live` | re-capture the dump, or use `--live` |
| 5 | `mado-options.py: <key>: cannot run <prog>: [Errno 2] …`; `<key>: <prog> exited N`; `<key>: malformed reply from <prog>`; `<key>: unknown reply form from <prog>` | named `--live` compositor failure, **with the key** — the reply is neither one of the four native forms nor `no such option` | the key is in the message: check `hyprctl version` / the instance, then re-read that one key |
| 1 | `MADO_OPTIONS_SELFTEST: k/n passed` with k < n, plus `selftest FAIL: <check>` per failure | a selftest assertion failed | the tool's own fixtures, never the host |

Native reply forms (frozen capture `.ufo/waves/round-40/c1/native-capture.jsonl`, 70 lines —
int 44, float 5, str 8, custom 13): either one JSON object
`{"option": K, "set": B, "<form>": V}` carrying exactly one form of `int|float|str|custom`, or
the plain text line `no such option` (the compositor exits 0 on it) → label `config-only`. The
declared string is converted host-style before comparison: `int` per hyprlang v0.6.8
`configStringToInt` (`0x` hex, `rgba(rrggbbaa)`/`rgba(r,g,b,a)`, `rgb(rrggbb)`/`rgb(r,g,b)` as
ARGB, `true|on|yes` → 1, `false|off|no` → 0, signed decimal); `float` within 1e-6; `str` exact
after trimming; `custom` by the shape of the live string (gradient, CSS gap `a b c d`, font
weight `<N>`).

### Reading a live gradient row — angle inheritance (`agreement*` vs `mismatch`)

The host's gradient handler clears the colours on every declaration but sets the angle only when
a `deg` token is present, so a gradient redeclared WITHOUT an angle keeps the angle the previous
declarer left in that option (0 when no earlier declarer set one). The comparison uses that
inherited angle. A custom-form row whose live value ends in `deg` reads:

| Declared (last declarer) | Live (native) | Label | Reading |
|---|---|---|---|
| `rgba(33ccffee) rgba(00ff99ee) 45deg` | `33ccffee 00ff99ee 45deg` | `agreement` (1 declarer) / `agreement*` (>1) | own angle, colours equal |
| `rgb(e68e0d)`, an earlier declarer wrote `… 45deg` | `ffe68e0d 45deg` | `agreement*` | **not** drift: the colour equals and the angle is inherited from the shadowed declarer — this row is the shadowing proof |
| `rgb(e68e0d)`, no earlier `deg` anywhere | `ffe68e0d 0deg` | `agreement` | inherited angle is 0 |
| `rgb(ff0000)`, an earlier declarer wrote `… 45deg` | `ffe68e0d 45deg` | `mismatch` | the colour differs — real drift (S2), a matching angle does not rescue it |

Reading rules: (1) compare colours as lowercase, unpadded ARGB hex words — `rgb(e68e0d)` *is*
`ffe68e0d` (opaque alpha), never a second value; (2) never report an angle-only difference as
`mismatch` while an earlier declarer carried that angle — check the declarer chain first;
(3) `agreement*` requires an equal native value **and** more than one declarer; equal with one
declarer is plain `agreement`; (4) `set=false` on a declared key is `mismatch` even when the
value text matches; (5) the same native comparison covers gaps (`0` vs `0 0 0 0` is agreement,
not drift) and font weights (`bold` vs `700`).

Host reading, round-40 census over the 70 declared keys: 62 `agreement`, 8 `agreement*`,
0 `mismatch`, 0 `config-only`. With angle inheritance switched off, the same tree flips exactly
two rows to `mismatch` — `general:col.active_border` and `group:col.border_active`, both declared
`rgb(e68e0d)` and reading `ffe68e0d 45deg`. An implementation that ignores inheritance therefore
does not merely lose a label: it fabricates two drift findings on this host.

## DRAFT — end additive block

---

## Grounding for the draft (not part of the additive text)

| Claim in the draft | Evidence |
|---|---|
| `SKILL.md` has no `mado-options` row | `grep -n 'mado-options' SKILL.md` → no output, exit 1 (HEAD `e2b51d3`); headings scan (`grep -n '^#'`) shows no options section |
| `--live` runs only `getoption -j KEY`, once per declared key, no other argv | observed on the reference control `c1/ctl-ref-tool.py.txt` (sha256 `f96d9e0a…a08aa`) with a stub compositor in `/tmp`: `argv.log` held exactly `getoption -j general:border_size`, `… general:col.active_border`, `… general:gaps_out`, `… input:kb_layout` — one line per declared key, 4 keys / 4 calls |
| Exit 0 + row shape (`live` text, `null` for config-only) | same run: rc=0, rows `{…, "live": "2", "agreement": "agreement"}`; `config-only` row printed `"live": null` |
| Exit 2 on a hostile probe, no program run | `--probe ''` → rc=2, stderr `mado-options.py: invalid probe key ''`, stub log absent (program never ran); `--probe --foo` → rc=2 via argparse `error: --probe: expected one argument` |
| Exit 3 | `--home /nonexistent` → rc=3, `mado-options.py: /nonexistent/.config/hypr/hyprland.conf: No such file or directory` |
| Exit 4 | `--getoption bad.json` (`[1,2,3]`) → rc=4, `mado-options.py: …/bad.json: getoption JSON root must be an object` |
| Exit 5 (four signatures) | `--hyprctl /bin/false` → rc=5 `general:border_size: /bin/false exited 1`; `--hyprctl /nonexistent/hyprctl` → rc=5 `general:border_size: cannot run …: [Errno 2]`; stub printing `not json` → rc=5 `general:border_size: malformed reply from …`; stub printing `{"option":"x","set":true}` → rc=5 `general:border_size: unknown reply form from …` |
| Exit 1 signature | `c1/ctl-ref-tool.py.txt:1207` writes `MADO_OPTIONS_SELFTEST: %d/%d passed` and returns 1 when `passed < total`; passing run prints `MADO_OPTIONS_SELFTEST: 71/71 passed` (the reference's base assertion count) |
| `no such option` is the compositor's own text at exit 0 | live read-only `hyprctl getoption -j general:definitely_not_an_option` → `no such option`, `rc=0` |
| `col.active_border` reads `ffe68e0d 45deg` with `set: true` | live read-only `hyprctl getoption -j general:col.active_border` → `{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }`, `rc=0`; same line at `c1/native-capture.jsonl:21` (frozen, sha256 `1fe39c05…9b4b25`, present at freeze commit `5e7e885`) |
| Angle inheritance is what makes the row `agreement*`, not `mismatch` | stub fixture: `col.active_border` declared `rgba(33ccffee) rgba(00ff99ee) 45deg` then `rgb(e68e0d)`, live `ffe68e0d 45deg` → `agreement*`; a different colour `rgb(ff0000)` against the same live → `mismatch` |
| 62/8/0 census and the two-row flip with inheritance off | `w1/ExecLiveCensus/census-receipt.txt` (labels `agreement=62 agreement*=8 mismatch=0 config-only=0`; `variant-noinherit labels agreement=62 agreement*=6 mismatch=2`, flipped `general:col.active_border`, `group:col.border_active`) and `w1/ExecLiveCensus/live-out.json` (sha256 `cde4b2df…905462`, 70 rows, `Counter({'agreement': 62, 'agreement*': 8})`). **Provisional**: the receipt is an uncommitted w1 candidate whose `tool sha256 <TOOLSHA>` is still a placeholder, so the census is not yet evidence. |
| Native form census int 44 / float 5 / str 8 / custom 13 | computed from the frozen `c1/native-capture.jsonl` (70 lines) |

Not observed by this seat, therefore not asserted in the draft: the delivered
`tools/mado-options.py` behaviour. At my read time the lane tool still printed
`usage: mado-options.py [-h] [--home DIR] [--getoption FILE] [--selftest]` (no `--live`), and
`grep -c -- '--live' tools/mado-options.py` → `0`; the candidate at
`w1/ExecToolLive/mado-options.py` documents the same exit map (`:65-67`) but its `main()` had
not yet gained `--live` when I read it. The draft describes the frozen contract
(`registration.md` C1 + `quality/counters/c1-r40-live.py` docstring) as the reference control
realizes it; the integrator should re-read the delivered tool's `--help` and docstring before
appending, and may only need to adjust `--probe`/`--hyprctl` help wording.
