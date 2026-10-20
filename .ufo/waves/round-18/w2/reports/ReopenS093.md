# Re-open S093 — non-author check of a newly credited row (R17-V3)

Verdict: **agree**. Row text at `corpus/SOURCES.md:105` (single line). Every sha in
its anchor cell reproduces from a fresh fetch, the tag resolves to the commit the
row names, the cited line ranges contain what the row and the citing note say, and
`corpus/knowledge/theme-route-r18.md` uses the source without overreach.

Seat receipts: `.ufo/waves/round-18/fetch/ReopenS093/receipts.jsonl` (5 lines,
schema `mado-fetch-receipt-v1`; bodies in the same directory, re-hashed after
write, 5/5 match their receipt).

## Commands run and their output

1. Row read: `sed -n '105p' corpus/SOURCES.md` — id S093, source cell names the
   tag URL plus `bin/omarchy-theme-bg-next`, `bin/omarchy-theme-bg-set`,
   `bin/omarchy-theme-set-templates`, `default/hypr/autostart.conf` and
   `commit 8fcc9d6048af4cb0e3af8512c78049857a3b53dd`; kind `code`, tier `A`,
   status `mined`, used-by `corpus/knowledge/theme-route-r18.md`.

2. Tag resolution:
   `git ls-remote --tags https://github.com/basecamp/omarchy 'refs/tags/v3.8.4*'`
   → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4` (rc=0, one line;
   no `^{}` peeled line, so `v3.8.4` is a lightweight tag on that commit). The
   commit equals the row's commit cell. **The URL is tag-pinned**: its ref segment
   is `v3.8.4`, not a branch.

3. Fresh fetch of the row's primary file and three further files it lists
   (`curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}' URL`;
   all four returned `200` and the same URL):

| file | bytes | sha256 measured | row anchor | wave-1 receipts |
|---|---|---|---|---|
| `bin/omarchy-theme-set` | 2147 | `79069c8018a7d6d20f52e357b0b473bd99fad0c5f2914523171687103eeb9516` | identical | 5/5 identical |
| `bin/omarchy-theme-bg-next` | 1650 | `ee4828127755566d48b46a3775d431601a4d56a9114277ddc78b49c273196c6a` | identical | 4/4 identical |
| `bin/omarchy-theme-bg-set` | 671 | `638f265f3a8e62e4d477499627a8f270049df838f038db4f95837acf29acdc05` | identical | 4/4 identical |
| `default/hypr/autostart.conf` | 742 | `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` | identical | 3/3 identical |

   Fifth file `bin/omarchy-theme-set-templates` was not re-fetched by me (three-file
   cap); its anchor `01264122666b3d49d4e976837db70d9f9962aa6afd1b2531010c8d7c7d0ea9c0`
   is reproduced by re-hashing the stored bodies of three independent seats
   (`SrcOmarchyThemeSet`, `SrcOmarchyThemeHooks`, `NoteTheme`) plus wave-2 peer
   `ReviewThemeUpstream`.

4. Commit-pin cross-check:
   `curl … https://raw.githubusercontent.com/basecamp/omarchy/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/bin/omarchy-theme-set`
   → `200`, 2147 B, sha256 `79069c80…9516`, byte-identical to the tag URL. The ref
   name and the commit name agree on the same bytes today.

5. All wave-1 receipts for these URLs: a scan of every
   `.ufo/waves/round-18/fetch/*/receipts.jsonl` found **20 rows across five seats**
   (`NoteTheme`, `SrcOmarchyBackground`, `SrcOmarchyThemeHooks`,
   `SrcOmarchyThemeLayout`, `SrcOmarchyThemeSet`), one sha per file, no dissenting
   digest, byte counts matching mine. I then re-hashed the 26 stored bodies those
   receipts point at: **26/26 match their receipt sha256 and byte count** (including
   the non-upstream `config_hypr_autostart.conf`, 65 B). A separate wave-2 peer,
   `ReviewThemeUpstream`, fetched the same five files at 16:00:31Z and agrees.

6. Host copies quoted by the note: `sha256sum` on
   `~/.local/share/omarchy/{bin/omarchy-theme-set,bin/omarchy-theme-bg-next,bin/omarchy-theme-bg-set,bin/omarchy-theme-set-templates,default/hypr/autostart.conf}`
   returned exactly the five tag digests above — the note's "byte-identical to the
   tag files" claim holds for all five (byte read only; no command executed).

## Line anchors (checked with `nl -ba` on the fetched bodies)

