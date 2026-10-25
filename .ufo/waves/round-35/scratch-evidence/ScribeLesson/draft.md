## Gate

Round 35 froze `PRED-C1-r35-v1` / `PRED-C2-r35-v1` at
`19e4ab3171c1540c40d6b12097745af98053b07d` before any corpus append; the
predicates were not rewritten after seats scored them. C1's assimilation is
frozen-scope: three knowledge entries and eight registry rows, every document
re-opened on this host during the round with a committed receipt under
`.ufo/waves/round-35/fetch/`. The eight rows were normalised in scratch first —
`status=mined`, a valid `recheck` cadence token, `used-by` exactly the admitted
entries citing them, `anchor` carrying the receipt sha256, no literal or escaped
pipe — and the append block was validated against a scratch mirror before the
real append (`ExecAppendBlock` probe: `closed_entries=3 closed_rows=8
open_cites=0 verdict=TARGET_MET`). The three package `recheck` recipes that
carried `find … \| wc -l` inside a pipe-delimited cell (package S327/S340/S342)
were dropped to their cadence stems, not escaped; the recipe text moves to the
citing entry's gate note.

### Candidates considered

- 3 staged knowledge entries (`idle-lock-never-asked-r12`, `idle-lock-chain-armed-r14`,
  `idle-lock-offered-in-the-bar-r15`) and their 8 cited documents, from the
  merge package `merge/mado/` — this round's frozen C1 data.
- The mado slice of the campaign absent-defect register
  (`shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`):
  13 rows, dispositioned row-by-row below (12 refused, 1 in-registry).
- The merge package's 147 staged rows (`merge/mado/SOURCES.append.md`,
  sha256 `684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0`,
  read 2026-10-24): 8 adopted by document, 139 not adopted this round.
- `considerthese/2026-10-24.md` proposals 1–6: the file's own marking is
  "proposals only; not acted on"; none is a source candidate and none was
  mined this round. The directory was read, never edited.

### Admitted — three entries

