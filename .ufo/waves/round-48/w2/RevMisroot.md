# RevMisroot — round 48 w2 · independent signoff on the attributed misroot note

Verdict: **signed off with one attribution caveat.** Every checkable claim in the note reproduces exactly:
the quarantined `tree.json` is 347495 B, sha256 `fdb0b7a49736a50b956ef899b64a4381547a0b37a4663a3eae46f731257e16d3`,
its `SHA256SUMS` verifies (`tree.json: OK`), the quarantine dir is fleet-git-ignored, and **no copy of those
bytes exists anywhere at the fleet root outside the quarantine batch** (931,904 files stat-scanned). The note's
writer attribution remains an orchestrator inference — no seat report admits writing it (four deny; the
pointed-at seat is silent) — which the note itself hedges. No move/delete performed by this seat.

Paths below are absolute under the fleet root `F = /home/vgpnk/Projects/shokunin`.
Receipts: `F/mado-shokunin/.ufo/waves/round-48/w2/RevMisroot/check1-quarantine-hash.txt`,
`F/mado-shokunin/.ufo/waves/round-48/w2/RevMisroot/check2-fleet-byte-scan.txt`.

## 1. The note under signoff

`F/.scratch/goal-20261026-hyaku-run9.md:221-225` (orchestrator run state, 20:44 -03 entry): `tree.json`
(347495 B, "a GitHub API tree dump of hyprwm/Hyprland `efb50993`") appeared at the fleet root; "the Hyprland
keymap scouting shape attributes it to a mado r48 w1 seat with cwd = fleet root"; moved bytes unchanged to the
ignored `F/.tower/quarantine/fleet-root-strays-20261026T2055/` (sha256 in `SHA256SUMS` there); MadoR48 told;
"a conformance item for mado r48's closure". Claims decomposed: (a) size 347495 and content = the named trees
dump; (b) quarantine + SHA256SUMS, bytes unchanged, dir ignored; (c) writer attribution; (d) fleet root
otherwise clean of these bytes.

## 2. Quarantine and SHA256SUMS — verified (observed)

- Dir holds exactly two files: `tree.json` 347495 B, mode 644, mtime `2026-10-26 20:44:14.650624751 -0300`;
  `SHA256SUMS` 76 B, mtime `20:48:20.574019361 -0300`.
- `cat -A SHA256SUMS` → `fdb0b7a49736a50b956ef899b64a4381547a0b37a4663a3eae46f731257e16d3  tree.json$`
  (single entry, two-space format, newline-terminated).
- `sha256sum -c SHA256SUMS` (run in the quarantine dir) → **`tree.json: OK`**; independent recompute gives the
  same hash; `stat -c %s` = 347495 = the size named in the notice.
- Content head: `"sha": "efb50993780079460b0cbed1363e2166a2de1d9f"` — the file is the trees-API dump the note
  names. mtime 20:44:14 predates SHA256SUMS 20:48:20 and matches the notice's 20:44 appearance, consistent
  with a preserved-mtime move; and since the bytes are identical to a pre-existing committed lane pin (§3),
  "bytes unchanged" holds regardless of the move mechanics.
