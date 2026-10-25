# ExecK2HostReads — host-side reads for K2 (mado round-40, w1)

Seat: leaf. Scope: read-only host capture of the two host-local bar producers and the bar config,
then a statement-by-statement re-derivation of the candidate K2
`merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md` against today's host state.
Compositor verbs used: `hyprctl version` only. No package transaction, no host mutation, no input
injection, no socket of my own. No tool installed (nothing needed installing).

## Files written (both inside the lane)

- `.ufo/waves/round-40/w1/ExecK2HostReads/host-reads.txt` — full capture, command + output, verbatim
  byte ranges, redaction statement.
- `.ufo/waves/round-40/fetch/host-k2-reads.txt` — the quotable subset (`[QUOTE-A..I]`, `[QUERY-1..5]`,
  `[PIN-1,2]`, `[CACHE-META]`), with every volatile timestamp excluded and marked `[NOT-QUOTABLE]`.
- this report.

## Captured state (2026-10-25)

| object | observation |
|---|---|
| `~/.config/waybar/config.jsonc` | 6354 B, 260 lines, 28 top-level keys, sha256 `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829` |
| `~/.local/bin/gkeep` | symlink (36 B) → `/home/vgpnk/Projects/gkeep/bin/gkeep`, 252 B, sha256 `c1b147a0…c748cfbf8` |
| `~/.local/bin/ai-usage` | symlink (52 B) → `/home/vgpnk/Projects/omarchy-usage-tray/bin/ai-usage`, 114246 B, sha256 `0ccd33ab…c50a0254` |
| `custom/gkeep` block | `exec="~/.local/bin/gkeep waybar"`, `return-type="json"`, `interval=30`, `signal=12` (config.jsonc:236-245) |
| `custom/ai-usage` block | `exec="~/.local/bin/ai-usage waybar"`, `return-type="json"`, `interval=60`, `signal=11`, `escape=false`, `exec-on-event=false` (config.jsonc:246-259) |
| `pgrep -f '^gpu-screen-recorder'` | no output, exit 1 |
| `makoctl mode` | `default`, exit 0 |
| `~/.cache/ai-usage/status.json` | 29865 B, mode `-rw-------`, sha256 `e7f45d27…b57dd0438f`; top-level keys `providers, selected, updated_at, version`; 12 provider keys; `updated_at` within 24 h (age 0.04 h) |

Supporting reads: `pgrep -a -x waybar` → `1683 /usr/bin/waybar`; `pgrep -a -x hypridle` →
`1680 /usr/bin/hypridle`; `command -v voxtype` → exit 1; `OMARCHY_PATH=/home/vgpnk/.local/share/omarchy`;
Hyprland 0.56.2 @ `efb50993780079460b0cbed1363e2166a2de1d9f`.

Redaction: `status.json` was opened for **key names only** — no provider value, no credential, no
token-shaped field was read out or printed. Producer heads contain no secret-shaped content.

## Statement-by-statement comparison with the candidate K2