| entry | cites | opened |
|---|---|---|
| `corpus/knowledge/idle-lock-never-asked-r12.md` | S203, S204 | 2026-10-24 |
| `corpus/knowledge/idle-lock-chain-armed-r14.md` | S205 | 2026-10-24 |
| `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | S206, S207, S208, S209, S210 | 2026-10-24 |

### Admitted — eight rows (S203–S210, lane ids)

All eight are `own-work`, tier A, `status=mined`, opened 2026-10-24, re-grounded
this round against the live host (no package text was copied; the receipts under
`.ufo/waves/round-35/fetch/` are this round's own re-opens). The located quote
is the verbatim remainder of the entry's `gate-quote:` line — confirmed a
contiguous substring of the committed receipt bytes, 13–17 words each, by
`ExecQuoteLint` (8/8 PASS) against the frozen spec.

- `S203` — host file `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run`
  (1089 B, file sha256 `20508471d8237a60e630baf58f87c0b5a4391e34196ce11e5034745f6a062630`;
  receipt `fetch/S203.receipt.txt` sha256 `1b7fa87f…dd1646`), accessed 2026-10-24,
  `used-by`: `idle-lock-never-asked-r12.md`.
  Located quote: `located: install/first-run/ lists 12 scripts; the omarchy-first-run body runs all 12; none is idle-lock`
- `S204` — measured receipt `.ufo/waves/round-35/fetch/S204.receipt.txt`
  (command `journalctl --user --no-pager | grep -c 'omarchy-toggle'` → `0`;
  receipt sha256 `4cd5ba65…d1c54ad`), accessed 2026-10-24,
  `used-by`: `idle-lock-never-asked-r12.md`.
  Located quote: `located: journalctl --user shows 0 omarchy-toggle invocations; the installer runs 12 first-run scripts`
- `S205` — measured receipt `.ufo/waves/round-35/fetch/S205.receipt.txt`
  (hypridle.conf sha256 `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41`;
  receipt sha256 `f3387bfc…08ae1a`), accessed 2026-10-24,
  `used-by`: `idle-lock-chain-armed-r14.md`.
  Located quote: `located: hypridle runs as pid 1667 and started in this session; hypridle.conf sets timeout 150 and 152`
- `S206` — host file `/home/vgpnk/.config/waybar/config.jsonc`
  (6354 B, file sha256 `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829`;
  receipt `fetch/S206.receipt.txt` sha256 `1d30e4a9…a938d5`), accessed 2026-10-24,
  `used-by`: `idle-lock-offered-in-the-bar-r15.md`.
  Located quote: `located: waybar config.jsonc line 207 opens the custom/idle-indicator module; line 208 runs omarchy-toggle-idle`
- `S207` — host file `/home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh`
  (159 B, file sha256 `6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750`;
  receipt `fetch/S207.receipt.txt` sha256 `81c33e79…0adec59`), accessed 2026-10-24,
  `used-by`: `idle-lock-offered-in-the-bar-r15.md`.
  Located quote: `located: idle.sh pgreps hypridle and prints the tooltip Idle lock disabled when it is absent`
- `S208` — host file `/home/vgpnk/.local/share/omarchy/bin/omarchy-menu`
  (33017 B, file sha256 `d196b086e961d524945a899c5eb6e1aa532d9594c924d78b78c1fff183a0f79d`;
  receipt `fetch/S208.receipt.txt` sha256 `6e72f0db…6ce4654`), accessed 2026-10-24,
  `used-by`: `idle-lock-offered-in-the-bar-r15.md`.
  Located quote: `located: omarchy-menu line 207 lists Idle Lock among the toggles; line 212 dispatches omarchy-toggle-idle`
- `S209` — measured receipt `.ufo/waves/round-35/fetch/S209.receipt.txt`
  (the dated `config.jsonc.bak*` copies under `~/.config/waybar/`;
  receipt sha256 `a170c7a5…3bdd27c`), accessed 2026-10-24,
  `used-by`: `idle-lock-offered-in-the-bar-r15.md`.
  Located quote: `located: four dated copies of the bar's configuration each carry the omarchy-toggle-idle handler`
- `S210` — host directory `/home/vgpnk/.local/state/omarchy/toggles/hypr`
  as captured in `.ufo/waves/round-35/fetch/S210.receipt.txt`
  (receipt sha256 `ef282e38…b8726`), accessed 2026-10-24,
  `used-by`: `idle-lock-offered-in-the-bar-r15.md`.
  Located quote: `located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock`

The registry continues S202 → S203 contiguously. S190–S195 and S197–S200 were
never allocated and stay so: contractually free, but `CritIdSpace` records them
permanently skipped rather than backfilled — backfilling would collide with the
pre-renumber package numbering and break id⇄time order.

### Refused — the register slice (twelve of thirteen)

