# ScoutQuarantine — mado register slice + 3-row hand-check

## Slice derivation

Command (awk verbatim from the round-33 prompt, §10 *Quarantine*):

```sh
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R" > .ufo/waves/round-33/scratch/ScoutQuarantine/slice.txt
```

Output: `mado-shokunin/.ufo/waves/round-33/scratch/ScoutQuarantine/slice.txt`, **13 rows** —

```
 S189   `payload-absent`
 S195   `payload-absent`
 S201   `payload-absent`
 S205   `payload-absent`
 S224   `payload-absent`
 S228   `payload-absent`
 S199`   the cited source could not be fetched, so no quote was checked
 S200`   the cited source could not be fetched, so no quote was checked
 S209`   the gate block named no locator, so no quote was checked
 S222`   the gate block named no locator, so no quote was checked
 S223`   the gate block named no locator, so no quote was checked
 S225`   the gate block named no locator, so no quote was checked
 S235`   the gate block named no locator, so no quote was checked
```

Composition: 6 `payload-absent` rows (S189, S195, S201, S205, S224, S228) — the
quarantine set — plus 7 unchecked-family rows (S199, S200, S209, S222, S223,
S225, S235) where field 5 is the register's "why it was not checked" cell, not
a class. Register's `## By lane` summary claims `mado | 6`; that counts only
the payload-absent family, while the awk catches both — consistent with the
prompt's warning that register summary totals are stale/derivable.

S190/S191/S197 do not occur in the mado slice at all (exclusion clause is a
no-op for this lane — those seats cover fetch/ artifacts, not register rows).

## Hand-checks (3 rows, all remote-cited; S224 cites `/home/vgpnk/.cache/…` and
S228 cites `lanes/mado/…`, so the URL-bearing candidates were S189/S195/S201/S205)

### S189 — PRESENT

- Cited: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp`
- Fetch: `curl -sS -o /tmp/mado-s189-EventManager.cpp` → **HTTP 200, 6479 bytes**.
- Register quote: `` auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024)); ``
- Located quote — byte-identical at line 128 of the fetched file:

  ```cpp
  128:    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));
  129:    std::replace(eventString.begin() + event.event.length() + 2, eventString.end() - 1, '\n', ' ');
  ```

- Note: the register's `payload-absent` verdict is a **false negative** against
  the very commit it pins. The line is verbatim in the fetched payload.

### S201 — PRESENT

- Cited: `https://arxiv.org/abs/2604.18860`
- Fetch: abs page → **HTTP 200, 42386 bytes** (title: "Temporal UI State
  Inconsistency in Desktop GUI Agents: Formalizing and Defending Against
  TOCTOU Attacks on Computer-Use Agents"). Neither quoted sentence is in the
  abstract text itself (abstract discusses TOCTOU window, "100%
  action-redirection success rate" but not these sentences verbatim).
- The abs page links `https://arxiv.org/html/2604.18860v1` (HTML fulltext);
  fetch → **HTTP 200, 243019 bytes**. Both register sentences located verbatim:

  ```
  Desktop agents interact across disjoint applications, manage overlapping windows
  ```

  ```
  that dynamic UI manipulation — such as notification overlays and X11 window
  focus hijacking — can redirect agent actions with up to 100% success rates
  ```

  (register's first quote shows trailing `X11/Wayland compositors` truncated in
  the register cell; the sentence continues past that point in the source.)
- Verdict hinges on whether the abs landing page's linked HTML fulltext counts
  as the cited payload — the quotes are verbatim in the arXiv page for the
  same identifier, so PRESENT.

### S205 — PRESENT

- Cited: `https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json`
- Fetch: `curl -sS -A 'mado-shokunin-scout/1.0'` → **HTTP 200, 8313 bytes**
  (compact JSON — the live API no longer emits the pretty-printed form the
  register quote was drawn from).
- Located quote (JSON-escaped `\u` sequences decode to the same characters;
  whitespace differs only because the response is now single-line):

  ```json
  {"prefix":"zh-hans","local":"","language":"\u4e2d\u6587\uff08\u7b80\u4f53\uff09","bcp47":"zh-Hans","url":"https://wiki.archlinuxcn.org/wiki/$1"},
  {"prefix":"zh-hant","local":"","language":"\u4e2d\u6587\uff08\u7e41\u9ad4\uff09","bcp47":"zh-Hant","url":"https://wiki.archlinux.org/title/$1_(\u6b63\u9ad4\u4e2d\u6587)"}
  ```

- Both register cells map exactly: `"prefix": "zh-hans", "url":
  "https://wiki.archlinuxcn.org/wiki/$1"` and `"prefix": "zh-hant", "url":
  "https://wiki.archlinux.org/title/$1_(正體中文)"`. PRESENT modulo
  whitespace/unicode-escape serialization.

## Remaining slice rows (not checked — seat scope was three)

- payload-absent, unverdicted: **S195** (sjtu mirror `.pkg.tar.zst`), **S224**
  (`/home/vgpnk/.cache/ai-usage/status.json` — host-local path, not a URL),
  **S228** (`lanes/mado/round5/fetch/cn-export-hyprland.html` — lane-local
  artifact path).
- unchecked family (register says "not fabrication; re-fetch or mark
  unverifiable"): S199, S200 (CSDN blogs, fetch-failed), S209, S222, S223,
  S225, S235 (gate blocks named no locator).

## Boundary notes

- Register untouched (read-only). Slice file written only under
  `scratch/ScoutQuarantine/`; fetched payloads kept in `/tmp/mado-s*.{cpp,html,json}`.
- Finding worth folding into the lane lesson: the register's payload-absent
  class produced at least one provable false negative (S189, verbatim at the
  pinned commit) — hand-check before any fabricated-quote verdict stands, per
  the register's own "candidate, not verdict" header.
