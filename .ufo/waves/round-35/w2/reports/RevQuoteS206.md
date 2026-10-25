# RevQuoteS206 — row S206 quote/anchoring audit (round 35, wave 2)

Seat: RevQuoteS206 (leaf reviewer, no dispatch). Lane: mado-shokunin. Date: 2026-10-25.
Substrates read-only: no bar started, no indicator executed, no toggle run, no menu opened.
Machine log with per-command exit codes: `.ufo/waves/round-35/scratch/RevQuoteS206/verify.log`
Raw evidence: `.ufo/waves/round-35/scratch/RevQuoteS206/findings.md`

## Axes

1. **A1 anchor integrity** — receipt sha256 equals the anchor cell of row S206.
2. **A2 receipt fidelity** — the receipt's recorded hashes/sizes/quoted lines equal live host bytes.
3. **A3 quote legality** — the entry's gate-quote is a contiguous, unique substring of receipt bytes.
4. **A4 statement truth** — the two facts the gate-quote asserts still hold on the host.
5. **A5 liveliness** (attack beyond the seat) — the on-click target is a present, wired command.

## Verdict: row S206 HOLDS. No divergence on (a), (b) or (c).

### (a) Live source re-opened

| check | command | result | exit |
|---|---|---|---|
| hash | `sha256sum /home/vgpnk/.config/waybar/config.jsonc` | `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829` | 0 |
| size | `wc -c /home/vgpnk/.config/waybar/config.jsonc` | `6354` | 0 |
| lines | `wc -l …` | `260` | 0 |
| numbered print | `cat -n … \| sed -n '200,215p'` | lines 200-215 below | 0 |

```
   200	  },
   201	  "custom/screenrecording-indicator": {
   202	    "on-click": "omarchy-capture-screenrecording",
   203	    "exec": "$OMARCHY_PATH/default/waybar/indicators/screen-recording.sh",
   204	    "signal": 8,
   205	    "return-type": "json"
   206	  },
   207	  "custom/idle-indicator": {
   208	    "on-click": "omarchy-toggle-idle",
   209	    "exec": "$OMARCHY_PATH/default/waybar/indicators/idle.sh",
   210	    "signal": 9,
   211	    "return-type": "json"
   212	  },
   213	  "custom/notification-silencing-indicator": {
   214	    "on-click": "omarchy-toggle-notification-silencing",
   215	    "exec": "$OMARCHY_PATH/default/waybar/indicators/notification-silencing.sh",
```

Line 207 opens the module; line 208 carries the handler. Line 18 (`"custom/idle-indicator",`)
sits inside **`modules-center`** (header line 11), with `modules-right` beginning line 21 — the
entry never names the array, so nothing here is wrong; recorded because a sibling asserting
"modules-left" would be.

### (b) Gate-quote vs receipt bytes

The seat's quote — `located: waybar config.jsonc line 207 opens the custom/idle-indicator module; line 208 runs omarchy-toggle-idle` — tested over raw bytes:

```
python3 -I -c '... b.find(q.encode()), b.count(q.encode())'
found_at 817 count 1 crlf False          exit=0
```

111 bytes, **contiguous**, **unique**, LF-only, terminating the receipt as `quote` + one LF. A2 holds too: the receipt's own recorded `a408a33…aae829` / `6354` equal the live values measured above, and a numbered-segment diff of the receipt's 14 quoted lines against live line numbers 18-213 yields **0 content mismatches** (a naive parser flags line 24 only because the excerpt's closing `---` is unnumbered).

One precision note, not a divergence: the entry renders `gate-quote: S206 located: …`. The `S206 ` token is a seat label added by the entry and is absent from the receipt (`b.find("S206 " + q)` = `-1`). The identical convention holds across all six seat quotes S205-S210 (receipts start `located:`; entries prefix `gate-quote: S20x `), so it is a uniform label, and the quoted assertion itself is contiguous.

Facts against the host now:

| gate-quote fact | live evidence | verdict |
|---|---|---|
| line 207 opens the `custom/idle-indicator` module | `207:  "custom/idle-indicator": {` | holds |
| line 208 runs `omarchy-toggle-idle` | `208:    "on-click": "omarchy-toggle-idle",` | holds |

### (c) Receipt anchor vs SOURCES.md

| value | receipt | SOURCES.md cell 7, row S206 | match |
|---|---|---|---|
| receipt sha256 | `1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5` | `1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5` | **equal** |
| file sha256 | `a408a33f…aae829` | `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829` | **equal** |
| file size | `6354` | `6354 B` | **equal** |

```
sha256sum .ufo/waves/round-35/fetch/S206.receipt.txt
1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5   exit=0
awk -F'|' '$2 ~ /S206 /{print $7}' corpus/SOURCES.md                     exit=0
 lines 207-212 and 18-19 at /home/vgpnk/.config/waybar/config.jsonc, 6354 B,
 file sha256 a408a33d…aae829; receipt .ufo/waves/round-35/fetch/S206.receipt.txt
 sha256 1d30e4a9…a938d5
```

## Findings by severity

**None blocking. No divergence requiring the STOP clause.**

**INFO-1 — receipt's handler count is block-scoped, and its header does not say so.**
`S206.receipt.txt` prints `--- on-click handler count ---` then `1`. Measured here:
`sed -n '207,212p' … | grep -c '"on-click"'` → **1** (exit 0); `grep -c '"on-click"' …` over the
whole file → **15** (exit 0). The `1` is correct for the quoted block and would understate by 14
if read as file-wide. No cited claim depends on it — neither the entry, the gate-quote, nor the
SOURCES cell mentions a count — so this is an annotation-ambiguity risk only, not a falsehood.

**INFO-2 — material corroboration the row did not claim (strengthens, does not falsify).**
The claim "offered in the running interface" survives an attack the entry did not run:
`pgrep -a waybar` → `935660 /usr/bin/waybar` (exit 0), started 2026-10-25 02:06:20, cmdline with
**no `-c` override**; `~/.config/waybar` contains exactly one live config (`config.jsonc`) with the
rest `.bak` copies, so the running bar loads the hashed file. The click target is live too:
`/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle` is `-rwxr-xr-x`, 316 B, resolves on
`PATH` (exit 0), and its line 13 `pkill -RTMIN+9 waybar` matches config line 210 `"signal": 9` —
the click/refresh loop is wired end to end. Executed nothing; file and process reads only.

## Residual risk

- The receipt proves content identity, not that the bar *renders* the module: `modules-center`
  membership is necessary, not sufficient (a hidden/dropped section or a theme that hides
  `#custom-idle-indicator` would not show). `style.css` does carry hooks at lines 86 and 99; no
  `hide`/`draw` gate was found. Not falsified, merely unproven — the entry's OBS is correctly
  scoped to a file read and its header says no bar was started.
- `verified-at: 2026-10-24` vs my measurement 2026-10-25: content hashes match, so the day
  difference carries no content drift.
- Cross-row consistency (S207's `pgrep -x hypridle` contract, S209's four copies, S210's empty
  toggles dir) is out of this seat's scope and was not adjudicated here.

## Verification gaps

- Nothing was executed from the substrate (no bar start, no indicator run, no toggle) — by design;
  A5 used presence/mode/PATH/process reads only.
- I did not attempt to observe waybar's rendered output (no IPC screenshot); "is displayed" is
  unverified as distinct from "is configured".
- No LSP server applies to `.jsonc`, a receipt text file, or a markdown registry; checks are
  byte/hash measurements, which are the appropriate proof for anchoring claims.

## Installs

None. Pacman is paused host-wide; no tool was needed (coreutils, python3, awk, grep sufficed).