- "Ignored": `F/.gitignore` rule `.tower/` ("tower orchestration comms/quarantine: local tool state, not
  fleet history"). `git -C F status --porcelain` → empty in my run.

## 3. Bytes not at fleet root — exhaustive checks (observed)

- Saturation: `find F -xdev -type f` stat-scanned **931,904 files**. Exactly two files of size 347495 B exist
  in the whole fleet tree, both sha256 `fdb0b7a4…16d3`:
  1. `F/.tower/quarantine/fleet-root-strays-20261026T2055/tree.json` (the quarantined stray itself), and
  2. `F/mado-shokunin/.ufo/waves/round-44/w1/ExecFsSemantics/pins/tree.json` — a legitimate **lane-committed
     round-44 pin**, not a fleet-root file: `git -C F/mado-shokunin ls-tree HEAD` → blob
     `177879a6797254e64ee7bcd83c8b14543ef0392b` at that path; last commit touching it
     `290cddea92a18e2202456db89cb2bb60d9aaacff` (2026-10-26T14:36:49-03:00); the pin's own manifest
     `pins/SHA256SUMS.txt:28` carries the same `fdb0b7a4…` hash.
- Name scan for `tree.json` outside `.tower` (maxdepth 6): only
  `F/audio-shokunin/corpus/live/r94-scout/sources/tree.json` — 156,257 B, sha256
  `cef126c4a8ac1e623dc0930f9013f33eb4a5e3be31a18bb7a6f82d9912a6f26e` ≠ stray. Not a copy.
- Substring sentinels (rule out embedded/appended partial copies that an equal-size scan would miss): the
  distinctive upstream line `"sha": "c6bf34ed9159899f55567bb5056f402f820733f1"` from inside the dump occurs in
  only three files under `F`: the quarantine copy, the r44 pin (same bytes), and
  `F/mado-shokunin/.ufo/waves/round-47/w1/ScrErrataR45/pins/hyprland-config-tree.json` (9,725 B, sha256
  `030874aee3d1073641a8d0af6052fdc390c57dd39f170ec17fe82c05cb86d3a5` — a different, smaller committed trees
  dump sharing upstream SHA-1 metadata; not the stray's bytes).
- The stray's hash as text appears only in: quarantine `SHA256SUMS`, r44 `pins/SHA256SUMS.txt:28`,
  `w2/ScoutMisroot.md`, and this seat's two receipts.
- No mado wave artifact at the fleet root: `F/.ufo/waves/` contains no round-48 dir; the only `*round-48*`
  paths outside lanes are `F/.ufo/reports/round-48`, `F/.ufo/prompts/*-round-48.md` and other lanes' own
  report dirs. No `tree.json` exists anywhere under `F/mado-shokunin/.ufo/waves/round-48/`.
- `git -C F status --porcelain` → empty (no untracked or modified file at the fleet root at signoff time).

Conclusion: the stray's bytes exist under the fleet-root tree **only** inside the ignored quarantine batch.
The `SHA256SUMS`, the seat reports and the lane wave artifacts contribute no copy at fleet root.

## 4. Seat-report admits (observed)

No round-48 seat report admits writing the fleet-root `tree.json`; the note's attribution is an inference,
not an admission.

- Denials with scratch-only evidence: `w1/ExecXkbLive.md:251-256` ("the stray `tree.json` … was not this
  seat", three absolute paths, fleet-root find clean); `w1/ExecXkbSource.md:111-113`;
  `w1/CritPremiseC2.md:23-24`; `w1/ScoutXkbSpecs.md:93` (admits a same-kind trees-API dump existed **inside
  its scratch**, removed with the scratch — unverifiable now, no hash recorded); matching `safety` fields in
  `w1-results.json` (ExecXkbSource, ScoutXkbSpecs).
- Silent: `w1/ScoutHyprKeymap.md` — the seat the note's "shape" points at — contains no `tree.json`, `fleet`,
  `cwd` or `api.github` mention; its report mtime 20:46:48 is ~2 min after the stray's 20:44:14.
- Conformance handling is landed, not silent: `receipts/m48-revived-r47-seat-edit.diff:14-17` adds "never
  `tree.json` and never in the fleet root" to the revived seat text.
- Other lanes' fleet reports at `F/.ufo/reports/round-48/` ({chousa,kama,kotoba,kumitate,mori,tameshi}.md)
  each record clean or unrelated misroot sweeps; none claims the `tree.json`. No mado.md there yet at signoff
  time (the note says MadoR48 was told; its fleet report is the closure vehicle).

## 5. Findings

- **F1 — signoff (verified):** all checkable note claims hold. Quarantine hash OK, bytes-unchanged
  consistent, dir ignored, no copy of the bytes at fleet root, no lane wave artifact at fleet root, and no
  frozen instrument touched: the lane round-48 tree contains no `tree.json` at all, so no C1/C2 predicate,
  fixture or counter depends on the stray (supports the note's "conformance item only" framing).
- **F2 — attribution caveat (MEDIUM for closure wording):** "attributes it to a mado r48 w1 seat" is not
  corroborated by any seat byte and cannot be: the bytes are byte-identical to a pin committed at round 44,
  so any fetcher of the same URL or copier of the pin produces them. Recommended closure wording: "writer
  unattributed; bytes identical to committed r44 pin `pins/tree.json` — no new data leaked". Matches the
  independent `w2/ScoutMisroot.md` conclusion.
- **F3 — INFO:** the stray carried no new data (same bytes already in the lane since round 44); the incident
  is a cwd/discipline defect with no data-integrity or predicate impact.

## Residual risk / verification gaps

- `git status` and the size scan prove absence only at the run instant (~22:4x -03); a stray created and
  removed in between would not show.
- ScoutXkbSpecs' scratch trees dump was deleted without a recorded hash, so writer identification from bytes
  is permanently impossible; attribution can only ever rest on timeline + shape.
- `-xdev` bounds the saturation scan to the fleet root's filesystem; other mounts are out of scope (all lanes
  live on the same fs; nothing indicated otherwise).

## Bounds / safety record

Writer shells started with `ulimit -f 2048`; largest output file this seat:
`w2/RevMisroot/check2-fleet-byte-scan.txt` (2,351 B). Scratch `/fast/scratch/hyaku/mado-r48/RevMisroot/`
created per call, trap-removed on every call, verified gone after the last. No fleet-root or lane file moved,
deleted or edited; git used read-only (`status --porcelain`, `ls-tree`, `log -1`); no pacman transaction, no
install, no subagent dispatch (leaf bound).
