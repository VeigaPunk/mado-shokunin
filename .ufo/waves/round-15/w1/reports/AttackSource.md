# AttackSource — round 15 w1 (critic)

Axis: **coverage** (C1 U6 source joins). I attacked three things: source semantic joins, mutable docs revisions, and duplicates of the existing libinput row S007.
I checked the working tree as it stood at about 04:31 -03 on 2026-10-20. L1 was still integrating, so the files moved during the review: SCORECARD.md at 04:25 and 04:30, SOURCES.md at 04:29, the note at 04:28, measure.py at 04:27.
Each finding below is marked **RESOLVED** or **RESIDUAL** against the latest bytes.

## Verdict

The landed S051/S052 design holds against my strongest counterexamples.
- S051 pins `tools.rst` to tag 1.32.0. S052 pins `wayland.xml` to tag 1.26.0. Each row carries its raw sha256.
- S051's teaches cell opens `supersedes S007 —`. S007 stays `queued`.
- The note, SOURCES, SCORECARD:606-610 and measure.py:13-22,155 now all agree on S051/S052.

Five defects remain. All are fixable; none needs a judge-level tradeoff:
- two anchor line ranges cut XML elements short (A4);
- measure.py joins rows by id only (A5);
- cited rows that are not mined are dropped silently (A6);
- the docs-era stability of the cited claims is not recorded (A3);
- one search-log sentence is too broad (A7).

## Findings

**A1. Identity churn across artifacts — RESOLVED, but the history needs a trail.**
- Counterexample: during the round the ids had two incompatible meanings. Under the first, S051 was the Wayland XML.
  - `input-draft.txt:1` (04:27:18) still reads: source `S007 (…doc/latest/tools.html…)`, `S051 (/usr/share/wayland/wayland.xml …)`.
  - The SCORECARD round-15 claim (04:25:34) read: "reciprocal mined A/B source joins S007/S051 … reuses queued S007; S051 is the new distinct input-XML scope".
  - The measure.py docstring at the same time had `U6_SOURCES = ('S007','S051')`.
- Final state: S051 = libinput tools.rst, S052 = Wayland XML (SOURCES:63-64; note:1,10-11; measure.py:155; SCORECARD:606-610).
- Impact: false provenance if any reviewer report or the draft is cited for an id. Peer acceptance criteria (ReviewSourceTier, AttackCoverage, ReviewDocsEra) assume S051 = libinput; the draft assumes S051 = XML.
- Smallest correction:
  - The lesson records the id reassignment old→new: S007/S051(XML) → S051(libinput)/S052(XML).
  - It also states that `input-draft.txt` is a superseded scaffold and not a provenance source.
  - The in-place SCORECARD rewrite was never committed (`git show HEAD:SCORECARD.md | grep -c 'Round 15'` → 0), so a lesson note is enough.

**A2. Mutable docs: the "1.32.0" banner does not prove the tag — RESOLVED by S051, with a recorded caveat.**
- Evidence:
  - Every page under `doc/latest/` is regenerated. `Last-Modified` for tools.html is 2026-10-19 11:28:47 GMT; the doc index shows 11:28:59.
  - The page bytes (sha256 `524c1776…`) carry no build commit.
  - libinput `main` HEAD is `4cf1775d3ddf7f70d13b70b3f2149a9be880a855` (2026-10-16, `git ls-remote`), 7 commits past tag 1.32.0 (`5cf833b5…`). It still declares `version : '1.32.0'` in meson.build. A build from main would therefore show the same "libinput 1.32.0 documentation" banner.
  - The GitLab compare 1.32.0→4cf1775 touches `tools/libinput-record.c`, which now records ID_INTEGRATION, and `doc/user/switches.rst`. It does not touch `doc/user/tools.rst`.
  - Raw `tools.rst` at 4cf1775 has sha256 `53264328…`, identical to the tag. Today's latest-page content therefore matches S051 by coincidence of an untouched file, not because of the banner.
- Corrections to peers:
  - LayerJoin.md:25 says latest.html is "generated from git commit `4cf1775`". The page bytes do not show that; 4cf1775 is only the current tip of main. `[INFERENCE]` is the most that claim can carry.
  - SOURCES:197 says "the apparently versioned libinput HTML path returned 404". That is true for `/doc/1.32.0/` and `/doc/1.31.3/`. The index `https://wayland.freedesktop.org/libinput/doc/` does list versioned trees up to `1.31.0`, whose `tools.html` returns 200 with a "1.31.0 documentation" banner.
