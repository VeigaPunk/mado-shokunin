# CritSidecars — the 47 untracked `*.synthetic` sidecars: commit or remove?

Seat: `CritSidecars` (leaf, critic lane; no subagents). Lane tip examined: `5f37c1b87b3ce5e438d19284e32b2e46fd548a92`
(round-49 claims commit; the routed item lives at base `03e4ae76`). Scratch: `/fast/scratch/hyaku/mado-r49/CritSidecars/`
(one `--shared` clone, three scratch commits, deleted after receipts were copied here).

**Recommendation: COMMIT all 47.** They are byte-identical to the audited install set delivered by round-48 w1
`ExecSessionMarker`; the tracked tree already contains the other two halves of the marker contract (gate v2 and the
48-row registry), so the untracked files are the missing third of an install the L1 already half-landed. Leaving them
untracked keeps 49 synthetic findings red forever and keeps the worktree dirty (N1).

## 1. What the 47 are

- `git status --porcelain -uall` → 47 untracked `*.synthetic` (45 under
  `.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/{w,w2,w3,w4}/`, 2 under `.ufo/waves/round-46/w1/`), nothing else
  inherited-untracked — reproduces N1's count and command.
- Each is a one-line marker, e.g. `SYNTHETIC-MATERIAL v1 kind=fixture rules=R3_MONITOR_IDENT sha256=<64hex>`
  (`gate grammar`: `quality/check-session-material.py:191-195`, `MARKER_RE`).
- Provenance: round-48 w1 `ExecSessionMarker` generated them (its `mark.py`/`triage.py`) for the 48-row install set of
  `quality/session-material-waivers.txt`; archived copies sit under
  `.ufo/waves/round-48/w1/ExecSessionMarker/sidecars/` and are digested in `SHA256SUMS` lines 23-70. The seat wrote them
  into round-45/46 dirs **outside its own seat dir** — the round-48 incident — but the bytes are the deliverable, not
  litter.

## 2. Digest verification (receipt: `receipts/sidecar-digest-verification.txt`, 47/47 OK)

For every live sidecar, computed not assumed:

- live file sha256 == archived copy sha256 under `ExecSessionMarker/sidecars/` (47/47 identical; archive digests match
  `SHA256SUMS` lines 23-69);
- sidecar first line matches `MARKER_RE` exactly (47/47);
- sidecar `sha256=` field == sha256 of the **current** target blob in the working tree (47/47; targets are all tracked
  and clean);
- `quality/session-material-waivers.txt` (tracked, `4d007fe8…`) row for the target repeats the same sha, rules, kind
  (47/47; the 48th row is the `gate-copy` row for `ExecSessionMarker/check-session-material.py`, whose sidecar is
  **already tracked** and already waiving at tip — `receipts/gate-tip.txt`: `SESSION_MATERIAL_WAIVED: findings=3 files=1`).

## 3. What the gate does with them committed (scratch mirror, receipts 3-6)

Clone `--shared` of the lane at `5f37c1b8`, asserted `rev-parse --show-toplevel` == clone dir, scratch identity:

| state | rev | result | receipt |
|---|---|---|---|
| tip, sidecars absent | `5f37c1b8` | `files=22019 findings=159`, waived 3 (gate-copy), rc 1 | `receipts/gate-tip.txt` |
| + 47 sidecars committed | `15510cb8` | `files=22066 findings=110`, `SESSION_MATERIAL_WAIVED: findings=52 files=48`, rc 1 | `receipts/gate-with.txt` |
| same rev, `--no-waivers` | `15510cb8` | `findings=162` — identical to `--no-waivers` at `5f37c1b8` (`findings=162`) | `receipts/gate-with-nowaive.txt` |

So the marker layer removes exactly 49 findings (45×`R3_MONITOR_IDENT` on the round-45 monitor fixtures + 2×`R2_PROC_TABLE`
and 2×`R3_MONITOR_IDENT` on the round-46 CritW2Gate pair). Delta is purely the marker: `.synthetic` blobs themselves
produce zero findings (0 hits in the `--no-waivers` run). The gate stays red (`findings=110`, rc 1) — the sidecars do
**not** launder the gate green.

Two loud rejections appear, both correct: `WAIVER_REJECTED …CritW2Gate.{md,report.md} rule=R1_CLIENT_DUMP
reason=rule-not-listed` — the pair's client titles are the `Example…` family the F1 tightening excludes, so their real
R1 findings stay counted (`gate-with.txt`). This is the marker working as designed, not a defect.