| # | candidate statement | today | evidence |
|---|---|---|---|
| 1 | screen-recording chip is a process probe, quote `if pgrep -f "^gpu-screen-recorder" >/dev/null; then` | **still true** (verbatim at host copy line 3) | `…/indicators/screen-recording.sh:3`, sha256 `28491cd3…` |
| 2 | notification chip is one read-only query, quote `if makoctl mode \| grep -q 'do-not-disturb'; then` | **still true** (verbatim at host copy line 3) | `…/indicators/notification-silencing.sh:3`, sha256 `312900d1…` |
| 3 | ai-usage declares `"""Cache AI CLI usage windows and render a Waybar chip. waybar reads cache only."""` | **still true**, line 2 unchanged | `bin/ai-usage:2` |
| 4 | "no `gpu-screen-recorder` process is running" | **still true** | `pgrep -f '^gpu-screen-recorder'` → exit 1 |
| 5 | "`makoctl mode` reports `default`" | **still true** | `makoctl mode` → `default` |
| 6 | cache metadata reads `"updated_at": "2026-10-23T22:52:44Z",` | **changed — rotated**. A fresh value is present (age 0.04 h). This is exactly the round-39 closure failure: the quote is volatile and must be replaced by the property "`updated_at` within 24 h" | `[CACHE-META]` |
| 7 | INF: "Three of the bar's **five** JSON producers currently render empty text … the idle chip … instead shows 'Idle lock disabled' because no `hypridle` runs" | **changed, twice over**. (a) The config declares **7** modules with `"return-type": "json"` (weather, screenrecording-indicator, idle-indicator, notification-silencing-indicator, voxtype, gkeep, ai-usage) — "five" is not the config's number. (b) `hypridle` **is** running (pid 1680), so the idle chip today takes the then-branch `{"text": ""}` — empty, not "Idle lock disabled". The sentence is also internally inconsistent ("render empty text … which instead shows …"). Today three chips *do* render empty (recorder, notification, idle) but the stated cause for the third is wrong | parsed config; `pgrep -a -x hypridle`; `idle.sh:3` |
| 8 | INF: "`gkeep` is a shim onto an **installed package**" | **shim true, "installed" false**. The shim is 252 B and does `from gkeep.cli import main` (line 9), but `importlib.util.find_spec('gkeep')` is `None` and no site-packages copy exists: it resolves only because the shim inserts `/home/vgpnk/Projects/gkeep` into `sys.path`. It is a local source checkout, not an installed distribution | `bin/gkeep:5-9`; `find_spec('gkeep')` → None; no `site-packages/gkeep*` |
| 9 | OBS: "`ai-usage` is a self-contained Python program (**134 777 B**)" | **changed by drift, and the pin is the wrong kind**. 134777 B was exact at `121c1e1` (2026-10-22T14:54:30-03:00), the HEAD when the entry was read; today 114246 B at `7a4d56f` "Remove the Token Plan and Charm Hyper meters (1.12.0)" (2026-10-25T02:18:49-03:00). A byte size is a volatile pin; use sha256 or drop it | read-only `git -C /home/vgpnk/Projects/omarchy-usage-tray log/show` |
| 10 | OBS: cache path comes from the environment, quote `return Path(os.environ.get("AI_USAGE_CACHE", …))` | **still true**, verbatim line 64 | `bin/ai-usage:64` |
| 11 | INF: the two host-local elements are "the only producers with no upstream counterpart" | **still true** | no `gkeep`/`ai-usage` hit anywhere under `/home/vgpnk/.local/share/omarchy/`; the tree ships only `indicators/` + `weather.sh` |
| 12 | UNK: weather's live icon not captured — network helper | **still true** | `weather.sh:3` → `omarchy-weather-icon` curls `https://wttr.in?format=j1` |
| 13 | UNK: `custom/update` and `custom/voxtype` outputs not determined | **partly resolved**. voxtype: `command -v voxtype` exits 1, so `omarchy-voxtype-status` takes the else branch and renders `{"alt": "", "tooltip": ""}` — decidable offline. update: `omarchy-update-available` runs `git -C "$OMARCHY_PATH" ls-remote --tags origin` — network, still not decidable offline | `$OMARCHY_PATH/bin/omarchy-voxtype-status`, `…/omarchy-update-available` |
| 14 | UNK: "The `gkeep` package's own Waybar output was not read." | **now measured — the item closes**. `gkeep/waybar.py` (807 B, sha256 `655a5c5b…f225dfb3`) says `"""One-line JSON for a waybar custom module. Local count only."""`; `payload()` = `{"text": f"{ICON} {count}", …}` from `list_notes()` over `$XDG_DATA_HOME/gkeep/notes.json`. Offline-decidable, no network. Today `notes.json` holds a list of 10 notes (keys `body, created, id`), so the chip text is the icon plus `10` | `gkeep/waybar.py:1`; `notes.json` shape only |
| 15 | INF: the AI-usage chip's text is a pure function of a cache that names its own freshness, so stale ≠ correct | **still true** | `cmd_waybar()` reads `load_cache()` only; `cache_age_sec()` parses `updated_at`; `STALE_AFTER_SEC = 20 * 60` (line 33) adds the `stale` class |

Summary: of 15 statements — **9 still true**, **4 changed** (#6 rotated timestamp, #7 producer count +
idle reason, #9 byte-size drift, #13 partly resolved), **1 imprecise** (#8 "installed package"),
**1 UNK closed** (#14).

## What the entry should quote instead

- Prefer `[QUOTE-A]`/`[QUOTE-B]` (config blocks), `[QUOTE-C..F]` (producer bodies), `[QUOTE-G..I]`
  (indicator probes) and `[QUERY-1..5]` — all stable byte ranges or exit-status facts.
- Replace the cache's `updated_at` literal with `updated_at_within_24h=true` plus the 20-minute
  `STALE_AFTER_SEC` threshold; both are properties, neither rotates.
- Replace "134 777 B" with the sha256 pin, or say "a single-file Python program (sha256 …)".
- Say "seven `return-type: json` modules" and "the idle chip renders empty because `hypridle` runs".

## Risks / notes for the integrator

- The 7-vs-5 and idle-reason defects (#7) are **content** defects in a held/candidate entry; fixing
  them changes the entry's claims, so the L1 decides whether to amend in place or record a rejection.
- #9 shows the entry's size pin already drifted twice inside two days upstream; any size pin in the
  entry will rot again.
- `notes.json` and `status.json` are `-rw-------`; only shapes/counts were read. Do not let a later
  seat quote note bodies or cache values.
- Nothing here was written outside the two seat/fetch files and this report. No blockers.
