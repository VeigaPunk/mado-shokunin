# R80ReviewerC2 — adversarial review of the C2 claim (chord grammar + state/exit-status matcher)

Seat scope: attack the C2 claim. Method: read the installed formatter (`fetch/S473.txt`) and the
`systemctl` man fragment (`fetch/S474.txt`); execute the *real* matcher bytes — both the frozen
counter at `6c302a53` (sha `462287fb…`, verified) and the live tip counter (R2/R3, sha
`d422892b…`) — against every candidate line; run the installed formatter live
(`omarchy menu keybindings --print | cut -c1-35`, read-only) and record host `is-active` word/rc
pairs. No installs performed. Scratch `/fast/scratch/hyaku/mado-r80/R80ReviewerC2` removed at end.

## Wave context discovered mid-review (decides the verdict on the frozen claim)

The lane moved past the freeze while the wave ran: `1e672749` repair R2 (the chord grammar accepts
the formatter's empty-key rendering), `eb00dd06` repair R3 (allowlisted child env, pinned TMPDIR),
re-measured at the tip `eb00dd06` → `measurement-c2-r80-at-tip.txt`: `matched=24`, `killed=16`,
`control_new=0/2`, `verdict=TARGET_MET`. The frozen counter at `6c302a53` is byte-identical to the
declared frozen sha and selftests 80/80 green, and it passes the entire frozen case set (verified
by direct execution) — but see F1: the frozen grammar rejects a shape the live formatter actually
produces, so the frozen measurement at `6c302a53` was invocation-lucky.

## F1 — HIGH — the frozen grammar rejects the formatter's real empty-key rendering (found in vivo; repaired post-freeze as R2)

- Source: `S473.txt:9-11` (`xkbcli compile-keymap` failure is tolerated, cache left empty),
  `S473.txt:40` (empty lookup prints nothing), `S473.txt:134-138` (`key_combo = $1 " + " $2`, trim
  → a line ending ` +`), `S473.txt:153` (space collapse runs only in the `action == ""` branch).
- Grammar clause (frozen, `6c302a53`): chord branch requires `" + "` in the line; a line ending
  ` +` falls to `elif "+" in line: return False`.
- Verdict: FALSE NEGATIVE, confirmed live. One live invocation produced **41 lines reading
  `SUPER +`** (keycode whose symbol map is empty; `corpus/lessons/round-80.md` “L1 repair R2”
  records the same observation), the next produced none — the keymap cache is intermittent. A
  single such line fails the whole row, so the frozen predicate at `6c302a53` is
  host-invocation-dependent: the frozen receipt caught a warm run. Verified directly: frozen
  matcher returns `False` for `SUPER +`; tip matcher (R2) returns `True`; frozen negatives still
  all reject under the tip matcher (padded-key check survives because `tail.rstrip()` keeps the
  leading space of `SUPER +  X`); selftest 80 → 81, green at the tip; `chord-key-padded` mutant
  re-cut and still killed (`killed=16` at tip). Repaired, but the frozen claim as written was
  measured on a lucky invocation.

## F2 — MEDIUM — the `code:201 → COPILOT KEY` rewrite is mask-65-only; the leak is accepted, uncovered

- Source: `S473.txt:49-50` — the substitution pattern is the *literal* `SUPER SHIFT,code:201`; for
  any other modmask the pattern is absent, the substitution is a no-op, and (unlike other codes)
  keycode 201 never falls back to the symbol lookup.
- Grammar clause: one to four distinct modifier words + ` + ` + one key token — `code:201` is an
  opaque valid token.
- Verdict: FALSE POSITIVE (accepts a defect-indicating form), verified against the real matcher:
  mask 77 + `code:201` → `SUPER SHIFT CTRL ALT + code:201` accepted; mask 0 → bare `code:201`
  accepted; mask 65 → `COPILOT KEY` (the only path the declaration's unconditional “`code:201` →
  `COPILOT KEY`” wording describes). No frozen sample or negative covers a `code:` key token, so a
  regression that drops or narrows the rewrite still passes the row on this host (today's config
  binds the copilot key at mask 65, so no live instance — yet the grammar cannot see it).

## F3 — MEDIUM — the state/exit-status contract is over-specified in both directions (residual)

- Source: `S474.txt` — “Returns an exit code 0 if at least one is active, or **non-zero**
  otherwise”; the local systemd 262 man page states the same and no more.
- Grammar clause: `rc == (0 if text == "active" else 3)`.
- Verdict: NOT the complete contract. Host-observed pairs this session: `hypridle` → `inactive` rc
  **3**; `pipewire-pulse` → `active` rc **0**; a nonexistent unit → `inactive` rc **4** — a genuine
  reply the matcher rejects. Direction two (source-documented, not host-observed — inducing a
  reload needs a mutation, which is out of bounds): `systemctl is-active` treats `reloading` as
  active (`arg_states = strv_new("active", "reloading")` in `systemctl.c`), so `reloading` comes
  with rc 0 and the matcher would wrongly reject it. Harmless for the bound unit today (hypridle
  exists, `UnitFileState=disabled`, `ActiveState=inactive`), but “otherwise rc 3” is an empirical
  narrowing, not the documented contract.

## F4 — LOW — the state enum is not closed against the instrumented systemd's own vocabulary (residual)

- Source: local `systemctl(1)` ACTIVE-states table (systemd 262): `active, inactive, failed,
  activating, deactivating, maintenance, reloading, refreshing` — the table itself warns “the list
  of possible LOAD, ACTIVE, and SUB states is not constant and new systemd releases may both add
  and remove values.”
- Grammar clause: `text not in value["enum"] → False`; the frozen enum has 7 words and omits
  `maintenance` and `refreshing` (while including `unknown`, which is not an ACTIVE state at all).
- Verdict: any `maintenance`/`refreshing` print (rc 3) false-negatives the row. Low likelihood for
  this unit; real gap against the instrumented version's documented states.

## F5 — LOW — >35-column chords truncate inside the key token and still parse (named by the L1, not fixed)

- Source: `S473.txt:164` — `printf "%-35s → %s"`; the row binds `cut -c1-35`.
- Grammar clause: any single non-empty tail token is a valid key.
- Verdict: ACCEPTED truncation — `SUPER SHIFT CTRL ALT + XF86AudioPla` (a 47-column chord cut at
  35) verifies `True` against the real matcher. The L1 already named this limit in
  `corpus/lessons/round-80.md` (“named not fixed”); no live instance (today's longest chord is 29
  columns; live run: 193 lines, 169 chords, 24 bare, all accepted).

## F6 — LOW — several frozen negatives cannot occur through the bound row (synthetic mutant-killers)

Per negative, the planted violating line and its producibility through `S473` + `cut -c1-35`:
neg0 `HYPER + X` — no path emits a foreign modifier word (unmapped masks stay *numeric*);
neg1 `SUPER +  X` — the joiner is exactly `" + "` (`S473.txt:134`), no source yields a double
space; neg3 `64 + RETURN` — mask 64 is rewritten (`S473.txt:108`), only unmapped masks (2/16/32)
stay numeric; neg4 `SUPER SUPER + X` — the table emits each modifier once; neg5 `SUPER + X → Y` —
the arrow sits at column ≥ 37 (`S473.txt:164`), `cut -c1-35` can never show it, and no token
contains `→`, so the matcher's arrow check is *unreachable* through this row; neg6 `SUPER + X + Y`
— keys never contain ` + `. Only neg2 (valid bare keys diluting chords below `min_chords=100` —
itself a hard floor a switch-heavy valid config could trip) and neg7 (99 lines, the floor) are
host-plausible. Verdict: fine as mutant-killers (all 16 die at the tip), but the set is not
host-faithful; the declaration's prose classes “an empty line” has **no** committed negative (all
10 texts verified to have 0 interior empty lines).

