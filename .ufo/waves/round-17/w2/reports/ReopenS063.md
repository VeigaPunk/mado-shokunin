# Reopen S063 — hypridle wiki page (`wiki.hypr.land/Hypr-Ecosystem/hypridle/`)

Lane: `mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60` (read only; no commits,
no `.jj`, no subagents). Assignment: re-open row S063, verify URL / verbatim quote at the
stated anchor / digest / tier / status / verdict, and verify every claim the citing note
(`corpus/knowledge/idle-lock-route-r17.md`) makes from this source at the anchors it gives.

**Result: the row and every P6 claim it supports survive.** Fresh bytes reproduce the
recorded digest, the quote is byte-exact at `[HW:6]`, and all 21 `[HW:*]` references in the
citing note resolve to the claimed text (26/26 substring assertions pass). One countable
defect remains in the gate line: it says the quote is **11 words**; the displayed quote is
**9**. Two informational notes (quote-vs-`teaches` narrowness; an over-strong "only" in one
note sentence) do not change any route conclusion. Installs: **none** — no pacman/sudo/
systemctl/hyprctl/live probes were run.

Axes walked: (1) digest identity, (2) quote fidelity + anchor existence, (3) registry row
contract, (4) citing-note entailment at its anchors, (5) provenance stability across the
round-17 commits and the "Latest git" label.

## 1. Fetch and digest

```
$ curl -sS -o /tmp/s063.html -w '%{http_code} %{size_download}\n' \
    https://wiki.hypr.land/Hypr-Ecosystem/hypridle/
200 254750
$ sha256sum /tmp/s063.html
b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640  /tmp/s063.html
```

- A second independent fetch (and a third, `-o s063c.html`) produced the **same 254750
  bytes and the same SHA-256**; the page is served stably today.
- 623 physical HTML lines; canonical link `https://wiki.hypr.land/Hypr-Ecosystem/hypridle/`
  matches the row URL exactly.
- `article:modified_time` and `dateModified` = `2026-08-26T14:50:40+02:00`; the article's
  last line reads `Last updated on August 26, 2026` — the row's "page modified 2026-08-26"
  holds.
- The digest is a three-way identity:

| origin | sha256 |
|---|---|
| fresh bytes (3 fetches) | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |
| `corpus/SOURCES.md:75` anchor cell | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |
| `corpus/lessons/round-17.md:50` gate | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |

`ALL-THREE-IDENTICAL` (64 lowercase hex, no truncation).

### Anchor convention — reproduced, not taken on faith

The note defines `[HW:n]` as "line n of the tag-stripped `<article>` text, one line per block
(table cells run together in the text)" (`idle-lock-route-r17.md:19`). Stripping the
`<article>` by turning block-level tags (`p div h1-6 li ul ol tr table thead tbody pre
blockquote section article hr br`) into newlines and deleting all other tags yields exactly
**121 non-empty lines**, and line 6 is byte-for-byte the gate quote:

```
  5| Configuration
  6| Configuration is done via the config file at ~/.config/hypr/hypridle.conf.
  7| A config file is required; hypridle won’t run without one.
```

So `[HW:6]` is not a guess: the stated convention reproduces it, and the row's citable range
"lines 6-120" contains the body, the last-updated line (120) and every `[HW:*]` the note uses.

Note on raw bytes: in the HTML the path is wrapped in `<code>…</code>`, so a raw `grep -F`
for the whole sentence fails; under the registry's own tag-stripped convention the quote is
verbatim. This is a convention property, not a misquote.

## 2. Registry row — `corpus/SOURCES.md:75`

The row parses as 11 columns (13 `|`-separated fields) under the registry's own census
predicate, alongside the header at `corpus/SOURCES.md:86`.

- **URL** — identical to the assignment URL (trailing slash, case-exact `Hypr-Ecosystem`).
- **kind `docs`** — allowed value (`CORPUS.md:91-92`).
- **tier `A`** — `CORPUS.md:93-97`: A is "primary or authoritative for that scope (spec,
  official docs, source code, …)". This is the upstream project's own wiki (edit link goes to
  `github.com/hyprwm/hyprland-wiki/edit/main/content/Hypr%20Ecosystem/hypridle.md`), kind is
  `docs`, not `community` (which "is never A"). Tier A is correct, not inflated.
