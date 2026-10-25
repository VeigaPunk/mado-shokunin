# RevAxisTranscriptAsk — `tip_axis_transcript` conforming-transcript recipe

Seat: reviewer, mado round 36 wave 1. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Verdict: **PASS** on all three asks (rule read, command produced, instrument run at `master`). One finding: **F1 (minor)**.

## 1. The `tip_axis_transcript` rule (C2 gate)

`quality/check-evidence-pointers.py:174-190` is the whole implementation. A committed blob passes when **all** of these hold:

- Path is `quality/receipts/axis-<HEX>.txt` inside the rev's tree (collected from `git ls-tree -r --name-only <rev>`, `:124` — committed files only; a worktree-only receipt scores nothing).
- `<HEX>` matches `^[0-9a-f]{40}$` (`HEX40`, `:48`) — lowercase 40-hex only.
- `git merge-base --is-ancestor <HEX> <branch>` exits 0 (`:180-182`), where `--branch` defaults to `master` (`:119`). Ancestor of the **branch**, not of `--rev`.
- Some line of the blob satisfies `line.startswith("MADO_AXIS:") and "mismatched=0" in line and f"rev={candidate}" in line` (`:185`), where `candidate` is the **filename's** hash — the rev printed inside the file must equal the filename's `<HEX>`.

Docstring restates it at `:25-27`; `registration.md:106` freezes the same wording.

## 2. The `MADO_AXIS:` line format

`quality/check-axis-scores.py:290` prints exactly:

```
MADO_AXIS: checked=3 mismatched=<N> rev=<40-hex>
```

`checked` is `len(AXES)` = 3 (navigation, calibration, operability, `:32`); `rev` is the `rev-parse --verify "<input>^{commit}"` resolution (`:269-273`), so any revspec (`master`, short sha, tag) is canonicalized to lowercase 40-hex — the filename can be taken verbatim from the emitted `rev=` field. `MADO_AXIS_ROW:`/ `MADO_AXIS_NOTE:` lines (`:286-289`) are ignored by the gate. The minimal contract the gate matches is the substring trio on a `MADO_AXIS:`-prefixed line: `mismatched=0` and `rev=<40hex>`.

## 3. Exact command that yields a conforming transcript

For a named 40-hex `<REV>` that is an ancestor of `master` and at which the instrument derives `mismatched=0`:

```sh
REV=<REV>   # full lowercase 40-hex
cd /home/vgpnk/Projects/shokunin/mado-shokunin \
  && python3 -I quality/check-axis-scores.py --rev "$REV" > "quality/receipts/axis-$REV.txt" \
  && git add "quality/receipts/axis-$REV.txt" \
  && git commit -m "axis transcript for $REV"
```

The commit step is **required**: the gate enumerates committed blobs (`ls-tree`), not the worktree. Redirecting only the `MADO_AXIS:` line also conforms, but the full transcript is the honest receipt — it preserves the per-axis rows proving *why* mismatched=0.

The conforming line inside the committed file — the only line the gate parses — is:

```
MADO_AXIS: checked=3 mismatched=0 rev=<REV>
```

If the instrument prints `mismatched=<N>` with `N>0` or a `SETUP_ERROR`, that revision cannot yield a conforming transcript; pick a rev whose committed axis publication is not stale (i.e., where `SCORECARD.md`'s last unquoted `Axis table re-derived at` block matches a fresh derivation of `check-index.py`, `round-31/c2/count.py`, and the `check-index.py --selftest` suite — the three derivations in `derive()`, `:125-159`).

## 4. Live run at `master`

Verbatim command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/check-axis-scores.py --rev master; echo "EXIT=$?"
```

Verbatim output:

```
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=43/43 derived=43/43 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=dbf8b579aeac0f023aaf595770f1cb0049e4baa2
EXIT=0
```

Yes — it prints **`mismatched=0`**, at rev **`dbf8b579aeac0f023aaf595770f1cb0049e4baa2`**, the current `master` tip, which is also the round-36 freeze commit named in `registration.md`. `git merge-base --is-ancestor dbf8b57… master` → `ANCESTOR=YES` (it *is* the tip; a receipt committed on top keeps the ancestry valid forever after).

Current gate state: `quality/receipts/` does not exist on disk (`ls` → "No such file or directory"), no `axis-*.txt` is committed under `quality/receipts/` at master (`git ls-tree` empty), so `tip_axis_transcript=0` today — consistent with `receipts/before-pointers.txt:1`.

## 5. Findings

**F1 — MINOR: the receipt binds the rev, not the instrument.**
The gate's authenticity check is exactly one substring triple on one line (`:183-186`). A hand-authored one-line file `MADO_AXIS: checked=3 mismatched=0 rev=<ancestor>` satisfies `tip_axis_transcript` without `check-axis-scores.py` ever having run — nothing binds the transcript bytes to the instrument, and the `checked=`/row fields are unverified. Also both tests are bare substrings: `rev=<HEX>anything` matches (`HEX40` constrains the *filename*, not the line), and `mismatched=0` inside e.g. `mismatched=0x` would match. Severity MINOR, not MAJOR: the lane's receipts are self-attested under the same trust model as every committed receipt dir, and `tip_axis_transcript` is one conjunct of six in the verdict (`:192-199`) — a forged receipt still must be genuinely committed and still can't satisfy the other five. Worth a clause-level hardening note if wave-2 tightens the gate: anchor on `^MADO_AXIS: checked=3 mismatched=0 rev=<HEX>$`.

**Residual risk / verification gaps:**

- The §3 recipe is verified by code reading plus the live §4 run; I did not create or commit a receipt (read-only bounds), so no end-to-end gate pass was run against a real file. Every gate-side half (filename→`HEX40`→`merge-base`→line scan, `:176-190`) was traced line-by-line.
- "Conforming" is relative to `--branch` (default `master`), not `--rev`: a tip receipt stays valid as the branch advances — intended forward-compatibility, but a receipt for an *old* ancestor also counts under a later `--rev`. Design choice, not a defect.
- The instrument itself is git-read-only: `run_script` extracts committed bytes via `git show` into a tempdir and runs them `cwd=repo` (`:108-122`); my run left no trace (tempdir self-cleans; the `git status` delta between my two checks — `controls/receipts/`, `receipts/clause-attribution.txt` — is concurrent sibling-seat work, not this instrument).

**Tools installed:** none (python3 + git already present; pacman paused host-wide per bounds). No files written outside this report.
