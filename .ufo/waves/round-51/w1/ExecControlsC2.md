# ExecControlsC2 — C2 control fixtures and expected receipts

Seat: `ExecControlsC2` (executor, leaf), mado round 51 / hyaku run 10, wave w1 — BUILD + first-attack.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Round base `6ca8c559a4a3d6d361101592116eea2bc7452437`.
Status: complete. No tracked file was written; everything below lives in the seat dir.

## What was built

Seven fixture controls over the round base, each a sandbox commit in a `git clone --shared` under
the seat scratch dir, scored twice — by the spec-faithful probe and by the frozen counter — with
expected vectors in `expected.json`:

- `ctl-a` round-50 entry bytes at the C2 path + two registry rows + pins → **MISS, clause (c)** at
  99.3% overlap with `corpus/knowledge/hyprland-bind-key-match-r50.md`.
- `ctl-b` round-49 candidate at the C2 path → **MISS, clause (c)** at 99.2% against
  `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md` (candidate baseline is now load-bearing).
- `ctl-c` authored entry, held citations whose pinned tokens are absent from the cited lines →
  **MISS, clause (d) only** (a,b,c pass; `token_missing:…:m_mDispatchers`).
- `ctl-d` authored entry citing S364/S365 with no pin files → **MISS, clause (b) only**
  (`pin_file_absent:ctl-dispatch-a.txt`).
- `ctl-a2` / `ctl-b2` (added) the same copied bodies with only the `source:`/`held:` block rewritten
  → (a)(b)(d) pass, **clause (c) alone rejects the reuse** (99.3% / 99.2%).
- `ctl-e` bare round base → **MISS, entry absent** (`admitted=0/1`, exit 1).

## Findings

1. **The controls named in `claims.md` are not clause-isolating.** `ctl-a`/`ctl-b` fail (c) as
   claimed, but also (b) — the copied bytes cite rows S352–S363, outside the S364–S379 window — and
   (d) — their `held (cited, not re-registered)` lines carry no `keys=` tokens. A counter that
   short-circuits would still MISS, but the receipt cannot prove (c) did the rejecting. `ctl-a2`/
   `ctl-b2` restore isolation by rewriting the metadata block only, keeping the copied body.
2. **The counter draft landed mid-seat and its bytes moved six times.** First pass ran with no
   counter (spec-only, as instructed). The draft then appeared in `w1/ExecCounterC2/`; observed
   states: 22858 B (clean), 22502 B (`932f99…`, **crashed at clause (b) on `ctl-a2`/`ctl-b2`** with
   `TypeError: 'dict' object is not callable`, no final line), 22493 B (`b2515d…`, clean), 23020 B
   (`9f7c4c…`, clean), and the recorded final `25258 B` /
   `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`, stable across a 90 s poll and
   clean on all seven controls. Log: `receipts/counter-drift.txt`. **Freeze must pin the counter
   hash; `receipts/build.txt` and `summary.txt` name the hash the recorded results belong to.**
3. **Counter vs frozen sentence divergences** (all recorded in `spec.md` § Instrument notes):
   the counter reads the quote from the *entry's* `source:` line, not the registry row's quote; the
   held keyword is `keys=`; the candidate baseline is listed at `<rev>` while the sentence says *at
   base* (a fixture that adds a candidate file at `<rev>` would self-match); and clause (c) carries
   an unstated `MIN_BODY_SHINGLES=300` floor that would fail a genuinely short entry on length alone.
4. **A too-short entry MISSes on (c) for the wrong reason.** The counter's body floor is 300
   shingles; the authored fixtures were grown to 359 body shingles so the control is decided by its
   intended clause, not by length. Worth knowing before a real entry is written.
5. Both instruments agree on every control (probe vectors equal counter vectors, one deliberate
   exception: the probe scores the whole entry, so `ctl-a`/`ctl-b` read exactly 100% where the
   counter's body-only overlap reads 99.3%/99.2%).

## Deliverables

- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/spec.md`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/probe-clauses.py`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/drive-controls-c2.py`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/expected.json`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/controls.json`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/SOURCES.md.frag`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/README.md.frag`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/entry-reblock.frag`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/entry-reblock-manifest.frag`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/files/.ufo/waves/round-51/fetch/ctl-dispatch-a.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/files/.ufo/waves/round-51/fetch/ctl-dispatch-b.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/ctl-c/files/corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/ctl-d/files/corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/summary.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/build.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/counter-drift.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-a.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-a2.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-b.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-b2.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-c.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-d.txt`
- `.ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-e.txt`

## Retained evidence

- `receipts/summary.txt`: seven lines of `clauses=… met=… max_overlap=… verdict=… counter=…/rc rev=…`
  plus `controls=7 matched=7 mismatched=0 verdict=OK` and the counter sha256.
- `receipts/<control>.txt`: overlay file hashes, insertion line numbers, full counter output
  (`C2_R51: a/b/c/d ok=…` diagnostics and final line) and full probe output per control.
- `receipts/build.txt`: base, lane, work dir, counter path + sha256 + bytes.
- Reproduce: `python3 -I <seat>/controls-c2/drive-controls-c2.py --work <scratch> --out <dir>
  --counter <lane>/quality/counters/c2-r51-dispatch-entry.py` (exit 0 iff all seven match
  `expected.json`). Fixture commit ids in the receipts are ephemeral (sandbox clone deleted); the
  overlay payloads and recipes are committed here, so the trees are re-derivable byte-for-byte.

## Discipline

- Scratch `/fast/scratch/hyaku/mado-r51/ExecControlsC2/` created and deleted (verified absent); `/fast`
  read 290 G free at the start and 166 G at the end (the delta is siblings' live waves), no ENOSPC.
- Mutating git only inside the sandbox clone, after `git rev-parse --show-toplevel` equalled it.
- No tracked lane file, config plane (`~/.config/hypr`, waybar, walker, terminals, theme), fleet file,
  `shokuknow`, `.ufo/state/`, sibling lane or `scripts/` touched. No compositor socket, no service,
  no pacman, no tool installs.
- `TMPDIR` honoured everywhere; no `/tmp` hardcode.

## Risks / open items for the freeze

- Counter bytes are a live draft: re-run the driver at freeze and pin the hash with the receipt.
- `ctl-a`/`ctl-b` receipts cannot prove clause (c) alone rejected the reuse; keep `ctl-a2`/`ctl-b2`
  in the frozen set if clause-(c) isolation is claimed.
- The counter lists the candidate baseline at `<rev>`; the frozen sentence says *at base*. Decide
  which one the freeze means, or a self-matching candidate fixture is possible.
- The unstated 300-shingle body floor can turn a short honest entry into a clause-(c) MISS; the real
  C2 entry must clear it.

Report: .ufo/waves/round-51/w1/ExecControlsC2.md
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/spec.md
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/probe-clauses.py
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/drive-controls-c2.py
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/expected.json
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/controls.json
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/SOURCES.md.frag
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/README.md.frag
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/entry-reblock.frag
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/append/entry-reblock-manifest.frag
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/files/.ufo/waves/round-51/fetch/ctl-dispatch-a.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/scaffold/files/.ufo/waves/round-51/fetch/ctl-dispatch-b.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/ctl-c/files/corpus/knowledge/hyprland-dispatcher-dispatch-r51.md
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/fixtures/ctl-d/files/corpus/knowledge/hyprland-dispatcher-dispatch-r51.md
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/summary.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/build.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/counter-drift.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-a.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-a2.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-b.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-b2.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-c.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-d.txt
Report: .ufo/waves/round-51/w1/ExecControlsC2/controls-c2/receipts/ctl-e.txt