- `omarchy-theme-set` 17 (name derivation: tag strip, lower, space→hyphen), 19-22
  (refusal when neither dir exists), 29-30 (official copy then user overlay into
  `next-theme`), 34 (colors.toml synthesis), 38 (template renderer call), 41-42
  (`rm -rf current/theme`; `mv next-theme current/theme`), 45 (`theme.name`),
  48-50 (bg-next unless `OMARCHY_THEME_SKIP_BACKGROUND=1`), 53-62 (waybar only if
  running, swayosd, terminal, hyprctl, btop, opencode, mako, helix), 65-70 (six app
  setters), 73 (theme-set hook). **No `swaybg` anywhere in 53-73.**
- `omarchy-theme-bg-next` 6 (`cat current/theme.name`), 7-9 (theme backgrounds,
  user backgrounds, link path), 11 (`find -L … -maxdepth 1 -type f -print0 | sort -z`),
  14-17 (zero-background branch: `pkill -x swaybg`, then
  `swaybg --color '#000000'` — no `-m fill` there), 41 (wrap `% TOTAL`),
  46 (`ln -nsf "$NEW_BACKGROUND" "$CURRENT_BACKGROUND_LINK"`), 49-50
  (`pkill -x swaybg`; `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`).
- `omarchy-theme-bg-set` 12 (`realpath`), 21 (`ln -nsf`), 24-25 (pkill, relaunch
  on the link with `-m fill`).
- `omarchy-theme-set-templates` 6 (`$OMARCHY_PATH/default/themed`), 38 (user `*.tpl`
  first, built-in second), 43 (render only when the output file is absent).
- `default/hypr/autostart.conf` 5
  `exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill`.

## Judgments

- **kind `code`** — bash source, correctly typed; not docs or a dataset.
- **tier A** — first-party project repository bytes at a release tag, i.e. a primary
  source for the stated scope ("upstream Omarchy theme-set and background writers,
  template renderer, and the swaybg autostart declaration"). No community restatement
  or generated index is involved.
- **scope keyword (P5)** — `measure.py` tests `source + ' ' + scope`; the source cell
  contains "theme writers" and the scope cell contains "theme-set … swaybg autostart
  declaration", so both `theme` and `swaybg` hit `SURFACE_KEYWORDS['P5']`. The row is
  mined / tier A / used-by the note, so it satisfies the instrument's upstream test.
  (The instrument does not itself check receipts — M6 stays an external discipline —
  but this row's receipts exist, are committed, and agree.)
- **`teaches` grounded** — every clause maps to bytes: payload copy (29-30),
  template render into `next-theme` (38 + set-templates 8/43), swap (41-42),
  `theme.name` (45), bg-next call (48-50), `ln -nsf` retarget in both writers
  (bg-next 46, bg-set 21), relaunch with `-m fill` on the link (bg-next 50,
  bg-set 25), swaybg absent from the restart list (53-62). One bounded nuance: the
  bg-next zero-background branch relaunches `swaybg --color '#000000'` instead; the
  row's anchor cell cites 14-17 and the note states that branch explicitly, so the
  summary is incomplete rather than false. The trailing caveat "Does not show the
  host ran any of these" is correct and is the right scope for a `mined` row.
- **Citing note truthful** — `theme-route-r18.md` carries `surface: P5` (line 4) and
  `source: … S093 …` (line 1); every `[OT]/[OB]/[OS]/[OP]/[OA]` citation I checked
  lands on the quoted statement, including `[OB:49-50]` ("the swaybg argument is the
  link, not the image"), `[OA:5]` verbatim, and `[OP:43]` as the payload-wins rule.
  Only immaterial slip: `[OB:7-9]` describes the user background dir before the theme
  dir, while the file assigns theme (7) then user (8); both paths are named correctly.
  The note's host-copy-equality claim is confirmed by the hash comparison in step 6.
  The note marks its 24-file arithmetic `[INF]` and keeps behaviour `[UNK]`.

## Attack limits (remaining unknowns)

- Tag-pinned is not commit-immutable: `raw.githubusercontent.com` resolves a mutable
  ref name, so a future force-retag would change the bytes. The row records the
  commit, and today tag→commit→bytes agree; a reader can detect drift by re-running
  step 3/4.
- Nothing was executed: no script, no `omarchy-*` command, no swaybg, no process or
  compositor state. The row claims source semantics only, and the note matches that.
- Receipts are seat-written JSON; re-hashing proves the stored bodies match the
  claimed digests, not the network provenance. Independently, four seats and this
  seat produced identical bytes for `omarchy-theme-set`, which is the property
  R17-V3 asks for.

GATE | S093 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/hypr/autostart.conf | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS093/autostart.conf:5 "exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill" (9 words) | acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441 | agree: fresh fetch reproduces the row anchor and all three wave-1 receipts; tag v3.8.4 resolves to the row's commit 8fcc9d60 and the commit-pinned URL is byte-identical; every cited line and the teaches sentence ground in these bytes; the note quotes them without overreach