The register's id column is the campaign's pre-remap staging id space, not this
lane's registry ids; each row below names the register id, the document it
cites, and the id that document currently carries in `SOURCES.append.md` so the
campaign can reconcile (`lanes/mado/ID-REMAP.md` is the map, and the file was
renumbered mid-wave — the ids below are the observed 2026-10-24 values, not the
frozen registration's). Twelve of the thirteen mado rows are refused; no locator
of the refused rows was fetched this round and none is needed to refuse them.

- `S195` (register, r2; staged as `S212`) — SJTU `arch-wiki-docs-zh-cn`
  package, class `payload-absent`. Documentation localization is outside
  `PROVINCE.md`, the same rule that refused `two-literature-drift-r26.md` in
  round 33. Flip: a desktop/compositor surface cited only from tier A or B,
  opened by this lane.
- `S201` (register, r2; the arXiv document now carried thrice, as `S218`,
  `S280`, `S325`) — `https://arxiv.org/abs/2604.18860`, class `payload-absent`.
  The register's "S201" is a different document from the lane's S201 and the
  arXiv URL is absent from the lane registry; no renumber is warranted — restated
  from round 34. Flip: fetched bytes under a fresh id plus an in-province
  desktop/compositor claim — never under the lane's S201.
- `S205` (register, r3; staged as `S222`) — ArchWiki `interwikimap` siteinfo
  JSON, class `payload-absent`. Localization metadata for the wiki
  translations, not a desktop/compositor surface — outside `PROVINCE.md`.
  Flip: a desktop/compositor surface cited only from tier A or B, opened by
  this lane.
- `S224` (register, r4; staged as `S241`) — `/home/vgpnk/.cache/ai-usage/status.json`,
  class `payload-absent`. A transient host cache file, not a source; its
  `updated_at` quote is stale on every read. Flip: reclassify as own-work
  probe output under `.ufo/evidence/`, or a durable published artifact.
- `S228` (register, r5; staged as `S245`) —
  `lanes/mado/round5/fetch/cn-export-hyprland.html`, class `payload-absent`.
  Chinese-article revision metadata — documentation localization, outside
  `PROVINCE.md`. Flip: a desktop/compositor surface cited only from tier A or B,
  opened by this lane.
- `S199` (register, r2; staged as `S216`) — `https://blog.csdn.net/2301_76324845/article/details/149787804`,
  never checked: `unreachable` is not fabrication. The staged row now reaches
  the body through a declared reader proxy, but the locator is tier C
  community and this lane did not open it. Flip: a desktop/compositor surface
  cited only from tier A or B, opened by this lane.
- `S200` (register, r2; staged as `S217`) — `https://blog.csdn.net/lxyoucan/article/details/164457293`,
  never checked. Same class and same grounds as register S199. Flip: a
  desktop/compositor surface cited only from tier A or B, opened by this lane.
- `S209` (register, r3; staging id does not resolve in the package), `S222`,
  `S223`, `S225` (register, r4), `S235` (register, r5) — the register cites only
  a `## Gate — Snnn` prose anchor; no locator was ever named, so each row is
  unverifiable, not fabricated. The register's own reason column says the gate
  block named no locator. Flip: a resolvable URL or path naming the row's
  claimed bytes, opened by this lane.

The thirteenth register row, `S189` (r1), is **not** refused: the round-34
quarantine hand-check found its quoted span — the `formatEvent` `eventString`
assignment — at line 128 of the pinned `EventManager.cpp`, a `payload-absent`
false negative, and the lane already holds that exact document at its own S189
(IN-REGISTRY-SAME-ID). It was adopted in round 32 and is not re-appended.

### Refused — merge-package rows not adopted this round

`SOURCES.append.md` stages 147 rows (S203–S349, contiguous). This round adopts
eight *documents*, not eight package rows: the adopted ids below are the file's
values at read time (sha256 above, mtime 2026-10-24 23:30) after the campaign's
mid-wave renumber; the frozen registration's recorded set {S309, S310, S321,
S329, S330, S331, S334, S336} is the pre-remap id space, already routed
campaign-side as L0 `ae2c52b8`. The package's own `source:` headers inside its
three knowledge files still carry the pre-remap ids — the map for reconciliation:

| lane id | package id (current) | document | package `source:` id (stale) |
|---|---|---|---|
| S203 | S315 | `lanes/mado/round12/fetch/host-omarchy-first-run.txt` / `omarchy-first-run` | S309 |
| S204 | S316 | `lanes/mado/round12/fetch/host-idle-lock-never-asked.txt` | S310 |
| S205 | S327 | `lanes/mado/round14/fetch/host-idle-lock-chain-state.txt` | S321 |
| S206 | S335 | `/home/vgpnk/.config/waybar/config.jsonc` | S329 |
| S207 | S336 | `~/.local/share/omarchy/default/waybar/indicators/idle.sh` | S330 |
| S208 | S337 | `~/.local/share/omarchy/bin/omarchy-menu` | S331 |
| S209 | S340 | `lanes/mado/round15/fetch/host-waybar-dated-backups-sweep.txt` | S334 |
| S210 | S342 | `lanes/mado/round15/fetch/host-omarchy-toggles-state-sweep.txt` | S336 |

