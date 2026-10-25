# ScoutK1K2Held — held-coverage map for the assimilation candidates K1/K2

Seat: `ScoutK1K2Held` (scout, round 40 w1). Date: 2026-10-25.
Candidates examined (read-only): `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-bar-producers-r28.md`
(K1) and `host-producer-outputs-r29.md` (K2).
Lane corpus checked (the five named in the task): `corpus/knowledge/waybar-walker-semantics.md`,
`waybar-walker-plane.md`, `config-health-report-r3.md`, `idle-lock-offered-in-the-bar-r15.md`,
`waybar-observation-boundaries-r16.md`. Secondary lane holds named where they decide a row:
`config-drift-r12.md`, `omarchy-drift-watch.md`, `waybar-module-text-route-r25.md`.

No file was written outside this seat directory. No package transaction, no compositor verb, no
mutating git/jj. Tooling: none installed (no tool needed beyond `grep`/`sha256sum`/`git
--no-mutating read`).

---

## 0. Verdict in one paragraph

Both candidates are **largely redundant with what the lane already holds**: K1 (r28) restates a
producer map the lane has held per-module since round 3 (`waybar-walker-semantics.md:119-149`,
`waybar-walker-plane.md:67-112`), and K2 (r29) restates probe semantics and outputs the lane
recorded as RUN payloads in the same file (`waybar-walker-semantics.md:137-140,149`). **Four
things are genuinely new ground**: (a) the `custom/gkeep` producer row and its *signal 12*
wiring, absent from the entire lane corpus; (b) the upstream-vs-host byte identity (the lane's
held "5114" figure is a *host backup* that is byte-identical to upstream `v3.8.4`'s
`config/waybar/config.jsonc`); (c) the AI-usage producer's `AI_USAGE_CACHE` override and the
gkeep shim's non-installed, `sys.path`-injected package; (d) the *upstream* custom-module set
(8 elements). **Three defects in the candidates must be fixed before admission**: K1's §1 INF
counts contradict K1's own table (7/4/3, not 6/5/2); K1 §2's "that state is currently off" and
K2 §1's "currently" claims have rotated (hypridle runs today); K2's `updated_at` quote is the
exact volatile timestamp the lane refused in round 39 (a different `S224`, same bytes), so
re-admitting it under a new id would re-admit a refused quote.

---

## 1. K1 — `host-bar-producers-r28.md` (fact-by-fact)