- Smallest correction: keep S051 as the only admitted libinput anchor. Never re-admit `doc/latest`. Narrow SOURCES:197 to "the 1.32.0 versioned path".

**A3. Docs era vs installed vs running library — RESIDUAL. A one-line strengthening is available.**
- Evidence:
  - First `pacman -Q` in this seat: `libinput 1.31.3-1`, and `libinput-tools` not found.
  - `/var/log/pacman.log`, 04:25:16: `Running 'pacman -S --needed --noconfirm libinput libinput-tools'`, then at 04:25:17 `upgraded libinput (1.31.3-1 -> 1.32.0-1)`. It installed python-libevdev, python-pyudev, python-yaml and libinput-tools 1.32.0-1, and ran `35-systemd-udev-reload.hook`.
  - `pacman -Qu | wc -l` → 413 pending updates. They include `aquamarine 0.15.0-2 -> 0.15.1-1`; aquamarine depends on `libinput`. They also include hyprland and systemd. This was a targeted partial upgrade of a library the compositor depends on, plus a udev reload. ReviewDocsEra F1/F2 reports the same event and a `(deleted)` 1.31.3 mapping in Hyprland. I did not re-read `/proc`.
- Counterexample: S051 (1.32.0) differs from 1.31.3 `tools.rst` (sha `20bcf797…`) in the very `libinput-record` section the note cites. 1.32.0 adds `record --no-events` and removes `--multiple`. It also says recording waits for device activity before creating the output file.
- I checked the lines S051 actually cites. They are byte-identical in both tags:
  - helper root sentence `:31-32`;
  - list-devices built-in-defaults note `:45-46`;
  - debug-events options `:141-143`;
  - record kernel-events independence `:220-223`;
  - key-code obscuring `:262`;
  - replay virtual device `:276`.
  So the cited claims hold in both eras.
- Smallest correction: add one sentence to the note's version boundary or the lesson. It should name the 1.31.3 tag raw sha `20bcf797…` and say the cited sections are unchanged between 1.31.3 and 1.32.0, while the `record` CLI forms differ and are not cited. No new row is required. This closes the runtime-1.31.3 vs on-disk-1.32.0 gap for the admitted claims.

**A4. Anchor line ranges cut elements short — RESIDUAL, low.**
- SOURCES:64 gives S052 as `wl_seat :2004-2086, wl_pointer :2138-2260, wl_keyboard :2573-2699`. The note:35 range is `XML:2138–2260`.
  - In `/usr/share/wayland/wayland.xml`, which matches tag 1.26.0 (sha `cc860987…`):
    - `wl_pointer.button` starts at :2244 and closes at :2264. The range stops at :2260, inside the description, and excludes the `serial/time/button/state` args (:2261-2264).
    - `get_keyboard` closes at :2087, one line past the range.
    - `wl_keyboard.key` closes at :2699. That range is correct.
- Smallest correction: use `wl_seat :2004-2087` and `wl_pointer :2138-2264` in both the row anchor and the note. The S052 row is new this round, so this is the moment to fix it.
- The draft's ranges `:2004-2137/2138-2572/2573-2753` run one line past each interface closer (`</interface>` at 2136/2571/2752). They are moot now that the draft is superseded.

**A5. The measure join is id-only; an identity swap passes — RESIDUAL. Hardening, not a defect in the current bytes.**
- measure.py:208 `reserved = {sid: mined_ab(sid, path) for sid in U6_SOURCES}` checks only status, tier, `used-by` and citation by id.
- Counterexample: land S051 = Wayland XML and S052 = libinput, the draft's original assignment, with both mined and reciprocal. Facets and reserved pass, the score reads 6/7, and every reviewer criterion keyed to "S051 = libinput" is silently violated. A1 shows this swap actually happened in-round.
- Smallest correction: one structural assertion per reserved id. It does not judge semantics:
  - the S051 source cell contains `libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`;
  - the S052 source cell contains `wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`;
  - each anchor's 64-hex sha256 appears verbatim on the note's head-15 `source:` line.
  Report this as `reserved_identity` next to `reserved`.

**A6. Cited rows that are not mined are silently dropped — RESIDUAL.**
- measure.py:178-180 keeps only mined, used-by-reciprocal ids. The `inverse` check (:212-213) runs one way only: it catches rows that list the note in `used-by` but are not cited.
- Counterexample: the draft header cites queued `S007` on the `source:` line. With S051/S052 mined, U6 would still count, so an unpinned queued row rides on an admitted note without being flagged.
- Smallest correction: report `cited_unmined` (cited ids not mined, or not listing the note in `used-by`). For U6, require it to be empty, or at least to exclude S007. The current note cites only S051/S052, so this changes nothing today.