## 4. Would committing waive REAL material? (attack surface)

Waiver needs all of: path under `.ufo/waves/`; sidecar sha == target blob sha; registry row repeats path/sha/rules/kind;
`gate-copy` ⇒ target byte-identical to `quality/check-session-material.py`; `fixture` ⇒ **every** matched value in a
reserved namespace (`check-session-material.py:609-690`); serial rules R5/R6 can never be waived (`:633-636`).

Measured, scratch clone, commit `1e5de3d0` (receipt `receipts/gate-forged.txt`):

- forged marker+registry row on a **real-shaped** monitor dump (`Dell Inc.` serial `84WXK23A9B1`) under
  `.ufo/waves/round-49/w1/` → `value-not-synthetic:serial-not-synthetic`, FINDING stands;
- forged marker on a real process row (`firefox pid=44210`) → `value-not-synthetic:program-not-synthetic`, FINDING stands;
- synthetic monitor dump **outside** `.ufo/waves/` (`.ufo/reports/`) → `path-outside-waves`, FINDING stands;
- serial-shaped prose under a well-formed R1 marker → `serial-rule-not-waivable`, FINDING stands.

The 47 waived targets themselves hold only reserved-namespace values (spot: `C00_shipped/mons.json` = `Fake Corp` /
`0x0000` / `SN00000`; the W4b pass on every waived file is what makes the WAIVER line print at all — `gate-with.txt`
has 52 WAIVER lines, 0 unexpected). No real value is waived by committing them; the residual class ("real value inside
a reserved namespace, e.g. a genuinely redacted dump") is inherent to the already-installed marker layer, review-visible
(one `WAIVER` line printed per waived file:rule), and identical whether or not these 47 are committed.

Staleness fails closed too: if any of the 47 target blobs is edited later, the marker's sha stops matching and the
waiver flips to `WAIVER_REJECTED sha-mismatch` (finding returns; visible, never silent).

## 5. Commit vs remove

COMMIT, because:

- The install is 2/3 landed already: tracked `quality/check-session-material.py` == delivered v2 `82c9053a…` (SHA256SUMS:1)
  and tracked `quality/session-material-waivers.txt` == delivered 48-row registry `4d007fe8…` (SHA256SUMS:22). Without
  the sidecars the 47 `fixture` registry rows are dead text; with them the measured delta is −49 false-positive
  findings and zero new waivers beyond the audited set (§3 reproduces ExecSessionMarker's predicted
  `WAIVED findings=52 files=48` exactly, `ExecSessionMarker.md` §3.7).
- Removing them fixes nothing: the registry is already committed, so the fixtures keep generating 49 findings with no
  path to waiver (gate stays red on synthetic noise), and the fleet "clean worktree" check keeps reporting 47 untracked
  files (N1). Removal would only be coherent as part of ripping out the whole marker layer — a larger decision than
  this item.
- `.synthetic` is not gitignored (`git check-ignore` rc 1) and nothing but the gate consumes the suffix; the gate reads
  blobs from the scanned revision only, so untracked sidecars are invisible to it — they must be **tracked** to function.

Waiver rows activated: the 47 `fixture` rows of `quality/session-material-waivers.txt` (lines 2-48); the `gate-copy`
row (line 49) is already live at tip.

One hygiene note for the L1, not a blocker: the round-47/48 demo and archive copies of these same sidecars are already
tracked under `.ufo/waves/round-4{7,8}/` — harmless (they mark paths that don't exist there) but duplicative evidence.

## 6. Evidence index (all in `receipts/`)

- `sidecar-digest-verification.txt` — 47/47 live==archive, marked==target sha, registry match.
- `gate-tip.txt` — `5f37c1b8`, findings=159, waived=3/1.
- `gate-with.txt` — `15510cb8` (tip + 47 sidecars), findings=110, waived=52/48, 2 `rule-not-listed` rejections.
- `gate-with-nowaive.txt` — same rev, findings=162 (== `--no-waivers` at tip).
- `gate-forged.txt` — `1e5de3d0`, all four forged-marker attacks rejected, findings stand.

Commands (repro): `git status --porcelain -uall | grep -c synthetic` → 47;
`python3 -I quality/check-session-material.py --repo <clone> --rev <rev>` (no `--serial-from-host`: zero compositor
access — the host serial probe is opt-in and was not used). No installs, no pacman, no compositor calls, no host state
touched; scratch HOME/XDG_* throughout; scratch dir deleted after receipts were copied.