- **scope** — four claims, all present: general key table (line 12 onward), listener table
  (47 onward), `inhibit_sleep` modes 0-3 (22-26, 30-33), `condition_cmd` (52-53, 55-60);
  "wiki 'Latest git'" and "page modified 2026-08-26" — see §5.
- **anchor** — digest plus the tag-stripped line convention (reproduced above); range 6-120
  covers all cited anchors.
- **teaches** — "documented meaning of lock_cmd, before/after_sleep_cmd, on-timeout/on-resume,
  inhibit_sleep 0-3; not version-pinned to v0.1.8": `lock_cmd` row at 13, `unlock_cmd` 14,
  `before_sleep_cmd`/`after_sleep_cmd` 17-18, listener `timeout`/`on-timeout`/`on-resume`
  36-38, 48-50, `inhibit_sleep` 22-26 + 33. "Not version-pinned" holds literally: the page
  bytes carry no version token at all (only a "Version selector ⚙️" link); see §5.
- **status `mined`** — honest: the note named in `used-by` exists and cites S063 (source line
  1; 21 anchored references).
- **opened `2026-10-20`, recheck `90d`** — fetch date matches; 90d is a sane cadence for a
  mutable `latest git` page.
- **used-by `corpus/knowledge/idle-lock-route-r17.md`** — path resolves.

Aggregate arithmetic in the gate block reconciles exactly (recounted from git, not trusted):
`9dcf248` 55 rows / A 51 / C 3 / mined 43 / rejected 4 / queued 8 →
`988b858` 70 rows / A 63 / C 6 / mined 55 / rejected 7 / queued 8. +15 rows = +12 A +3 C;
+15 statuses = +12 mined +3 rejected. S063 is one of the 12 added tier-A mined rows.

## 3. Gate line — `corpus/lessons/round-17.md:50`

```
| S063 | https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | [HW:6] "Configuration is done via the config file at ~/.config/hypr/hypridle.conf." (11 words) | `b45c03dc…f640` |
```

- **URL** — identical to the row and to the canonical link.
- **Quote** — byte-exact at `[HW:6]` under the note's stated convention. The sentence is the
  first of four in the Configuration section's opening paragraph, separated by `<br>` tags and
  a source newline; that is why it is its own block line (line 6) rather than part of line 5.
  Verbatim, with the sentence-final period.
- **Word count: 9, not 11 — D1.** `q.split()` = 9 tokens and `printf '%s\n' "$q" | wc -w` = 9:
  `Configuration is done via the config file at ~/.config/hypr/hypridle.conf.` The count 11
  is reproducible only by counting text the displayed quote does not contain: the section
  heading `Configuration` (+1) and the sentence-final period as its own token after
  `</code>` (+1). Reproduced: heading + `Configuration is done via the config file at` +
  `~/.config/hypr/hypridle.conf` + `.` = 11 tokens. So 11 is a tokenizer artifact, not the
  word count of the quote. (`ReopenS056` reports the same class of off-by-one in S056's
  "(12 words)"; nothing in the lane computes gate counts — `label-claims.json` has 7 entries,
  none S063, and `label-check.py` contains no gate/`words` logic.)
- **Digest** — equal to fresh bytes and to SOURCES (§1).
- **Tier / status / verdict** — the gate table has no tier or verdict column; those live in
  the row (tier A, mined) and the gate's admitted "New rows" block. S063 is not annotated
  `(rejected)`; the Admit/Reject text admits "documentary P6 … routes from rows opened this
  round" and none of the reject triggers apply (not a tier-C restatement, not a snippet-only
  read, no tag/pkgver-as-binary claim, no declared-listener-as-observed claim). Verdict:
  **admitted**, consistent with the +15 arithmetic.

**G1 (informational, not a defect):** `CORPUS.md:112-115` asks for "a ≤25-word quote with
its location grounding `teaches`". This quote grounds the Configuration section's
config-path/required facts; `teaches` is about key meanings and `inhibit_sleep` modes, which
the quote does not itself evidence. Every `teaches` element *is* present in the article and is
grounded by the note's own anchors (§4), so nothing over-reads; the gate quote is a narrow
locator, the same "compliant but narrow" shape `ReopenS056` recorded for S056.

