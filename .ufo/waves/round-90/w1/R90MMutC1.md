# R90MMutC1 — extra C1 mutants vs the frozen round-90 case set

Seat: `R90MMutC1` (mutation tester, leaf; no dispatches). Round mado 90 (hyaku run 15, attempt 1), wave `w1`.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base revision `5041acf99e27263872bf0441ad5f9d4316152605` (master).
Scratch: `S=/fast/scratch/hyaku/mado-r90/R90MMutC1` (deleted on exit — see §11).
Every counter/oracle run below is **DRAFT** (`--draft-tool`, exit 3; the oracle is not a measurement). Nothing was
written under `.ufo/waves/round-90/receipts/`.

## 1. Result in one paragraph

30 new semantic mutants of the C1 candidate were written, anchor-checked (each `find` occurs exactly once) and scored in
draft against the frozen case set: **6 are killed by the frozen 92, 24 survive**. 19 of the 24 survivors are killed by 19
new oracle-labelled cases (all 19 cases pass on the pristine candidate, so they can be appended to the frozen set); 3 more
survivors are *upstream-equivalent* and unkillable by any oracle case — they expose **candidate defects** (each has an
oracle-labelled case the candidate FAILS); 2 are equivalent under the predicate or out of the modelled surface. M07 and
M11 are confirmed equivalent. No kill in this set is crash-only (QUALITY 148 clear).

## 2. Inputs read (hashes at read time = at exit)