| # | Fact in K1 | Held? | Where (lane `file:line`) | New ground? |
|---|---|---|---|---|
| K1-1 | "Ten elements on this bar are `custom/*` modules; each declares a producer; producers fall into three kinds" | **partial** | `waybar-walker-semantics.md:119-149` (9 custom elements + drawer at `:146`), `:77-79` rails; census of 18 top-level / 20 with drawer children in `config-drift-r12.md:35-36` (outside the five named files) | **Yes**: the count *ten* (incl. `custom/gkeep`) and the three-kind taxonomy (no-producer pure-format / scripted / compositor-fed) are not stated in the five named files; `custom/gkeep` is absent from them entirely (`grep -n gkeep` on the five files → only `config-drift-r12.md`) |
| K1-2 | Producer row `custom/update` → `omarchy-update-available`, text, interval 21600 | **yes** | `waybar-walker-semantics.md:136`; `waybar-walker-plane.md:68`; signal 7 at `plane.md:90-93`, `semantics.md:173-176` | no (return-type *text* for `custom/update` is not stated by the lane; the host config has no `return-type` key for it — trivial) |
| K1-3 | `custom/weather` → `$OMARCHY_PATH/default/waybar/weather.sh`, json, 60 | **yes** | `semantics.md:135`; `plane.md:72` (json + interval 60) | no |
| K1-4 | `custom/screenrecording-indicator` → `indicators/screen-recording.sh`, json | **yes** | `semantics.md:138`; `plane.md:112`; `plane.md:107` (stock path) | no |
| K1-5 | `custom/idle-indicator` → `indicators/idle.sh`, json | **yes** | `semantics.md:139`; `plane.md:108`; `idle-lock-offered-in-the-bar-r15.md:37-40`, `:16` (gate-quote) | no |
| K1-6 | `custom/notification-silencing-indicator` → `indicators/notification-silencing.sh`, json | **yes** | `semantics.md:140`; `plane.md:110` | no |
| K1-7 | `custom/voxtype` → `omarchy-voxtype-status`, json | **yes** | `semantics.md:137`; `plane.md:424` | no |
| K1-8 | `custom/omarchy` — no producer, pure format, click opens a terminal | **yes** | `semantics.md:119` ("none — no `exec`", R → `xdg-terminal-exec`); `plane.md:67` | no |
| K1-9 | `custom/expand-icon` — no producer, pure format | **yes** | `semantics.md:147` ("static"); `plane.md:146` (drawer leader) | no |
| K1-10 | `custom/gkeep` → `~/.local/bin/gkeep waybar`, json, interval 30 | **no** | `grep -rn "gkeep waybar"` over `corpus/` → **0 hits**; `config-drift-r12.md:35,:65` hold only that the *module* was inserted into `modules-right` and that the installer writes it | **Yes** — the producer wiring is unheld. Host bytes today: `~/.config/waybar/config.jsonc:236-245` (`exec`, `return-type: json`, `interval: 30`, **`signal: 12`**, `on-click: … gkeep capture`, `on-click-right: … gkeep list`) |
| K1-11 | `custom/ai-usage` → `~/.local/bin/ai-usage waybar`, json, 60 | **yes** | `semantics.md:149`; `plane.md:80-85` (symlink → `~/Projects/omarchy-usage-tray/bin/ai-usage`) | no |
| K1-12 | "host config = omarchy stock file plus local edits; **upstream `v3.8.4` file is 5114 B vs host 6354 B**" | **partial / mis-labelled** | The five named files carry the **stale** host pin 6068 B / 249 L: `plane.md:19,:295,:401-402`, `semantics.md:443`, `config-health-report-r3.md:189,:643`. The current host pin (260 L / 6 354 B / sha `a408a33d…`) is held in `config-drift-r12.md:33-34`. The number **5114** *is* in the lane but as the size of the host backup `config.jsonc.bak.1791314470` (`plane.md:297`) — not as the upstream file | **Yes.** Measured today: upstream `v3.8.4:config/waybar/config.jsonc` = **5114 B / 182 L**, sha256 `ff387b21ab51f4d5c4752142de31d1cfb2e8a459647a8f84849a522aee57c061` — **byte-identical** to `~/.local/share/omarchy/config/waybar/config.jsonc` **and** to `~/.config/waybar/config.jsonc.bak.1791314470`. So the lane's "5114" row is upstream stock wearing a backup's name; the drift is stock → 6354 B. Neither the upstream blob's sha nor this identity is held |
| K1-13 | "all eight omarchy custom modules appear in both; host additionally declares `custom/gkeep` and `custom/ai-usage`" | **partial** | Host-side additions held: `config-drift-r12.md:35` (`custom/gkeep` inserted before `custom/ai-usage`), `plane.md:281-282` (ai-usage is a local addition), `plane.md:80` ("is a local extension") | **Yes** — the *upstream* custom-module set (8 keys: `expand-icon`, `idle-indicator`, `notification-silencing-indicator`, `omarchy`, `screenrecording-indicator`, `update`, `voxtype`, `weather`) is nowhere in the lane; the five named files list only the host's modules |
| K1-14 | INF "eight of ten custom elements are stock; the two host-local producers are the only ones without an upstream counterpart" | **partial** | Local-edit drift list `plane.md:280-290`; gkeep provenance `config-drift-r12.md:109` ("operator-applied"); ai-usage local extension `plane.md:80` | Mostly derivable; the "upstream counterpart" framing is new but rests on K1-13's new upstream set |
| K1-15 | "remaining elements are standard Waybar modules (clock, clock#secondary, group/tray-expander, bluetooth, network, pulseaudio, cpu, battery) plus the single built-in Hyprland element `hyprland/workspaces`" | **yes** | `plane.md:51-58`; `semantics.md` §3.1-3.3; compositor-fed element held in `waybar-module-text-route-r25.md` | no |
| K1-16 | INF "the bar has **six** JSON producers, two pure-format elements with no producer, one element fed by compositor events … five of the six run scripts with no poll interval … only two poll on a timer" | **no — and self-contradictory** | not held anywhere | **Defect + new ground.** K1's own table lists **7** json rows (weather, screenrecording, idle, notification-silencing, voxtype, gkeep, ai-usage) and 3 "text" rows (omarchy, expand-icon, update). Measured from the host bytes today: json **7**; of those **4** have no `interval` (screenrecording, idle, notification-silencing, voxtype) and **3** poll on a timer (weather 60, gkeep 30, ai-usage 60). Correct counts are 7 / 4 / 3, not 6 / 5 / 2 (the 5+2 split also exceeds its own "six"). The "one element fed by compositor events" (`hyprland/workspaces`) part **is** held |
| K1-17 | "`custom/idle-indicator` runs `idle.sh`, byte-identical to omarchy's stock script at `v3.8.4`" | **partial (held in substance)** | `plane.md:107` ("all three are stock `$OMARCHY_PATH/default/waybar/indicators/*.sh`"); omarchy checkout is exactly tag `v3.8.4` at HEAD — `omarchy-drift-watch.md:71-72`, `semantics.md:25` | Explicit upstream-blob identity is new evidence I produced today: sha256 of the three host indicator scripts == sha256 of `git show v3.8.4:default/waybar/indicators/{idle,screen-recording,notification-silencing}.sh` (`6d8d2c11…`, `28491cd3…`, `312900d1…`) |
| K1-18 | Quotes `if pgrep -x hypridle >/dev/null; then` and the `echo '{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}'` | **partial** | Probe semantics held at `plane.md:108`, `semantics.md:139`, `idle-lock-offered-in-the-bar-r15.md:37-40` | The *upstream* quote locations are new: both lines exist verbatim in upstream `v3.8.4` `default/waybar/indicators/idle.sh` at lines **3** and **6** (read via `git show v3.8.4:…`) |
| K1-19 | INF "the bar's idle element is a *process probe*, not a compositor-state read … a direct witness of the idle plane's runtime state" | **yes** | `plane.md:113-116` (INF: "bar state for idle/notifications/recording is a *process or Mako-mode probe*, not a bar-owned flag"); `semantics.md:139`; `idle-lock-offered-in-the-bar-r15.md:37-40` | no |
| K1-20 | INF "(that state is currently 'off')" | **stale / rotating** | Historically held as *absent*: `config-health-report-r3.md:285-300` (F1), and `idle-lock-offered-in-the-bar-r15.md:76-84` (E2 withdrew "never taken it"; records the toggle-off at 2026-10-23T19:24:38 and a restart at 22:14:11) | **Yes — and the claim is false today.** Measured: `pgrep -x hypridle` → **1680**, started `Sun Oct 25 13:36:23 2026`. The idle chip now takes the `{"text": ""}` branch (`idle.sh:3-4`), not the disabled glyph. Must be re-measured, not copied |
| K1-21 | UNK "the contents of the five JSON producers' outputs were not captured; no producer was executed" | **no — the lane is ahead of this** | `semantics.md:138` (screenrecording RUN `{"text": ""}`), `:139` (idle RUN `{"text": "󱫖", "tooltip": "Idle lock disabled", "class": "active"}`), `:140` (notification RUN `{"text": ""}`), `:137` (voxtype RUN `{"alt": "", "tooltip": ""}`), `:149` (ai-usage RUN payload) and `:436-438` ("Executed scripts were pure-read producers only: the three indicator scripts, `omarchy-voxtype-status`, `ai-usage waybar` (cache-only by its own argparse help)") | no — the candidate's open item is already closed by lane-held observations. Only `custom/gkeep`'s output remains unread in the lane (still open, and cheaply decidable — see §3) |

