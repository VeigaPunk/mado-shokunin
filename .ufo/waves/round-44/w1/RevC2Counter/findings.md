# RevC2Counter — findings on the frozen counter `quality/counters/c2-r44-gkeep-size-request.py`

All fixtures were built and scored in `/fast/scratch/hyaku/mado-r44/RevC2Counter/` (git discipline:
`D=$(mktemp -d -p …)`, `git -C "$D" init -q`, `git -C "$D" rev-parse --show-toplevel == $D` before the
first commit, every later git call `-C "$D"`). Builder + per-fixture counter logs are copied to this
seat dir (`build_fix.py`, `log-*.txt`); scratch was deleted after the copy. The counter was never
edited. Fixture rev hashes differ between runs only via commit timestamps; verdicts and clause maps
reproduce exactly (verified twice).

## A. Diff classification: `c2-r43-gkeep-entry-v2.py` → `c2-r44-gkeep-size-request.py`

637 → 644 lines; 64 insertions, 57 deletions; six changed hunks, everything else byte-identical:

| Hunk (r44 lines) | Change | Class |
|---|---|---|
| 3–35 | docstring rewritten: PRED-C2-r44 header, the three declared change classes, final line, residuals | docstring |
| 145–149 | `PRED`, `BASE_DEFAULT`, `ENTRIES`, `LESSON`, `FETCH` | constant |
| 167–172 | `PINS`: nine round-43 receipts → five round-44 receipts (sha256s verified byte-equal to the lane's `fetch/` files: d735d454…, d90b534c…, 0ee38458…, 07a3c4a5…, 7ba7f9c8…) | constant |
| 176 | `STAGED` drops `gkeep-size-to-real-size-r11.md` (admitted in round 43) | constant |
| 382–409 | `host_census` rebuilt: own-work filter dropped; census now gkeep-ui.py + Hyprland-Window.cpp halves; `set_size_request` count; sendWindowSize body bound | clause h |
| 561–563 | `entry_lines` exclusion prefixes `host `/`gkeep request ` → `gkeep client `/`hyprland sendWindowSize ` | clause h (census exclusion) |

No other function, regex, or clause body changed. Clauses a–g, i logic is inherited verbatim from v2.

## B. Findings

### F1 — HIGH — held-id receipt substitution; the docstring's declared closure does not exist in code

- **Attack**: clause d applies the PINS digest check only to NEW ids (`quality/counters/c2-r44-gkeep-size-request.py:496-499`: `pin_ok = True` unless `i in new_ids`). A HELD id's gate may name any committed file under `fetch/` with any sha256 — the only checks are the gate's own self-consistency (sha256 of the committed blob equals the gate's declared digest, :501-506). Clause i (:603) then checks `set(PINS) <= used` where `used` is **basenames only** — no sha comparison anywhere.
- **Docstring contradiction**: the r44 docstring (lines 26-28) declares the residual closed: "whose receipt is nevertheless one of PINS and must be byte-equal to be counted by i+". False: i+ counts `os.path.basename(gates[i][0][0])` (:603); a forged `Hyprland-Window.cpp` committed at REV satisfies i+ while differing from the pin in every byte.
- **Census poisoning**: `host_census` reads `byname[os.path.basename(gl[0][0])] = receipts_raw[i]` (:387) — the Hyprland half of clause h is computed from whatever bytes the held id's gate names. The frozen claim's `xdg_setSize=1 x11_configure=1` (true values on the real pin: body 1732-1754, first lone `}` at 1754, 1×`->setSize(`, 1×`->configure(`) can be replaced by any pair.
- **Fixture** (`log-forged_s164.txt`, builder kind `forged_s164`): commits an 8-line forged `Hyprland-Window.cpp` (sha256 `ae0db5c06faa73382c67cc5be1abe4c7af6e0075fb8432b3d03b86befb8a1ada`, ≠ pin `d735d454…`), gates held S164 with the forged sha and quote `m_reportedPosition = REPORTPOS;`, entry carries `hyprland sendWindowSize xdg_setSize=0 x11_configure=0` (truth: 1/1) and the S164 claim "the window side forwards one reported size and parks the ack serial" — the opposite of what the forged body shows. All four other receipts are the genuine pins. **Result: `admitted=1/1 verdict=TARGET_MET`, exit 0, clauses a-i all 1.**
- Also: a held id's receipt path need not even be `FETCH + basename` — any path under `fetch/` (e.g. a subdirectory) passes; only `path.startswith(FETCH)` gates blob loading (:493).

### F2 — MEDIUM — the census-prefix exclusion lets claim lines escape the g+ universal binding

- **Attack**: `entry_lines` (:559-563) drops every line starting `gkeep client ` or `hyprland sendWindowSize ` from clause-g scrutiny. `all_body_lines_bound` (:354-368) — the g+ invariant "EVERY unfenced entry line that names a cited id carries that id's Gate quote and locator" — therefore never sees such lines. The real census lines contain no `S###` tokens, so the exclusion is unnecessary for them; it exists only as a hiding channel. A decorated census line (`gkeep client …` + arbitrary claim text naming a cited id) is invisible to both `all_body_lines_bound` and the census exactly-once check (which compares raw lines for equality with the two `want` strings).
- **Fixture** (`log-hidden_line.txt`, kind `hidden_line`): honest entry + one extra line 14 `gkeep client follow-up: per S164 the pending ack serial is the only transport of the configured size` — names cited S164, carries no quote and no locator. **Result: `admitted=1/1`, g:1.**
- **Isolating control** (`log-hidden_line_control.txt`, kind `hidden_line_control`): the identical sentence without the prefix → `clauses=… g:0 … admitted=0`, exit 1. The prefix filter is the sole enabler.

### F3 — LOW — clause e binds a new id's location by basename containment only; false provenance URLs pass for non-Hyprland pins

- **Attack**: the e block computes `comp` (registry location's last path component, lower-cased) and `rb` (receipt basename) and requires only containment (`comp in rb or rb in comp`); the `raw.githubusercontent.com/hyprwm/Hyprland/efb5099…` prefix check fires only when the receipt basename starts `hyprland-`. For the GTK, wayland-protocols and gkeep pins the location cell is unverified against the pinned URL — a genuine (sha-pinned) receipt can be cited behind a fabricated location.
- **Fixture** (`log-false_url.txt`, kind `false_url`): S301's location cell set to `https://example.com/docs/ui.py` (receipt still the genuine pinned `gkeep-ui.py`). **Result: `admitted=1/1`.** (`example.com` dodges every BAD_LOC marker.)

### F4 — INFO — comment stripping of the gkeep pin: no effect on the real pin, two latent falsification directions

- `strip_comments` for `.py` is `re.sub(r"#[^\n]*", " ", text)` (:347-349) — strips from any `#` to EOL, including `#` inside string literals. On the real pin the only `#`-in-string is `gkeep-ui.py:145` (`foreground="#202124"`); no census token follows it on that line, so raw and stripped counts agree: `set_default_size` = exactly one (line 476, `420, 500`), `application_id` = exactly one (line 449, `org.omarchy.gkeep`), `set_size_request(` = 0 both ways. No scoring effect today.
- Latent: (a) a `set_size_request(` inside a docstring or string literal is NOT stripped and would be counted — the emitted label says `size_request_calls=` while the docstring (:15-16) defines N as "occurrences"; a string occurrence would be reported as a call. (b) a real call on a line after a `#`-in-string would be silently dropped. Both directions change the census the honest entry must carry; neither is entry-controllable.

### F5 — INFO — sendWindowSize body bound: correct on the real pin, fragile by construction

- The bound (:395-401) is `src.index("void CWindow::sendWindowSize(bool force) {")` (exact full-line match) to the FIRST following line that is exactly `}`. On the real pin the first lone `}` is line 1754 — the function's closing brace (nested braces are indented), so X=1, Y=1 is the true count (whole-file counts are 2 and 3 — the bound is doing real work). A column-0 `}` inside the body, or any whitespace drift in the signature line, would truncate the body or fail clause h. Fragility, not an exploit; the census is pinned-byte bookkeeping either way.

### F6 — INFO — census lines cannot be satisfied without citing the receipts (no bypass)

- `byname` is built only from ids present in `receipts_raw` (clause-d-passed cited ids) with exactly one gate line (:384-387); clause i requires all five PINS basenames among the used receipt basenames (:603-604). GATE lines for uncited ids populate `gates` but never `receipts_raw`, so they cannot feed the census. No fixture needed; no hole found.

### F7 — INFO — dead parameters in `host_census`

- `host_census(new_ids, reg_rev, gates, receipts_raw, lines)` (:382): `new_ids` and `reg_rev` are unused in r44 (leftovers of the round-43 own-work filter). Dead weight only; no scoring effect.

## C. Assigned sub-questions, answered

| Question | Answer |
|---|---|
| `set_size_request(` inside a string/docstring of the gkeep pin? | Not in the real pin (N=0 raw and stripped, verified). Counter would count one if present (F4a). |
| sendWindowSize body bound = first line exactly `}`? | Yes; on the real pin that is the function's closing brace (line 1754), counts correct (F5). |
| Gates lookup by basename? | Pin check requires `path == FETCH + basename(path)` — no traversal; `byname` keyed by basename with clause-d distinct-path guarantee. Sound for new ids; the held-id path is the hole (F1). |
| Census lines satisfiable without citing the receipts? | No (F6). |
| Can a claim line hide in the `entry_lines` filter? | Yes (F2) — the one filter exploit found. |
| Held S164 with a pinned receipt: forged receipt substitutable? | Yes (F1) — and it feeds clause h. |

## D. Reproduction

```
python3 .ufo/waves/round-44/w1/RevC2Counter/build_fix.py honest forged_s164 hidden_line hidden_line_control false_url
```
(each fixture: mktemp under `/fast/scratch/hyaku/mado-r44/RevC2Counter/`, two commits, counter run
`python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <D> --rev <rev> --base <base>`;
per-fixture stdout in `log-<kind>.txt`).
