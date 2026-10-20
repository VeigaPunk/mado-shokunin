# CriticC2W2 — falsify C2 (rubric V 6/6) at 4c103b55b1ea5c3c555884afe3eb69b5189701b7

Seat: MadoR18.CriticC2W2 (critic, leaf). Scope: P3 `corpus/knowledge/walker-route-r18.md` and
P5 `corpus/knowledge/theme-route-r18.md`, rows S072–S095, round-18 fetch receipts.
Writes: this report only. No fetches, no lane tool other than `measure.py`, no package/service/process
command. One scratch clone, `/tmp/c2w2`; mutant commits were made only there.

## Verdict

**The 6/6 credit holds.** P5 depends on swaybg (S092) and the omarchy theme and background writers
(S093). It does not depend on walker theme code. P3 depends on walker and elephant tag sources.
Every anchor digest in a credited web row has a committed HTTP 200 receipt with the same sha256.
I found these defects, all fixable by rewording:

- **(D1)** One P5 sentence claims live behaviour outside `## Unexercised behavior`. It contradicts the note's own `[UNK]`.
- **(D2)** One P3 sentence asserts host behaviour from a function the note says it did not read.
- **(D3)** The SCORECARD wording overstates the evidence: receipt *bodies* are not in the revision, and
  host rows have no receipts.
- **(D4)** S094 and S084 rest on single-fetch support that cannot be re-checked or is unpinned. The round-18 lesson says
  to reject or not row that kind of support. Neither row is needed for the credit.

**Instrument limits:** two mutants show that `measure.py` would credit P5 using only walker
theme code, and P3 using only the xdg docs row (M1, M5). This is a gap for round 19, not a defect in the
credit that landed.

## Commands run and output

1. `python3 .ufo/waves/round-17/measure.py 4c103b55b1ea5c3c555884afe3eb69b5189701b7`, rc 0:
   `c2.count 6, score 10.0, rejected []`. P3 entry: `walker-route-r18.md`, `surface: P3`,
   sources_ok S072–S091. P5 entry: `theme-route-r18.md`, `surface: P5`, sources_ok
   `S092 S093 S094 S095`. `u_routes 7`, so U1–U7 are intact.
2. Upstream filter (`measure.py:254-258`, re-applied by hand to the registry at the rev):
   - P5 passes on S092 (`swaybg` in the source cell, kind docs), S093 (`omarchy v3.8.4 theme writers …
     bin/omarchy-theme-set`, kind code) and S094 (`theme`). S095 is not https, so it is not upstream.
   - S077 (walker `src/theme/mod.rs`) is cited only in the P3 note, and its used-by names only
     `walker-route-r18.md`.
   - **So P5 rests on swaybg and the omarchy theme/bg scripts, not on walker theme code.**
3. Receipt join, Python over `git show REV:` of every `.ufo/waves/round-18/fetch/*/receipts.jsonl` (21 files,
   301 lines, every line valid JSON):
   - The credited web rows S072–S089 and S092–S094 carry **31 anchor digests**. All 31 have at least
     one receipt with `http_status 200` and an equal `sha256`: **81 matching receipt lines, 0 non-200**.
   - Each matched body in the working copy re-hashes to its receipt sha256 (81/81).
   - No URL has two different 200 digests across seats.
   - Six digests have exactly one fetching seat: S079 tarball `e50c6060…`, S084 docs.rs `0291cfe6…`,
     S088 `05cd9c67…`, S094 tree `50c1ac25…`, S094 colors `dbdd13a6…`, S094 backgrounds-tree `9e1160a0…`.
4. Anchor-line spot checks against the fetched bodies. Every cited line says what the note claims:
   - P5: OT:17,29-30,38,41-42,45,48-50,53-62,65-70,73; OB:6-9,11,14-17,41,46,49-50; OS:12,21,24-25; OP:6,38,43;
     OA:5; SW:19-31; SM:521-529,575-577,658-663; SB:24-46. The tree HTML lists the 8 payload names and the 4 backgrounds.
   - P3: WR:3,59,167-185,213-215; WM:104-108,124-126,142,149,635-642,670-674,782-786,802-803;
     WS:7-8,212-239,586-594; WD:153-169,653-660; WT:56-63,132-135; WK:3,21; ER:123,129,140-141,177-178,183-194,211;
     EC:38-47; ED:46-47,94-95,177-187,299-305,325; EG:28-48,84-97; XD:302,306,356-358; OL, OR, OF, OD whole files.
   - The tag tarball's `Cargo.lock` has `xdg 3.0.0`, which equals the docs.rs page fetched (`xdg/3.0.0`).