Note the trap the renumber left: stale `S336` (toggle-state sweep) and current
`S336` (indicator script) name different documents — a literal id read
mis-resolves all eight. The 139 rows this round does not adopt:

- **Staged copies of register-refused documents — refused on the same grounds
  as their register rows** (6 rows, 4 documents):
  - `S212` (SJTU zh-cn offline wiki package) — localization, outside
    `PROVINCE.md`. Flip: a desktop/compositor surface cited only from tier A or
    B, opened by this lane.
  - `S218`, `S280`, `S325` (three staged rows for the one arXiv paper) —
    refused with register `S201`; the package also duplicates this document
    three times, which the campaign must deduplicate. Flip: fetched bytes under
    a fresh id plus an in-province desktop/compositor claim — never under the
    lane's S201.
  - `S222` (ArchWiki `interwikimap` JSON) — localization metadata, outside
    `PROVINCE.md`. Flip: a desktop/compositor surface cited only from tier A or
    B, opened by this lane.
  - `S241` (`~/.cache/ai-usage/status.json`) — transient host cache, quote
    stale on every read. Flip: reclassify as own-work probe output under
    `.ufo/evidence/`, or a durable published artifact.
- **`S220` (hypridle v0.1.8 `ConfigManager.cpp`) — held, not admitted.**
  The campaign itself forced its `status` to `queued`: its `used-by` names
  `corpus/knowledge/idle-lock-runtime-state-r28.md`, a staged entry the merge
  report marks "target already exists — append, do not replace," and no staged
  entry text cites it. A `queued` row is not an admitted row. Reason: the
  citation the row claims does not exist in the package. Flip: land the r28
  amendment so a citing entry exists, then re-open the document in-round; or
  drop the pointer, per the merge report's own rule.
- **The remaining 132 rows — `S203`–`S211`, `S213`–`S217`, `S219`, `S221`,
  `S223`–`S240`, and `S242`–`S349` except the adopted `S315`, `S316`, `S327`,
  `S335`, `S336`, `S337`, `S340`, `S342` and the refused `S280`, `S325` — out
  of scope, not adopted.** This round's
  frozen predicate covers exactly the three idle-lock entries and their eight
  documents; nothing else in the package was claimed, re-opened or measured by
  this round, so no other row is admitted on this round's authority. This is a
  scope refusal, not a defect verdict. Package-wide flip: a future round
  re-opens the document in-round (or verifies the staged fetch artifact under
  `shokuknow/lanes/mado/roundN/fetch/`), normalises the row — cadence-token
  `recheck` only, no pipe literal or escape, `status=mined` with a `used-by`
  that names a landed entry, `anchor` carrying that receipt's sha256 — and
  resolves the id collision: package `S203`–`S210` now numerically collide with
  this round's own lane ids (different documents), so adoption under new lane
  ids needs a recorded remap, or the campaign renumbers its slice, before any
  append. Eight staged rows additionally duplicate documents the lane already
  holds — `S203`→S186, `S204`→S187, `S205`→S188, `S206`→S189, `S213`→S196,
  `S276`→S187 (a second staged copy of the 0.56.0 IPC page), `S207`→S201 and
  `S208`→S202; their flip is the duplicate-URL rule — a materially new aspect,
  stated per the merge report's own caveat.

### What this round does not pretend

The register's `payload-absent` rows are refused on province and
verifiability grounds, not re-litigated as fabrications: the lane did not
re-fetch a single register locator, and the refusal reasons do not require one
(round-34's hand-check is the authority for the S189 exception). The campaign's
id-space churn — proposal ids, pre-remap staging ids, append ids — is recorded
for reconciliation here and at L0 `ae2c52b8`; this lane keeps one space only:
its own registry, ending at S210 after this append.
