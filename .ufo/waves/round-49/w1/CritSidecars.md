# CritSidecars — report (round-49 w1, routed item: the 47 untracked `*.synthetic` sidecars)

**Verdict: COMMIT all 47.** Full evidence: `.ufo/waves/round-49/w1/CritSidecars/findings.md` + `receipts/` (5 files).

Lane tip examined `5f37c1b8` (round-49 claims commit; item routed against base `03e4ae76`). The marker install from
round-48 w1 `ExecSessionMarker` is 2/3 landed: tracked `quality/check-session-material.py` sha `82c9053a…` (the
delivered v2) and tracked `quality/session-material-waivers.txt` sha `4d007fe8…` (the delivered 48-row registry). The
47 untracked files are the missing third.

Measured on a `--shared` scratch clone (toplevel asserted, scratch identity, scratch HOME/XDG_*, no compositor, no
`--serial-from-host`):

- 47/47 live sidecars are byte-identical to the archived copies digested in
  `.ufo/waves/round-48/w1/ExecSessionMarker/SHA256SUMS`; 47/47 `sha256=` fields equal the current target blobs; 47/47
  registry rows agree on sha/rules/kind (`receipts/sidecar-digest-verification.txt`).
- Gate at tip: `findings=159` (waived 3/1 — the gate-copy row already live). Tip + sidecars committed:
  `findings=110`, `WAIVED findings=52 files=48` — the exact set ExecSessionMarker predicted. `--no-waivers` at both
  revs = `findings=162`: the −49 delta is purely the marker layer; `.synthetic` blobs produce zero findings.
- No real material waived: every waived value is inside a reserved namespace; the two CritW2Gate files keep their real
  R1 title findings (`rule-not-listed`, printed). Forged-marker attacks on a scratch commit all fail closed:
  `value-not-synthetic:serial-not-synthetic` / `program-not-synthetic`, `serial-rule-not-waivable`,
  `path-outside-waves` (`receipts/gate-forged.txt`). Stale markers fail closed too (`sha-mismatch` → finding returns).
- Removing instead would leave the 47 `fixture` registry rows dead, keep 49 synthetic findings red forever, and keep
  N1's dirty-worktree state. `.synthetic` is not gitignored; only the gate consumes the suffix, and it reads committed
  blobs — sidecars must be tracked to function.

Waiver rows activated: `quality/session-material-waivers.txt` lines 2–48 (the `fixture` rows); line 49 (`gate-copy`)
already active.

L1 note (not a blocker): tracked duplicate copies of these sidecars exist under
`.ufo/waves/round-4{7,8}/…/{demo,sidecars}/` — inert (their mark-targets don't exist there) but duplicative.

No installs, no pacman, no compositor reads, no host state writes, no mutating git in the lane or fleet; scratch
`/fast/scratch/hyaku/mado-r49/CritSidecars/` deleted after receipts were copied into the seat dir.

Report: .ufo/waves/round-49/w1/CritSidecars.md