| input | sha256 |
|---|---|
| `quality/counters/c1-r90-portal-routing.py` | read in full, unmodified |
| `.ufo/waves/round-90/controls/portal-cases-r90.json` | `d76065d00c8f3160e881681edc0ab1274e55cb173657befb4a349153540c7189` |
| `.ufo/waves/round-90/controls/portal-mutants-r90.json` | `4b5127f82ea99d564822dadf3ed8880189f25f742c4dc39a90e346ab07378582` |
| `.ufo/waves/round-90/build/mado-portals.c1.py` | `dee65d3a1adc1e23bb81598f6d802172c0294b03ac555623aff8c418f7416f17` |
| upstream `src/xdp-portal-config.c` 1.22.1 (tarball sha256 `5afeda95…` verified) | downloaded to scratch |
| upstream GLib 2.90.1 `glib/gkeyfile.c`, `glib/gcharset.c` | downloaded to scratch (declaration's cited file + the language-name source the locale rule depends on) |

The oracle binary digest and host tail digest seen in every label set are the frozen ones
(`e1429fbe…a4f8`, `4a4cf319…fbf9`), and `/etc/xdg-desktop-portal` is absent — the labels describe this host.

## 3. Method

1. Read the candidate, the counter (including `case_correct`'s reason normalization), the case generator/labels, the
   oracle, and `xdp-portal-config.c` 1:1004 plus the GLib key-file rules the candidate models.
2. Enumerated behaviour-bearing points that the 92 frozen cases do **not** appear to touch: GKeyFile whitespace/CR/locale/
   Encoding rules, D-Bus name limits, descriptor validation order, config error granularity, desktop-token validation,
   sort comparator, `*` literalness, and reason strings for empty picks.
3. Wrote 30 mutants (`mutants-extra-c1-r90.json`), each a single `find`→`replace`; verified `src.count(find) == 1` and
   that the mutated source compiles before scoring.
4. Scored in draft with the lane counter over the frozen 92 cases; for every killed mutant, re-ran with an rc-aware
   harness to separate *value* kills from *crash* kills.
5. For each survivor, authored a case in the oracle case format and obtained labels from
   `controls/portal-oracle-r90.py` (private activation-free bus). Labels were produced twice; the two runs are
   byte-identical (`labels identical: True`, same tail/bin digests).
6. Re-scored: merged 111 cases (92 + 19) under the official counter; compared pristine vs mutant per case; checked M07/M11
   against all 111.

## 4. Scores (DRAFT)

```sh
# frozen 92 cases, the 30 extra mutants
python3 -I quality/counters/c1-r90-portal-routing.py --repo <lane> --rev master --base-rev master \
  --cases controls/portal-cases-r90.json --mutants w1/mutants-extra-c1-r90.json \
  --expect-cases-sha256 d76065d0… --expect-mutants-sha256 <mutants sha> \
  --scratch-root $S/ctr --draft-tool build/mado-portals.c1.py
# rc=3
# MADO_PORTAL_ROUTING: DRAFT_TARGET_MISSED … cases=92 correct=92 mutants=30 killed=6
#   r12_rule_correct=20 host_table_correct=10 base_tool=absent base_correct=0

# merged 111 cases (92 + the 19 killing cases below), same mutants
python3 -I quality/counters/c1-r90-portal-routing.py … --cases $S/merged-cases.json \
  --expect-cases-sha256 e32edd89… --expect-mutants-sha256 88ff84b0… --scratch-root $S/ctr3 --draft-tool …
# rc=3
# MADO_PORTAL_ROUTING: DRAFT_TARGET_MISSED … cases=111 correct=111 mutants=30 killed=25
#   r12_rule_correct=22 host_table_correct=10 base_tool=absent base_correct=0
#   survivors: X03 X16 X22 X28 X30
```

`correct=111` on the merged set is the proof that the 19 new cases do not disturb the candidate: the pristine tool passes
all of them. `mutants-extra-c1-r90.json` sha256 `88ff84b091ce4a6e6e541134e141d0e345caa2ab6bd0d8f801348ee616932db9`
(earlier, before the `classification` block was added: `a72b70ad…`; same 30 mutants, same scores).

Per-mutant detail (rc-aware, `$S/detail.py`): every killed mutant returned **rc=0** on its killing case and differed in
value — no kill here rests on a crash. The 24 survivors produced **0/92** differing cases.

## 5. The 30 mutants and their verdicts

`line` is the first line of `find` in `build/mado-portals.c1.py`.

| id | line | mutation | frozen 92 | with new cases |
|---|---|---|---|---|
| X01 | 88 | `]` followed by a form feed still a group header (`strip()` not `strip(" \t")`) | survives | killed by `n01-ff-after-group` |
| X02 | 119 | every trailing CR stripped, not exactly one | survives | killed by `n02-double-cr` (reason-only) |
| X03 | 119 | final CR kept when no LF follows it | survives | **survives** — upstream-equivalent (§7-B) |
| X04 | 124 | form feed not skipped as leading line whitespace | survives | killed by `n04-ff-leading-ws` |
| X05 | 144 | tab not chugged from a value | survives | killed by `n05-tab-after-equals` |
| X06 | 145 | locale-suffixed key voids the file | survives | killed by `n06-locale-key-inert` |
| X07 | 101 | locale part of a key admits any byte but `]` | survives | killed by `n07-locale-key-chars` |
| X08 | 241 | non-ASCII desktop token kept | survives | killed by `n08-nonascii-desktop` |
| X09 | 241 | empty desktop token kept | survives | killed by `n09-empty-desktop-token` |
| X10 | 310 | sort continues past a desktop both backends match | survives | killed by `n10-sort-both-match` |
| X11 | 306 | sort matches UseIn case-sensitively | **killed by `s01-default-star`** | — |
| X12 | 202 | unknown escape kept in a plain string (DBusName) | survives | killed by `n12-plain-escape` |
| X13 | 218 | no 255-byte cap on a bus name | survives | killed by `n13-busname-256` |
| X14 | 273 | interface names not validated in a descriptor | survives | killed by `n14-bad-iface-name` |
| X15 | 272 | empty `Interfaces` element skipped, descriptor kept | survives | killed by `n15-empty-iface-element` |
| X16 | 277 | invalid UseIn escape keeps the descriptor (`use_in=None`) | survives | **survives** — upstream-equivalent (§7-B) |
| X17 | 343 | key `Default` treated as `default` | survives | killed by `n17-default-case-key` |
| X18 | 339 | a malformed value drops only that key, not the file | **killed by `g09-invalid-escape-voids-file`** | — |
| X19 | 85 | unterminated `[group` header accepted | survives | killed by `n19-unterminated-group` |
| X20 | 109 | empty group name accepted | survives | killed by `n20-empty-group-name` |
| X21 | 112 | control characters allowed in a group name | survives | killed by `n21-group-control-char` |
| X22 | 149 | bad `Encoding` value rejected (upstream check added) | survives | **survives** — upstream-equivalent (§7-B) |
| X23 | 397 | `*` recognised as a prefix | survives | killed by `n23-star-prefix` |
| X24 | 343 | interface key matched case-insensitively | **killed by `k01-iface-key-kde-filechooser`** | — |
| X25 | 452 | `find_all` does not deduplicate backends | **killed by `a05-settings-dup-entries`** | — |
| X26 | 417 | Settings UseIn fallback does not deduplicate | **killed by `a06-settings-usein-all`** | — |
| X27 | 240 | desktops split on `;` | **killed by `d06-desktop-two-hypr-first`** (reason-only) | — |
| X28 | 437 | `[]` reason reported as `none-key` | survives | **survives** — equivalent under the predicate (§7-C) |
| X29 | 171 | `\t` escape drops the character | survives | killed by `n29-tab-escape` |
| X30 | 289 | descriptor enumeration order reversed | survives | **survives** — equivalent, order not observable (§7-C) |

The six frozen-set kills (all value kills, rc=0):

- `X11` / `s01-default-star`: case-sensitive sort drops the `Hyprland` UseIn matches, so `default=*` gives
  `Screenshot=gnome` instead of `hyprland` (and `FileChooser` still `gnome`).
- `X18` / `g09`: the desktop config keeps existing after its only bad value is skipped, so `portals.conf` (`default=gnome`)
  is never reached; gives `gtk`/`gtk-last-resort` instead of `gnome`/`default config`.
- `X24` / `k01`: `FileChooser=KDE`-style casing is not the interface key; gives `gtk`/`default config` instead of
  `kde`/`interface specific config`.
- `X25` / `a05`: Settings picks `gtk,gtk,darkman` instead of `gtk,darkman`.
- `X26` / `a06`: Settings picks `gnome,kde,gnome,gtk` instead of `gnome,kde,gtk`.
- `X27` / `d06`: `Hyprland:GNOME` becomes one invalid token; same picks, wrong reasons (`gtk-last-resort` instead of
  `default config`).

## 6. Survivors A — 19 mutants killed by a new oracle-labelled case

All 19 cases are in `w1/mutc1-cases.json` under `cases` (labelled, mergeable; the pristine candidate passes every one).
Key interface shown; the full pick/reason vectors are in the labelled JSON (`oracle`, `oracle_reason`).

| mutant | case (desktop) | oracle's own label | mutant output | why the oracle says so |
|---|---|---|---|---|
| X01 | `n01-ff-after-group` (XFCE, config `[preferred]\f`) | FC `gtk` / gtk-last-resort | FC `kde` / default config | only space/tab may follow `]`; the file is void (gkeyfile.c:4647-4666) |
| X02 | `n02-double-cr` (XFCE, `default=gtk\r\r\n`) | FC `gtk` / gtk-last-resort | FC `gtk` / default config | one CR is erased before LF; the value is `gtk\r` (gkeyfile.c:1856-1861) |
| X04 | `n04-ff-leading-ws` (XFCE, `\fdefault=kde`) | FC `kde` / default config | FC `gtk` / gtk-last-resort | leading `\f` is whitespace (gkeyfile.c:1625-1626) |
| X05 | `n05-tab-after-equals` (XFCE, `default=\tkde`) | FC `kde` / default config | FC `gtk` / gtk-last-resort | value leading whitespace chugged with `g_ascii_isspace` (gkeyfile.c:1757-1758) |
| X06 | `n06-locale-key-inert` (XFCE, `default=kde` + `default[C]=gtk`) | FC `kde` / default config | config void → FC `gtk` / gtk-last-resort | a well-formed locale key is inert for routing (see defect D3 for the invalid-value half) |
| X07 | `n07-locale-key-chars` (XFCE, `default[c!d]=gtk`) | FC `gtk` / gtk-last-resort | FC `kde` / interface specific config | `!` is not in the locale alphabet, the file is void (gkeyfile.c:4584-4637) |
| X08 | `n08-nonascii-desktop` (desktop `é`) | FC `gtk` / gtk-last-resort | FC `aaa` / usein | non-ASCII token fails `validate_xdg_desktop` (xdp-portal-config.c:115-131) |
| X09 | `n09-empty-desktop-token` (desktop `:KDE`) | FC `kde` / usein | FC `gtk` / default config | the empty token is invalid, `-portals.conf` is never read (xdp-portal-config.c:127-128) |
| X10 | `n10-sort-both-match` (KDE:GNOME, `default=*`) | FC `aaa` / default config | FC `bbb` / default config | both match the first desktop → compare source names (xdp-portal-config.c:271-296) |
| X12 | `n12-plain-escape` (XFCE, DBusName `…gtk\q`, `default=gtk`) | FC `[]` | FC `gtk` / default config | bad escape ⇒ `DBusName` NULL ⇒ descriptor skipped (xdp-portal-config.c:201-213) |
| X13 | `n13-busname-256` (XFCE, 285-byte DBusName, `default=gtk`) | FC `[]` | FC `gtk` / default config | `g_dbus_is_name` rejects >255 bytes |
| X14 | `n14-bad-iface-name` (XFCE, `Interfaces=…FileChooser;…-Bad`, `default=gtk`) | FC `[]` | FC `gtk` / default config | invalid interface name voids the descriptor (xdp-portal-config.c:226-240) |
| X15 | `n15-empty-iface-element` (XFCE, `Interfaces=;…FileChooser`, `default=gtk`) | FC `[]` | FC `gtk` / default config | empty element is an invalid interface name (same lines) |
| X17 | `n17-default-case-key` (XFCE, `Default=kde`) | FC `gtk` / gtk-last-resort | FC `kde` / default config | only the exact key `default` is the default list (xdp-portal-config.c:440-449) |
| X19 | `n19-unterminated-group` (XFCE, `[preferred\ndefault=kde\n[preferred]\n…FileChooser=kde`) | FC `gtk` / gtk-last-resort | FC `kde` / interface specific config | a line that is neither group nor key/value voids the file (gkeyfile.c:1640-1655) |
| X20 | `n20-empty-group-name` (XFCE, `[]` then `[preferred]`) | FC `gtk` / gtk-last-resort | FC `kde` / default config | empty group name voids the file (gkeyfile.c:4567-4582) |
| X21 | `n21-group-control-char` (XFCE, `[pre\x01ferred]` then `[preferred]`) | FC `gtk` / gtk-last-resort | FC `kde` / default config | control characters are rejected in group names (gkeyfile.c:4572-4577) |
| X23 | `n23-star-prefix` (XFCE, `default=*x`) | FC `[]` | FC `aaa` / default config | only the exact entry `*` means any backend (xdp-portal-config.c:749-753) |
| X29 | `n29-tab-escape` (XFCE, `default=g\ttk`) | FC `[]` | FC `gtk` / default config | `\t` decodes to a tab; `g<TAB>tk` is not a backend name (gkeyfile.c:4724-4726) |

Reproducing input for each is the case's `files` + `desktop` in `w1/mutc1-cases.json`; the oracle's label is the
`oracle`/`oracle_reason` pair in the same file.

Two of these kills (X02, and the `Notification` part of X09) rest on the **reason** field only — the picks are equal and
`case_correct` fails on the reason. That is within PRED-C1-r90-v1 as written (the tool must answer "exactly as the oracle
labels it", reasons included), but if the predicate is ever relaxed to picks-only, `n02-double-cr` stops killing X02.
The other 17 differ in picks as well.

## 7. Survivors B/C — the five that no frozen or new case kills

### B. Upstream-equivalent mutants = candidate defects (X03, X16, X22)

These three mutants make the tool behave like xdg-desktop-portal; the oracle therefore agrees with them on every input and
**no case can kill them** — they are not gaps in the case set, they are places where the candidate is wrong. Each has an
oracle-labelled case in `w1/mutc1-cases.json` under `candidate_divergence_cases`; the case **fails the pristine
candidate** and passes the mutant. Do not append these three to the frozen set (they would make `correct == cases`
unreachable); fix the candidate or declare a named limit.

**D1 — a final bare CR is treated as CRLF.** `build/mado-portals.c1.py:120-122` strips `\r` from every line, but GLib
erases a CR only when it is followed by LF (`gkeyfile.c:1856-1861`; the last buffer is flushed at `gkeyfile.c:1003`).
Reproducer `n03-final-cr`: desktop `XFCE`, `xfce-portals.conf` = `[preferred]\ndefault=gtk\r` (no final LF), `gtk.portal`
with `DBusName=…desktop.gtk` and `FileChooser`, `UseIn=gnome`.
Oracle: `FileChooser=gtk` **gtk-last-resort** (the value is `gtk\r`, not a backend). Candidate: `FileChooser=gtk`
**default config** (wrong reason). Mutant X03: gtk-last-resort (matches).

**D2 — an invalid `UseIn` does not void a descriptor.** `build/mado-portals.c1.py:277` parses `UseIn` inside the same
`try` as everything else, so a bad escape drops the whole descriptor. Upstream passes the `GError**` to
`g_key_file_get_string_list` and never checks it (`xdp-portal-config.c:244-248`), so the descriptor is registered with
`use_in = NULL`. Reproducer `n16-bad-usein-escape`: desktop `XFCE`, `hypr.portal` with `UseIn=wlroots\q` and
`Screenshot`, `xfce-portals.conf` = `[preferred]\ndefault=hypr`.
Oracle: `Screenshot=hypr` **default config**. Candidate: `Screenshot=[]` (descriptor skipped). Mutant X16: hypr (matches).

**D3 — the key file `Encoding` rule is not modelled.** The candidate has no Encoding check at all
(`build/mado-portals.c1.py:115-152`); GLib rejects a first-group `Encoding` whose value is not exactly `UTF-8`
(case-insensitive, `gkeyfile.c:1768-1786`), which voids the whole file — including a `.portal` descriptor.
Reproducer `n22-bad-encoding`: desktop `XFCE`, `gtk.portal` = `[portal]\nEncoding=latin1\nDBusName=…desktop.gtk\n…`,
`xfce-portals.conf` = `[preferred]\ndefault=gtk`.
Oracle: `FileChooser=[]` (descriptor void). Candidate: `FileChooser=gtk` **default config**. Mutant X22: `[]` (matches).

The three are outside the declaration's named limits (they are not locale/dir-order/UTF-8 issues) and each is a single
local rule; D1 and D2 are silent misroutes, D3 is a false backend.

### C. Equivalent under the measured contract

**X28 — `[]` reason renamed `no-backend` → `none-key`** (`build/mado-portals.c1.py:437`). The oracle emits no decision
line when nothing is chosen (`xdp-portal-config.c:923` returns the gtk fallback result; when that is NULL nothing is
logged), so `oracle_reason` has no entry; `case_correct` maps both strings to `None`
(`quality/counters/c1-r90-portal-routing.py`, `why = None if why in ("none-key", "no-backend")`). No case can differ.
Note for the L1: the tool's own documentation distinguishes the two, so the *predicate* cannot see this documented
distinction — not a defect, but a known blind spot of PRED-C1-r90-v1.

**X30 — descriptor enumeration order reversed** (`build/mado-portals.c1.py:289`). Within a directory the source name is
the basename up to the last `.portal`, so two distinct files cannot share a source (the only order-sensitive step,
`xdp-portal-config.c:192-199` first-wins); every collected impl is then re-sorted by a total order
(`xdp-portal-config.c:267-296`), so collection order never reaches the output. This is also the declaration's named limit
("directory enumeration order only matters for same-named descriptors within one directory (impossible)"). Equivalent.

## 8. The L1's two `equivalent_not_counted` claims — agree on both

**M07 (`*` does not stop the list) — agree.** The mutation only changes the branch where **no** backend implements the
interface (`return None` → `continue`). Upstream returns NULL from `find_any_impl_config` in exactly that case
(`xdp-portal-config.c:694-711`), and a later named entry is resolved through `find_impl_config_by_name` +
`supports_iface` (`xdp-portal-config.c:761-771`), which cannot match when no backend supports the interface. Continuing therefore cannot
change the result. Empirical check: M07 scored against 92 frozen + 19 new + 3 evidence cases = 111 cases, **0
differences** (all oracle-identical).

**M11 (UseIn fallback backend-major) — agree.** The comparator orders backends by the first current desktop whose
`UseIn` names one but not the other, breaking to a `strcmp` of the source names when both match
(`xdp-portal-config.c:267-296`); the resulting order is exactly "first matching desktop index, then source". A
backend-major scan over that order (`xdp-portal-config.c:897-921`) returns the same first hit as the desktop-major scan, and for `find_all`
(`xdp-portal-config.c:969-993`) collects the same sequence with the same de-duplication. Empirical check: 111 cases, **0 differences**.

Neither argument depends on anything the tests do not exercise; both are structural. I found no case that refutes them.

## 9. Notes for the freeze

- Recommended additions: the **19** mutants `X01 X02 X04 X05 X06 X07 X08 X09 X10 X12 X13 X14 X15 X17 X19 X20 X21 X23 X29`
  with the 19 `cases` from `w1/mutc1-cases.json`. With them the frozen predicate would read
  `cases=111 correct=111 mutants=<31+19> killed=<all>` (kills are monotone in the case set, so the existing 31 stay
  killed; the draft merged run already shows `correct=111` and `killed=25/30` for this file).
- **Do not** add X03/X16/X22 (upstream-equivalent; their cases fail the candidate — §7-B) or X28/X30 (§7-C).
- If any of D1/D2/D3 is fixed in the candidate before the freeze, X03/X16/X22 become ordinary mutants that the evidence
  cases in `candidate_divergence_cases` kill; in that case move those three cases into `cases` as well.
- The mutants file keeps the frozen JSON shape (`note`, `mutants`, plus a `classification` block the counter ignores).

## 10. Environment / installs

No package installs, no pacman transactions, no service restarts. `curl` fetched the pinned upstream tarball
(`sha256 5afeda95…` verified) and two GLib 2.90.1 source files into scratch only.

## 11. Integrity, restoration and scratch

- The candidate and both frozen control files were only ever **read**: their sha256 at the end of the seat equals the
  values recorded at the start (`dee65d3a…`, `d76065d0…`, `4b5127f8…`). No mutation was ever applied outside scratch.
- Files written in the lane: `w1/R90MMutC1.md`, `w1/mutants-extra-c1-r90.json`, `w1/mutc1-cases.json`. Nothing else.
- Scratch `S=/fast/scratch/hyaku/mado-r90/R90MMutC1` (downloaded sources, helper harnesses, merged case file, counter
  scratch roots `ctr*`, oracle scratch roots `orc*`) was removed on exit; `S` does not exist after this seat.