## F7 — LOW — declaration/set counting inaccuracies (prose only; the predicate is unaffected)

- “seven committed negatives” for `keybindings-chords` — the case commits **8** (verified distinct
  by content and length), covering 7 of the 8 prose classes (empty line uncovered).
- “the twelve-mask table” — the bytes hold **sixteen** `s/^N,/` rules at `S473.txt:100-115`
  (`grep -c` → 16); already captured by the wave as M80-6 with the S476 supersede row, and this
  review independently reproduces it.
- The two positive samples are synthetic bind sets, not captured bytes: 4 of their 8 chord lines
  (`SUPER + Q`, `CTRL ALT + BACKSPACE`, `SUPER SHIFT CTRL ALT + X`, `SHIFT + F1`) do not exist in
  today's live output. Allowed by “a changed bind set passes”; noted for honesty.

## Enumeration requested by the seat (every chord-producing path vs the grammar)

| Path (S473 source) | Emits | Grammar verdict |
|---|---|---|
| mask table `:100-115` (16 rules incl. 77 = SUPER SHIFT CTRL ALT) | bare key (mask 0) or 1–4 distinct words + ` + ` + key | accepts all ✓ |
| `code:201` rewrite `:49-50` | mask 65 → `COPILOT KEY`; mask ≠ 65 → literal `code:201` key token | accepts both (F2 leak) |
| mouse rewrites `:55-66` | 272/273/274 → multi-word `LEFT/RIGHT/MIDDLE MOUSE BUTTON`; else literal `mouse:N` | accepts all ✓ |
| keycode symbol path `:38-46` | map hit → symbol key; miss (≠201) → empty key → line ending ` +` | frozen: rejects (F1); tip: accepts (R2) |
| `switch:` lines | untouched by `parse_keycodes` → bare `switch:on/off:Lid Switch` | accepts ✓ (space-containing bare key) |
| `static_bindings` `:119-121` | `SHIFT ALT + L` | accepts ✓ |
| `s/null//` `:94` + empty key `:98-99` | blank chord column (all-space line) | rejects as empty line (intended; uncommitted negative) |
| unmapped modmask (2/16/32) | numeric head `16 + Q` | rejects ✓ (neg3 covers the class, not the instance) |

## Host evidence recorded

- `systemctl --user is-active hypridle` → `inactive`, rc **3** (unit exists: `ActiveState=inactive`,
  `UnitFileState=disabled`).
- `systemctl --user is-active pipewire-pulse` → `active`, rc **0**.
- `systemctl --user is-active definitely-not-a-unit-xyz` → `inactive`, rc **4**.
- Live `omarchy menu keybindings --print | cut -c1-35` → 193 lines (169 chords, 24 bare keys, max
  chord 29 cols), no `code:`, `mouse:`, arrow, or blank lines; full output matches the tip grammar.
- Frozen counter at `6c302a53`: sha `462287fb…` = declared frozen sha; selftest 80/80; passes the
  full frozen set; rejects `SUPER +` (F1). Tip counter: sha `d422892b…`, selftest 81/81, passes
  the full frozen set; accepts `SUPER +`.

STATUS: ok — one in-vivo false negative (F1) found and already repaired post-freeze by the wave
(R2, re-measured TARGET_MET at the tip); residual uncovered gaps F2–F4 named with source lines,
grammar clauses, and live verdicts; no tool installs or host mutations performed.