## 4. Claims the citing note makes from S063

21 `[HW:*]` references (all within lines 6-120). I asserted the adjacent quoted text against
the reproduced line content: **26/26 assertions pass, 0 failures.**

| anchor | note claim (wording) | line content at anchor | holds |
|---|---|---|---|
| 6 | config path `~/.config/hypr/hypridle.conf` | exact sentence | ✓ |
| 7 | "A config file is required; hypridle won’t run without one." | exact | ✓ |
| 8-9 | autostart / `systemctl --user enable --now hypridle.service` under uwsm | both statements present | ✓ |
| 13 | `lock_cmd` "command to run when receiving a dbus lock event (e.g. loginctl lock-session)" | exact description, `string`, default `empty` | ✓ |
| 14 | `unlock_cmd` same on unlock | exact | ✓ |
| 15-16 | `on_lock_cmd` / `on_unlock_cmd` "session gets locked/unlocked by a lock screen app" | exact | ✓ |
| 17-18 | `before_sleep_cmd` / `after_sleep_cmd` "dbus prepare_sleep" / "post prepare_sleep" | exact | ✓ |
| 19 | `ignore_dbus_inhibit` (e.g. firefox), bool, false | exact | ✓ |
| 20 | `ignore_systemd_inhibit`, `systemd-inhibit --what=idle`, false | exact | ✓ |
| 21 | `ignore_wayland_inhibit`, false | exact | ✓ |
| 22-26 | `inhibit_sleep` 0 disable / 1 normal / 2 auto / 3 lock notify; default 2 | all four modes and `int2` | ✓ |
| 33 | "3 makes your system wait until the session gets locked by a lock screen app." | exact | ✓ |
| 36-37 | "Every listener has a timeout (in seconds). After idling for timeout seconds," | exact across the two lines | ✓ |
| 38 | "When action is resumed after idle, on-resume will fire." | exact | ✓ |
| 51 | `ignore_inhibit` per-listener row | exact | ✓ |
| 52-53 | `condition_cmd` / `condition_retry` table rows | exact (`/bin/sh -c`, exit 0 vs non-zero, 0 disables retry) | ✓ |
| 55-60 | condition retry prose ("re-runs every N seconds…", default 0 skips) | exact | ✓ |
| 78-107 | wiki example timeouts and dpms/suspend examples, documentary only | the full five-listener example is exactly lines 78-107 | ✓ |
| 120 | "last updated 2026-08-26" | `Last updated on August 26, 2026` | ✓ |

The note's S063-depending assertions therefore hold: `lock_cmd`/`before_sleep_cmd`/
`after_sleep_cmd` meanings, `on-timeout`/`on-resume` firing description, `inhibit_sleep`
0-3 with default 2, `condition_cmd` documentation, config path/required sentence, and the
page date. No note claim overstates what the page says.

**O2 (wording, outside the row; low):** `idle-lock-route-r17.md:130` says the wiki documents
`condition_cmd`, "which the v0.1.8 source also contains ([HC:71]), so the two agree on that
key only." The S063 half holds, but "that key only" is stronger than the note's own evidence:
the same note pairs other key names across both sources (`lock_cmd` HC:473 / HW:13,
`before_sleep_cmd`/`after_sleep_cmd` HC:493-510 / HW:17-18, `on_lock_cmd`/`on_unlock_cmd`
HC:402/433 / HW:15-16, `inhibit_sleep` HC:104-129 / HW:22-33). Under the natural reading the
sentence is false; it errs toward caution (understates agreement), so it cannot inflate P6.

## 5. "Latest git" provenance and page identity

The S063 bytes contain **no** `Latest git` token — only a `Version selector ⚙️` link to
`/version-selector/`. That selector page (`sha256 21f2e795f6a8f2d4009367af81a5b96ee252fdf94b939a09be3ddc1c329a684b`,
255003 B) states: "Select the latest Git version of the wiki, or a previous one below"
(versions listed from v0.56.0 back through v0.16.0-beta). Corroborating the unversioned page as latest-git:

- it differs from the newest release page `https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hypridle/`
  (HTTP 200, different bytes/line count; release page last-updated **2026-07-07** vs the
  fetched page's **2026-08-26**);
- `https://wiki.hypr.land/v0.56.0/Hypr-Ecosystem/hypridle/` 404s (no `v` prefix).

So "wiki 'Latest git'" is externally supported (the label is not self-evidencing from the
S063 bytes alone, but it is not invented). For a later recheck, the release-pinned page is
`/0.56.0/Hypr-Ecosystem/hypridle/`; the unversioned URL is the mutable latest-git page whose
digest today is the recorded one.

## 6. Provenance stability across round-17 commits

- `corpus/SOURCES.md` S063 row: line-content sha256 `035bb03f…b1c8` at **a9998d1** (C2, where
  it landed), **3e9848a** (corrections) and **988b858** (C3) — identical, so no later commit
  silently rewrote it.
- `corpus/lessons/round-17.md` S063 gate line: absent before C1 (the file did not exist at
  a9998d1), first present at **3722ba4** and line-hash `d99e5427…1c42` identical at
  **3e9848a** and **988b858** — stable since landing.

## 7. Attack surface traversed (failed to unseat the row)

1. Wrong URL / redirect / alternate casing — canonical URL 200, canonical tag matches row.
2. Digest mismatch or truncation — three-way exact 64-hex match; two fresh fetches equal.
3. Anchor drift — convention reproduced (121-line block text); `[HW:6]` exact.
4. Quote not verbatim — exact, including the period; only `<code>` markup separates it in
   raw bytes, which the registry convention strips.
5. Quote over 25 words — 9 words (D1 says 11; still ≤25).
6. Tier inflation — official maintainer docs (`docs`, not `community`); A allowed.
7. Status inflation — `mined` backed by an existing note that cites the row 21 times.
8. Note misquote/misplaced anchor — 21 anchors, 26 assertions, 0 failures.
9. Version-label fabrication — "Latest git" supported by the selector page's own wording plus
   content newer than the v0.56.0 release page.
10. Gate arithmetic hiding a rejected row — 55→70 / A 51→63 / C 3→6 / mined 43→55 /
    rejected 4→7 reconciles exactly; S063 is admitted, not rejected.

## 8. Findings and recommended one-line fixes

| id | finding | severity | impact |
|---|---|---|---|
| D1 | Gate line says the displayed quote is "(11 words)"; it is 9. 11 = section heading + the 9-word sentence + the sentence-final period counted separately | low, countable | none on P6: 9 and 11 are both ≤25; no lane checker validates gate counts |
| G1 | Gate quote is a narrow locator (config path/required) and does not itself ground the `teaches` key/mode list; the note grounds every teaches element at its own anchors | informational | none; wording of the gate contract (`CORPUS.md:112-115`) reads stricter than the artifact |
| O2 | Note:130 "the two agree on that key only" is contradicted by the note's own cross-source key pairs | low, wording | none; errs toward caution |

Suggested edits (not applied; report-only lane): change `(11 words)` → `(9 words)` at
`corpus/lessons/round-17.md:50`. Optionally, if the gate quote must satisfy "grounding
`teaches`" literally, cite a `teaches`-bearing anchor (e.g. `[HW:13]` `lock_cmd`, or
`[HW:22-26]` for the modes) — but that is a contract-reading call, not a defect the bytes
force.

## 9. Residual unknowns / limits

- The page is mutable latest-git: the digest anchors 2026-10-20 only; the 90d recheck date is
  the right control, and `/0.56.0/Hypr-Ecosystem/hypridle/` is the release-pinned comparator.
- "Latest git" is inferred from the selector page and content recency; the S063 bytes carry no
  version token, so no single-file proof exists.
- Gate word-count annotations are not machine-checked anywhere in the lane (`label-claims.json`
  has 7 entries, none S063), so D1-class errors cannot fail a gate automatically.
- Behaviour (listeners firing, lock success, inhibit transitions) is out of scope here and
  remains `[UNK]` per the note; nothing in this reopen exercises or asserts it.

Environment record: installs **none**. Commands used: `curl` (S063 twice/thrice,
`/version-selector/`, `/0.56.0/…` page, one HEAD probe), `sha256sum`, `python3 -I` (tag
stripping/assertions in `/tmp`), `git show|rev-parse`, `grep/awk`, `wc`. No sudo, pacman,
systemctl, hyprctl, loginctl, journalctl, pidof, or any live probe.