5. Host re-hash with read-only sha256sum/readlink/sed on the log. No drift: `theme.name` `48749715…`; link →
   `…/0-ship-at-sea.jpg` `55fa691a…`; `~/.config/walker/config.toml` `fecf71fa…`; `/etc/xdg/walker/config.toml`
   `3c5c6867…`; `/usr/bin/walker` `25240650…`; omarchy-default `style.css` `481267af…`; `autostart.conf` `acb6a668…`;
   `omarchy-theme-bg-next` `ee482812…`. `pacman.log` lines 1158, 1943, 2929, 3062, 3095, 3123 and 3135-3146 match the notes.
6. `git ls-tree -r --name-only <rev> -- .ufo/waves/round-18/fetch` at **both** 4c103b55… and abfbf35b…:
   21 files, all named `receipts.jsonl`, and **0 body files**.
7. Mutants in `/tmp/c2w2`: commits on top of 4c103b55…, then `measure.py HEAD`:

| mutant | change | result |
|---|---|---|
| M1 | P5 `source:` = `S077; S095` (walker theme code + host), and S077 used-by also names the theme note | **count 6, P5 covered**, sources_ok `[S077, S095]` |
| M2 | P5 `source:` = `S095` only (host row) | count 5, P5 rejected ("no cited mined tier-A row is an upstream https …") — the gate bites |
| M3 | anchor shas of S092/S093/S094 replaced with `0`×64 | **count 6, P5 covered** — receipts are outside c2 |
| M4 | inserted "swaybg is running now (PID 1203358) and re-reads the link on every retarget." before `## Safe observation` | **count 6, P5 covered** |
| M5 | P3 `source:` = `S084; S090` (xdg docs + host log) | **count 6, P3 covered**, sources_ok `[S084, S090]` |

## Findings

### D1 — P5 live-behaviour claim outside `## Unexercised behavior` (fixable)
- Location: `theme-route-r18.md:60`, under `### Default autostart`: "retargeting the link changes the wallpaper
  without editing config."
- This is a present-tense statement about live rendering. The note's own `:137` says the opposite is open:
  "`[UNK]` Whether the running swaybg re-reads the retargeted link".
- Upstream shows that retargeting alone does not do it. Both writers kill and relaunch swaybg after `ln -nsf`:
  - `OB:49` `pkill -x swaybg`
  - `OB:50` `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`
  - `OS:24-25`, the same pair.
- The image is re-opened only when `load_required` is set. Visible at `SM:651-652`: `if (output->config->image && buffer_change) { … load_required = true;`.
- Axes affected: coverage-V honesty (the "documentary route, not observed behaviour" contract) and internal consistency.
- **Honest wording:** "`[OA:5]` names the link, not the image. A swaybg started after the link is retargeted opens the
  new target, and both upstream writers relaunch swaybg for that reason (`[OB:46,49-50]`, `[OS:21,24-25]`).
  Whether an already-running swaybg follows a retarget is `[UNK]` (§ Unexercised behavior)."
- While editing: the `:137` `[UNK]` can cite `SM:651-652`, the buffer-change reload path the note says it did not trace.

### D2 — P3 host-behaviour assertion beyond the code read (fixable)
- Location: `walker-route-r18.md:212`: "no `elephant.toml` is present, so `EG:85-89` applies to the global config."
- That depends on how `ProviderConfig` resolves files. The note's own `:306-308` lists this as `[UNK]` ("the `ProviderConfig` path resolution (the function body was not in the fetched files…)").
- The function was fetched by another seat (`SrcElephantProviders/common-files.go`, v2.22.1 `pkg/common/files.go`):
  - `:28-55` `ConfigDirs()` returns the explicit `--config` dir only, or `~/.config/elephant` plus every
    `$XDG_CONFIG_DIRS/elephant`.
  - `:65-77` `ProviderConfig` returns `ErrConfigNotExists` when no directory has the file.
- On this host `/etc/xdg/elephant` is absent (`ls`). The conclusion is probably right today, but it also depends on two
  things nobody read: the running process's `XDG_CONFIG_DIRS`, and any `--config` set by the user unit.
- **Honest wording:** "no `elephant.toml` is present in `~/.config/elephant` and `/etc/xdg/elephant` is absent. If the
  running elephant has no `--config` and default `XDG_CONFIG_DIRS`, `ProviderConfig` returns `ErrConfigNotExists`
  (`pkg/common/files.go:28-77`, uncited here) and `EG:85-89` applies `[INF]`." Alternatively, move the sentence under
  § Unexercised behavior.

### D3 — Claim wording overstates the committed evidence (fixable, SCORECARD and lesson text)
- SCORECARD "Round 18 — declared claims", C2: "each new credited row backed by a committed raw fetch receipt
  (body bytes, sha256, byte count, fetch time — R17-V3)".