---

## 2. K2 — `host-producer-outputs-r29.md` (fact-by-fact)

| # | Fact in K2 | Held? | Where (lane `file:line`) | New ground? |
|---|---|---|---|---|
| K2-1 | screen-recording chip is a process probe; quote `if pgrep -f "^gpu-screen-recorder" >/dev/null; then` | **yes** | `plane.md:112`; `semantics.md:138` (RUN `{"text": ""}`) | no (the quote's upstream location is `v3.8.4` `screen-recording.sh:3`, verified today) |
| K2-2 | notification chip is a single read-only query; quote `if makoctl mode \| grep -q 'do-not-disturb'; then` | **yes** | `plane.md:110`; `semantics.md:140` (RUN `{"text": ""}`, "makoctl mode → default") | no (`v3.8.4` `notification-silencing.sh:3`, verified today) |
| K2-3 | AI-usage producer declares its own contract: docstring `"""Cache AI CLI usage windows and render a Waybar chip. waybar reads cache only."""` | **partial** | `semantics.md:149` cites `ai-usage:2` as the cache-only anchor and quotes the argparse help "print Waybar JSON from cache only" | The verbatim docstring line is not in the lane's text (same anchor, `ai-usage:2` — verified present in the host file today) |
| K2-4 | measured: no `gpu-screen-recorder` process running | **yes** | `semantics.md:138` ("RUN `{"text": ""}` → inactive (no recorder running, `pgrep` empty)"); re-verified today: `pgrep -f "^gpu-screen-recorder"` → no match | no |
| K2-5 | measured: `makoctl mode` reports `default` | **yes** | `semantics.md:140`; `plane.md:220`; `config-health-report-r3.md:451`; re-verified today: `makoctl mode` → `default` | no |
| K2-6 | measured: the AI-usage cache's own metadata reads `"updated_at": "2026-10-23T22:52:44Z",` | **no — refused-grade, and the refusal is already held twice** | Not held as a fact; the **refusal** is held: `corpus/lessons/round-32.md:111` ("1 ABSENT as quoted (S224, rotating `updated_at`)"), `corpus/lessons/round-34.md:62-64` ("`/home/vgpnk/.cache/ai-usage/status.json` is a transient host cache file, not a source; its `updated_at` quote is stale on every read"), `corpus/lessons/round-39.md:73`; seat verdict `.ufo/waves/round-39/w1/ExecQuarantineSlice/verdicts.md`, S224 row: "Current bytes contain only `"updated_at": "2026-10-25T19:05:31Z"` … quoted value appears nowhere … Volatile timestamp rotated; row not appendable". Today: `~/.cache/ai-usage/status.json:3` = `"updated_at": "2026-10-25T20:47:13Z",` — grep for the quoted value → **0 hits** | **No admissible ground.** Also an **id hazard**: the package's `S241` (AI-usage cache) and the register's refused `S224` are the same bytes under different ids; K2 re-introduces a refused quote under a fresh id. Fix per the round-40 registration's D2 (over-label) item: the lane's lesson label "fabrication class" should be corrected to "rotated volatile telemetry", and K2's cache row must be re-sourced with a fresh value plus a snapshot, or dropped |
| K2-7 | INF "three of the bar's five JSON producers currently render empty text (recorder, do-not-disturb, and the idle chip's counterpart)" | **partial — count wrong, contents partly stale** | `semantics.md:138` (recorder `{"text": ""}`), `:140` (DND `{"text": ""}`), `:139` (idle `{"text": "󱫖", …, "class": "active"}`) | **Defect**: the producer count is 7, not 5 (see K1-16), and the idle chip today renders `{"text": ""}` because hypridle runs (K1-20) — so "three render empty" is now arguably right for a different reason. The three *payloads* are held |
| K2-8 | INF "the AI-usage chip is the fourth decidable case: its text is a pure function of a cache file that names its own freshness, so a stale chip is distinguishable from a correct one" | **partial** | `semantics.md:149` (chip is cache-only; cache `~/.cache/ai-usage/status.json`), `:362` ("chip is cache-only; staleness is rendered as a class, not an error", `STALE_AFTER_SEC = 20*60`), `:218` (`.stale` opacity 0.55) | **Yes**: the mechanism "the cache names its own freshness" (its `updated_at` field) is not held — the lane holds only the derived class/timeout, not the cache-side freshness stamp |
| K2-9 | §2 "the `custom/gkeep` producer is a shim onto an **installed** package" — quote `from gkeep.cli import main` | **no** | not in the lane corpus (`grep -rn "from gkeep"` → 0 hits; `config-drift-r12.md` holds the *installer*, not the producer) | **Yes, plus a correction.** Measured today: `~/.local/bin/gkeep` is a 36-byte symlink → `~/Projects/gkeep/bin/gkeep`; the quote is at `bin/gkeep:9` (the shim injects `ROOT` into `sys.path` at `:5-7`). The package is **not installed**: `python3 -c "import gkeep.cli"` → `ModuleNotFoundError`; `importlib.metadata.version("gkeep")` → `PackageNotFoundError`. So "installed package" is wrong — it is a source checkout reached by `sys.path` injection |
| K2-10 | §2 "the `custom/ai-usage` producer is a self-contained Python program (**134 777 B**) that resolves its cache path from the environment" — quote `return Path(os.environ.get("AI_USAGE_CACHE", Path.home() / ".cache/ai-usage/status.json"))` | **partial / stale figure** | Lane holds the symlink and target path: `plane.md:83-84`; the default cache path: `semantics.md:149` | **Yes**: the `AI_USAGE_CACHE` override is **not** in the lane (`grep -rn AI_USAGE_CACHE corpus/` → 0 hits; the value is at `ai-usage:64` today). The byte figure **134 777 B is stale**: the target is now **114 246 B / 3 038 L** (`git log` shows `7a4d56f` 2026-10-25 "Remove the Token Plan and Charm Hyper meters (1.12.0)"); 134 777 B was revision `121c1e1` (2026-10-22) — `git show 121c1e1:bin/ai-usage \| wc -c` = 134777 |
| K2-11 | §2 INF "the two host-local elements are the only producers with no upstream counterpart; `gkeep` is a thin entry point whose behaviour lives in an installed Python package; `ai-usage` is a self-contained program whose rendered state is a cache file" | **partial** | ai-usage local extension: `plane.md:80-85`, drift item `plane.md:281-282`; gkeep operator-installed: `config-drift-r12.md:109` | Partly new (see K2-9/K2-10); the "installed package" phrase is the inaccurate part |
| K2-12 | §3 UNK "the `custom/weather` producer's live icon was not captured (network)" | **yes** | `plane.md:343-344` (unknown #3); `semantics.md:135` ("**not run** (network); value UNK"); `config-health-report-r3.md:453` ("`custom/weather` live render unread") | no |
| K2-13 | §3 UNK "the `custom/update` and `custom/voxtype` producers' current outputs were not determined — their scripts were located but not read" | **no — the lane is ahead** | update producer read: `semantics.md:136` (quotes `omarchy-update-available:5` `git ls-remote`, and the offline error text at `:6-9`); voxtype producer read and re-run: `semantics.md:137`, `:436-438` | no — the candidate's open item is already closed in the lane for voxtype; only update's live remote-tag value remains genuinely open |

---

## 3. Genuinely new ground, ranked (what an assimilated entry could add)

1. **The `custom/gkeep` producer row and its signal-12 wiring** — entirely unheld. Host bytes
   `~/.config/waybar/config.jsonc:236-245`; producer `~/.local/bin/gkeep` (36-byte symlink →
   `~/Projects/gkeep/bin/gkeep`, quote at `:9`); the producer is offline-decidable —
   `~/Projects/gkeep/gkeep/waybar.py` reads only `~/.local/share/gkeep/notes.json`
   (mode 0600, `version` 1, `notes` array length 10 measured today, bodies not read).
   The bar's own signal-12 producer is `~/Projects/gkeep/gkeep/ui.py:122-132`
   (`pkill -<SIGRTMIN+12> waybar`). **The lane's signal-bus tables stop at 11**
   (`plane.md:90-93`, `semantics.md:173-176`); `grep -rn "signal 12|RTMIN+12|SIGRTMIN+12" corpus/`
   → **0 hits**. That is a real hole in the held surface, independent of K1/K2.
2. **Upstream-vs-host byte identity** — upstream `v3.8.4:config/waybar/config.jsonc` = 5114 B /
   182 L / sha256 `ff387b21…`, byte-identical to the checkout copy *and* to the host backup
   `~/.config/waybar/config.jsonc.bak.1791314470`; host today 260 L / 6354 B / sha `a408a33d…`
   (matches `config-drift-r12.md:34`). The lane holds the numbers but not this identity, and
   its five named files still carry the superseded 6068 B pin.
3. **The upstream custom-module set (8 keys)** — the only lane-held "upstream" fact is the file
   path (`plane.md:271-273`, `semantics.md:91-92`); the upstream module inventory is not held.
4. **The AI-usage producer's environment override** (`AI_USAGE_CACHE`, `ai-usage:64`) — unheld;
   it is the one place the chip's data source can be redirected, so it belongs with the cache
   fact at `semantics.md:149`.
5. **The AI-usage producer's current size** — 114 246 B / 3038 L at `7a4d56f` (2026-10-25), not
   K2's 134 777 B. Related: the lane's own ai-usage line anchors have drifted
   (`ai-usage:2534` → the argparse `waybar` help is now at `:2994`; `ai-usage:31`
   `STALE_AFTER_SEC` → now `:33`; `ai-usage:406-408` → the `omp usage --json` comment is now at
   `:409-413`). Any re-quote of that producer must re-anchor.

## 4. Defects to fix before any admission

- **D-a (K1 §1 INF)**: JSON-producer / interval counts contradict K1's own table — 7 json, 4
  without interval, 3 on a timer, not 6 / 5 / 2. Fix the prose or drop it.
- **D-b (K1 §2 INF, K2 §1 INF)**: "currently off" / "currently render empty text" are
  rotating claims; hypridle runs today (PID 1680, since 2026-10-25 13:36:23). The lane already
  holds the mechanism of that instability (`idle-lock-offered-in-the-bar-r15.md:76-84`).
- **D-c (K2 §1)**: the `"updated_at": "2026-10-23T22:52:44Z"` quote is the value round 39
  refused as rotated telemetry (`corpus/lessons/round-39.md:73`; the seat's own verdict file).
  Today's value is `2026-10-25T20:47:13Z`. Re-source with a fresh read plus a snapshot, or drop
  the row; do not re-admit it under `S241`. This is the round-40 registration's D2 item seen from
  the K2 side.
- **D-d (K2 §2)**: "installed package" for gkeep is wrong (not pip-installed; `sys.path`
  injection); and the ai-usage byte count 134 777 B is stale (114 246 B today).
- **D-e (K2 §1 / K1 §3)**: both candidates cite the host waybar config as a source; the lane's
  five named files still pin the *pre-gkeep* 6068 B file, so any admitted entry must cite the
  current 6354 B / `a408a33d…` bytes or the delta explicitly.

## 5. Unresolved / not decided here

- Whether K1/K2 should be admitted at all (scope-check + gate decision belong to the
  integrator); this seat only reports coverage.
- The lane's `SOURCES.md` id space: `S224`, `S228`, `S231`, `S237`-`S241` are **absent** from the
  lane registry (`grep -c "^| S224 " corpus/SOURCES.md` → 0; same for the others), so new rows
  could take those ids — but K2's `S241` (ai-usage cache) and the register's refused `S224` are
  the same bytes, so the id space and the refusal must be reconciled before appending anything.
- Whether `custom/gkeep`'s producer output may be quoted at all without running it: the file
  read is enough for the *form* (a local note count), but the rendered value is a second
  question; the package's own round-5 entry (`host-producer-current-outputs-r30.md`) already
  attempts it and is outside this seat's scope.

## 6. Commands run (read-only, all re-runnable)

```
sha256sum ~/.local/share/omarchy/config/waybar/config.jsonc \
          ~/.config/waybar/config.jsonc.bak.1791314470 ~/.config/waybar/config.jsonc
git -C ~/.local/share/omarchy show v3.8.4:config/waybar/config.jsonc | sha256sum
git -C ~/.local/share/omarchy show v3.8.4:default/waybar/indicators/{idle,screen-recording,notification-silencing}.sh | sha256sum
wc -lc ~/.config/waybar/config.jsonc ~/.local/share/omarchy/config/waybar/config.jsonc
pgrep -x hypridle ; ps -o pid,lstart,cmd -p 1680
pgrep -f "^gpu-screen-recorder" ; makoctl mode
sed -n '236,245p' ~/.config/waybar/config.jsonc ; cat -n ~/.local/bin/gkeep ; sed -n '1,9p' ~/Projects/gkeep/bin/gkeep
sed -n '64p;33p;2994p' ~/Projects/omarchy-usage-tray/bin/ai-usage ; wc -lc ~/Projects/omarchy-usage-tray/bin/ai-usage
git -C ~/Projects/omarchy-usage-tray show 121c1e1:bin/ai-usage | wc -c
grep -n updated_at ~/.cache/ai-usage/status.json
grep -rn "gkeep waybar|AI_USAGE_CACHE|signal 12|from gkeep" corpus/
```

No tool was installed; no package transaction ran; no compositor mutation was attempted; the
only compositor-adjacent calls were `pgrep`/`makoctl mode`/`git show` reads.