**A7. Duplicates of existing libinput/Wayland rows — RESOLVED as designed. The census cannot see them; the disclosure is prose-only.**
- `scripts/sources-census.sh:600-653`:
  - `url_of` takes the first `https?://` URL in the source cell and strips the fragment and the trailing `/`.
  - W04 fires on the same URL with a different scope string.
  - E04 fires on the same URL with the identical scope string, a non-rejected prior row, and no `supersedes S###`.
- S051's raw-tag URL differs from S007's `doc/latest` URL, so the census emits neither W04 nor E04. The supersession is machine-visible only through the `supersedes S007 —` marker, which is present (SOURCES:63).
- S052 and S043 cover the same bytes (sha `cc860987…`). S043's census key is `wayland.freedesktop.org/docs/html/apa.html`; the local path is ignored and the `#protocol-spec-wl_registry` fragment is stripped. S052's key is the GitLab raw URL. The census therefore shows no overlap at all. The relation exists only in the SOURCES:195-196 search log ("same core XML as S043 but a disjoint input-contract scope") and in S052's scope cell.
- Counterexample to watch: any future row citing `apa.html#protocol-spec-wl_keyboard` would collide with S043 under W04, because both reduce to `…/apa.html`.
- `[INFERENCE, static read; census not executed]`: after S051/S052, the expected warnings are still W04 S030/S042/S045 and nothing new.
- Smallest correction: none required. Optionally, S052's teaches or anchor could name "same bytes as S043" so that the row itself carries the overlap rather than only the search log.

**A8. The S007 owed-anchor omission is historical — RESOLVED by supersession.**
- SOURCES:115 (round-12 errata) lists S006, S008, S009 and S010 as owing revision anchors and omits S007, which has the same defect: a mutable `latest` URL with only a version label.
- S051 now pays that debt, so no action is needed beyond A1's lesson note.
- The historical U4/U6 frontier path (SOURCES:72) still ends at S007. The appended U6 path (:86-91) redirects to S051, following the round-13 U2 path-correction pattern. That is consistent.

## Evidence commands (read-only)

- Packages:
  - `pacman -Q libinput wayland wayland-protocols libxkbcommon hyprland` → 1.31.3-1 (first read), 1.26.0-1, 1.49-1, 1.13.2-1, 0.56.2-2.
  - Later `pacman -Q libinput-tools` → 1.32.0-1, and `pacman -Qo /usr/bin/libinput` → libinput-tools 1.32.0-1.
  - `pacman -Qu | wc -l` → 413.
- `sha256sum /usr/share/wayland/wayland.xml` → `cc860987…5f07`; `wc -c` → 168656.
- Raw fetches to `/tmp/as15` with `curl` + `sha256sum`:
  - libinput `raw/1.32.0/doc/user/tools.rst` → `53264328…`;
  - libinput `raw/1.31.3/…` → `20bcf797…`;
  - libinput `raw/4cf1775…/…` → `53264328…`;
  - wayland `raw/1.26.0/protocol/wayland.xml` → `cc860987…`, blob `28babc70…`, last commit `c28d9417…`.
- GitLab API: libinput tags (1.32.0 `5cf833b5…` 2026-09-17; 1.31.3 `26191d39…`); wayland tags (1.26.0 `87cc8a87…`); compare 1.32.0→4cf1775 (7 commits, file list above); `meson.build` version at the tag and at main.
- `curl -w` HTTP status / Last-Modified for `doc/latest/tools.html` (200), `doc/1.32.0/` (404), `doc/1.31.3/` (404), `doc/1.31.0/` (200), `docs/html/apa.html` (200).
- Static reads of SOURCES.md, SCORECARD.md:598-615, the round-14 and round-15 measure.py, input-draft.txt, the U6 note, `scripts/sources-census.sh`, and `/var/log/pacman.log`.
- Not run: no libinput subcommand, no `/dev/input` access, no `/proc` read, no hyprctl, no compositor action, no census/gate/test run, no omp CLI, nothing under agent.db* or any credential/auth file.

## Tooling

- This seat installed or updated nothing.
- Observed but not done by this seat: the 04:25:16 `pacman -S --needed --noconfirm libinput libinput-tools` transaction (libinput 1.31.3-1→1.32.0-1, plus libinput-tools 1.32.0-1, python-libevdev 0.13.1-1, python-pyudev 0.24.4-1, python-yaml 6.0.3-2). The actor is unidentified. It was a partial upgrade with 413 updates still pending, and the round record must carry its tool/version/channel/reason.