- `round-18.md` M6: "`fetch-verify.py` re-hashes bodies and joins rows."
- Counterexample 1: at 4c103b55… and abfbf35b… the fetch tree is receipts only, with 0 bodies (command 6). In a clean
  checkout of either revision the receipts cannot be re-hashed against bodies. Only a re-fetch or the uncommitted
  working copy can do it.
- Counterexample 2: the host rows S090, S091 and S095 are "new credited rows" (they appear in `sources_ok`), but they
  have no fetch receipt and cannot have one. Digests with no receipt: `/usr/bin/walker` `25240650…`, `theme.name`
  `48749715…` and the background target `55fa691a…`.
- Counterexample 3: M3 shows that c2 credits P5 with every anchor sha zeroed. Receipt backing is a separate check
  that the 6/6 number does not include.
- Axes affected: false provenance at the wording level. The data is sound: 31/31 digests and 81/81 body re-hashes
  pass in the working copy.
- **Honest wording:** "Rubric V 4/6 → 6/6 at 4c103b55… (unchanged `measure.py`). Separately, each anchor digest of
  the credited *web* rows S072–S089 and S092–S094 (31 digests) equals the sha256 of at least one committed `HTTP 200`
  receipt. Receipt bodies are not committed; verification needs the working copy or a re-fetch of the tag-pinned URL.
  Host rows S090, S091 and S095 are file-byte declarations without fetch receipts. `measure.py` does not read receipts."

### D4 — S094 and S084 contradict the round-18 source-admission rule (tradeoff; not load-bearing)
- `round-18.md` says: "Reject or leave unrowed: HTML pages as sole support (per-fetch tokens make the digest
  irreproducible), unversioned docs sites as version-specific support."
- S094's payload-name claims (`[OM]`, theme `:64`) rest only on two GitHub tree HTML pages. Both bodies contain
  `nonce`, `request-id` and `visitor-hmac` tokens, so the `50c1ac25…` and `9e1160a0…` anchors cannot be reproduced.
  The note's recheck line ("compare SHA-256 with the receipts") will fail on a correct re-fetch.
- S084 cites `docs.rs/xdg/latest/…`, which is unversioned. Today it equals walker's locked `xdg 3.0.0`; a new crate
  release will break that silently.
- Credit impact: none. Removing S094 leaves P5 on S092 and S093, and removing S084 leaves P3 on 17 walker/elephant
  rows.
- **Smallest correction:**
  - Keep the raw `colors.toml` digest `dbdd13a6…` as S094's anchor. Mark the tree pages as "digest is per-fetch, names
    only, not re-verifiable by sha", or drop them for a tag-pinned tree listing such as the tarball.
  - Re-anchor S084 to `https://docs.rs/xdg/3.0.0/…`, or the tarball's vendored source.

### Minor (wording)
- `theme-route-r18.md:87`: "which the hook runner skips" is true. `omarchy-hook:25` reads `[[ $hook == *.sample ]] && continue`
  (fetched by `SrcOmarchyThemeHooks`, receipt 200). But the claim is uncited and the file is not in S093. Add `bin/omarchy-hook:25` to S093 or mark it `[INF]`.
- `theme-route-r18.md:76`: "they are not loaded" is a live claim. Honest form: "no import line in the
  loaded files names them (grep) `[INF]`".
- `theme-route-r18.md:119`: the swaybg host-version binding cites `/var/log/pacman.log:1158`, but S095's path list
  does not name `pacman.log`. Add it to S095's source cell.
- Host rows are typed `kind=code, tier A` (S090/S091/S095). That follows the precedent of S059/S060/S071 and is
  excluded from the upstream gate, so it is not load-bearing. A `host` kind would describe them better.

## Instrument gaps (route to round 19; not a defect in the landed credit)
- **M1:** the P5 keyword set (`'theme', 'wallpaper', 'hyprpaper', 'swaybg'`) accepts a walker URL containing `theme`.
  An entry backed only by walker theme code covers P5.
- **M5:** the P3 gate matches keywords in the *scope* cell. The xdg crate docs row covers P3 because its scope says
  "used by walker's find_config_file".
- **M3, M4:** c2 checks neither receipts nor live-claim placement.
- Smallest instrument correction for round 19:
  - Match keywords on the `source` cell only, not `scope`.
  - Narrow P5 to `swaybg | hyprpaper | omarchy-theme | /themes/ | wallpaper` and exclude `abenz1267/walker`.
  - Optionally join a 200 receipt whose sha256 appears in the anchor cell.
  - Under QUALITY 25, each change counts only with a committed pre/post mutant receipt; M1 and M5 above are ready-made mutants.
- Impacted axis: coverage-V instrument strength. The current 6/6 is unaffected; re-running it at 4c103b55… under the tightened rules would still credit both routes (S092/S093 and S072–S083 name their surface in the source cell).

## Tool installs
None.
