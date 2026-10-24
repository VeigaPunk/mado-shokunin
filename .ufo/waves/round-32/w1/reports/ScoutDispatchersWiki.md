# ScoutDispatchersWiki — S188 re-open (round 32, w1)

Leaf scout; no subagents dispatched. Read-only network fetch; no substrate writes.

## Fetch record

- URL: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md`
- HTTP 200; curl wrote to `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/scratch/ScoutDispatchersWiki/dispatchers.md`
- Byte length: **12879**
- sha256: `c830ce0717f92776f03a977506141c549705aebe4e738ce801faddaa7b2d7d14` (prefix `c830ce0717f92776`)
- Accessed: **2026-10-24** (UTC)
- sha256 prefix **matches** the staged entry's recheck expectation (`c830ce0717f92776`).

## Requested items (line numbers refer to fetched bytes)

**(1) "returns a description, does not invoke"** — lines 8–9:

- L8: "Dispatchers return tables that describe an action you want to make."
- L9: "**They do not invoke any action immediately, and their contents are not guaranteed to be stable at all.**"

Supporting, L15: "**Simply writing `hl.dsp.whatever()` on its own will do nothing.**"

**(2) `force_idle` entry** — L69 (table row, split for quote limit):

- "`force_idle( int )` | Sets elapsed time for all idle timers in seconds, ignoring idle inhibitors."
- "Timers return to normal behavior upon the next activity. Do not use with a keybind directly!"

**(3) `event` dispatcher's target socket** — L59: "`event( string )` | Send an event to socket2". Target socket: **socket2**.

**(4) `dpms` entry** — L58: "`dpms({ monitor?, action? })` | Toggle monitors on/off (not physically, as in idle-screensaver). Do not use with a keybind directly!"

**(5) Keybind-warning lines** — L81–90; the warning sentence, L82: "It is NOT recommended to set DPMS or force_idle with a keybind directly, as it might cause undefined behavior." Followed by a `hl.timer` oneshot workaround snippet (L83–90).

**(6) Instability statement** — present at L9 (quoted above). **Scope caveat:** "their contents" refers to the *dispatchers'* returned tables (subject of L8–9 is dispatchers), i.e. unstable across releases — **not** a statement that the wiki document's own contents are unstable. No text in the fetched bytes describes the wiki page itself as unstable.

## Staged-entry verification

File checked: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/dispatcher-semantics-r25.md`

| # | Staged sentence checked (quoted) | Verdict |
|---|---|---|
| 1 | §1: `A dispatcher *describes*; it does not act (S188:9)` + quote "They do not invoke any action immediately, and their contents are not guaranteed to be stable at all." | **Agree** — verbatim substring of L9 (bold markers aside); pair with L8 confirms "describes". |
| 2 | §1: `Execution requires the wrapper (S188:14)` + quote "To use a dispatcher (any of `hl.dsp.*`) inside a function, you need to wrap it in `hl.dispatch()` for it to be executed." | **Agree** — verbatim match of L14. |
| 3 | §1 INF: "dispatcher behavior" splits into description vs execution | **Agree** — consistent with L8–9 + L14–15 read together. |
| 4 | §2: `` `event( string )` — "Send an event to socket2" (S188:59) `` | **Agree** — verbatim substring of L59. |
| 5 | §2: `` `force_idle( int )` — "Sets elapsed time for all idle timers in seconds, ignoring idle inhibitors." (S188:69) `` | **Agree (partial quote)** — verbatim substring of L69, but truncated: the cell continues "Timers return to normal behavior upon the next activity. Do not use with a keybind directly!" The dropped clauses are load-bearing for the §2 INF. |
| 6 | §2: quote "It is NOT recommended to set DPMS or force_idle with a keybind directly, as it might cause undefined behavior." (S188:82) | **Agree** — verbatim match of L82. |
| 7 | §2 INF: "`force_idle` is a *clock* operation on the idle timers, not a lock or a suspend operation" | **Agree** — L69 scopes it to elapsed idle time + inhibitor override; no lock/suspend semantics present. |
| 8 | §3: "The upstream text declares the dispatcher contents unstable (S188:9)" | **Agree** — L9 says dispatcher contents not guaranteed stable. Correctly scoped to dispatchers, not the wiki page. |
| 9 | §3 INF: pattern-matching on dispatcher contents can break across releases | **Agree** — direct consequence of L9's instability wording. |
| 10 | §3 UNK: host runs v0.56.2; version-matched 0.56.0 page "was **not** fetched this round" | **Not checkable against S188 bytes** — the file contains no version marker for 0.56.x; the "not fetched" part is a meta-claim about prior rounds. Bounded-agree: S188 indeed pins no Hyprland version. |
| 11 | §4: `curl … | grep -c 'hl.dispatch'`; expectation "1 or more occurrences" | **Agree** — re-run on the fetched bytes: `grep -c 'hl.dispatch'` → **7** (7 matching lines, 7 occurrences). |

## Discrepancies / notes

- Only material caveat: claim 5's staged quote truncates the L69 cell; the omitted tail is what ties `force_idle` to the keybind warning. No claim contradicted.
- Item (6) wording: instability is attributed to **dispatcher contents**, not the wiki document. Staged §3 reads it correctly; the lane title's "the wiki says their contents are unstable" resolves `their` → dispatchers.
- `.ufo/waves/round-32/scratch/ScoutDispatchersWiki/dispatchers.md` retains the raw bytes for re-checks.
