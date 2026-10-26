# RevC1Counter — review of `quality/counters/c1-r46-devices.py` (round-46 w1)

Seat RevC1Counter-3, 2026-10-26. Target: the frozen C1 counter (freeze commit `8c5434c6`), line-by-line, for
bugs and unfair passes/fails. Method: full source read; every suspicion then executed — a baseline scoring run
plus six diagnostic runs, five of them on clearly-labeled scratch COPIES of the counter (never the frozen file),
one on the frozen counter itself against a fake-tool clone. All runs used bubblewrap 0.13.1 already on the host;
nothing was installed. Scratch lived under `/fast/scratch/hyaku/mado-r46/RevC1Counter/` and was deleted after
receipts were copied to `receipts/` beside this file.

## Baseline (the counter as frozen, on honest input)

- Pins check out: `c1-r46-fixtures.json` sha256 `027ed508…` and `l1-draft/mado-devices.py` sha256 `b229efd0…`
  equal the constants at `c1-r46-devices.py:66,68`; both blobs are tracked at the freeze commit (modes 100644 /
  100755, `git ls-tree 8c5434c6`).
- Full run, scratch clone `b6721575` (reference copied to `tools/mado-devices.py`, committed there), nonce 46,
  17 s: `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0 —
  reproduces the REF line of `receipts/ctl-c1.txt` independently (`receipts/baseline-nonce46.txt`).
- Same run repeated: byte-identical stdout (`receipts/baseline-rerun-nonce46.txt`); nonce 999: TARGET_MET
  (`receipts/baseline-nonce999.txt`). The docstring's "seed-46 part reproduces exactly / under any nonce" holds.

## Findings, by severity

### F1 — MEDIUM (unfair pass; adversarial tool): clause r defeated by erasing the marker
`sandbox()` (`c1-r46-devices.py:251-257`) ro-binds `/` but leaves the counter's own `--work` tree visible, and
`marker_dir` is the sandbox's ONLY writable bind (`:256`). `hidden_paths()` (`:241-243`) hides {repo, lane, lane
parent} — not the work dir — so a scored tool can walk to `../../mk-*/marker` and unlink it after calling the
fake `hyprctl` (which creates it, `make_fakebin` `:141-146`). Demonstrated on two clones, same 0-fixture
diagnostic copy of the counter:
- `receipts/probe-r-noerase.txt` (rev `c8be2897`, tool `receipts/fake-noerase.py`): fake hyprctl called via
  inherited PATH → `clause=r marker=present`, `readonly=fail`. The clause works.
- `receipts/probe-r-erase.txt` (rev `84d1f836`, tool `receipts/fake-erase.py`): same call **plus**
  `os.unlink` of the marker → `clause=r marker=absent`, `readonly=ok`. Evaded.
The declared residual ("the read-only clause catches PATH lookups only") does not cover post-hoc erasure.
Fix: `--tmpfs` the work dir (or its parent) inside the sandbox, or check a nonce-valued marker name.

### F2 — MEDIUM (weakens clause i): "model invisible" is lane-local only
Inside the same sandbox, `/fast/scratch/hyaku/mado-r46/*` is readable (`receipts/probe-hide.txt`: 7 sibling
seat dirs visible, including other executors' and the L1's). Any sibling clone checked out at the freeze holds
`l1-draft/mado-devices.py` — the clause-g oracle — and `c1-r46-fixtures.json` as plain files. The lane, fleet
root and repo ARE hidden (lane model hidden: yes; fleet root: 0 entries), but the docstring sentence "The model
is invisible to the tool (clause i)" only holds within {repo, lane, lane parent}. Corroborates and extends
SentTool-3's F1/F2 (`.ufo/waves/round-46/w1/SentTool/findings.md`): live `hyprland.sock` reachability via
`/run/user/<uid>` — which `env_b` itself hands the tool (`:268`) — absolute-path execs bypassing the fakes, and
the selftest env having no fakebin at all (`:375`, `PATH=/usr/bin:/bin`). Scoring impact is bounded by the
declared residual "a tool holding a model of the contract is an implementation of it", but a v2 should tmpfs
{work parent, `/run/user/<uid>`, `$HOME`} and ro-bind the four fakes over their `/usr/bin` names.

### F3 — MEDIUM-LOW (crash instead of clause-fail; exit-code ambiguity): selftest parse
`:382` `n[0].isdigit() and int(n[0])`: a tool printing `MADO_DEVICES_SELFTEST: ³/³ passed` (superscript digits
are `isdigit()`-true) raises `ValueError` — traceback, exit 1, no `clause=s` line, no verdict line
(`receipts/probe-sup.txt`, run against the FROZEN counter). Exit 1 is indistinguishable from an honest
TARGET_MISSED for any consumer keying on exit codes. Fix: `isascii()` guard or try/except, and always print a
`clause=s` line.

### F4 — LOW (unfair pass, currently pinned shut): vacuous fixture count
`:402` `fixtures_ok == len(fixtures)` is vacuously true for an empty fixtures file. Demonstrated on a
diagnostic copy re-pinned to the sha256 of `[]`: `fixtures=0/0 generated=150/150 selftest=ok readonly=ok
tool=present verdict=TARGET_MET`, exit 0 (`receipts/probe-empty.txt`). Only `FIXTURES_SHA256` (`:66`) prevents
it; the counter enforces no minimum count even though the registration target is 90/90. Fix: minimum count or
per-clause minimums in `met`.

### F5 — LOW (coverage hole, unexercised by pinned fixtures): stdin dropped by the usage branch
`:300-301` `if configs == "usage": args = ["--devices", dp]` overwrites the stdin form `["--devices", "-"]`
(set `:293-295`) while still piping the dump (`data` stays non-None). Demonstrated with a synthetic
stdin+usage fixture on a diagnostic copy: `DEBUGPROBE args=['--devices', '<file>'] data_is_None=False`
(`receipts/probe-argv.txt`, fixture `receipts/fx-stdin-usage.json`). The pinned 90 never combine stdin+usage
(2 stdin fixtures both have config lists; the 1 usage fixture is stdin=false — jq over the pinned file), and
both branches produce the same observable output (SETUP usage, rc 2), so no wrong verdict is reachable this
round. Fix: `args = ["--devices", "-" if fx["stdin"] else dp]`.

### F6 — INFO (availability; undeclared timeout): hanging tool costs 20 s per run
`run_tool` timeout is 20 s (`:275`); the docstring declares only the 60 s selftest budget. A tool that hangs
every run ⇒ 90×3 + 150 runs ⇒ ~2h20 m of grinding. Behavior verified honest and clean: per-fixture
`FAIL 46A:timeout; 46B:timeout; nA:timeout`, verdict TARGET_MISSED exit 1, and no orphan bwrap/python
processes afterwards (`receipts/probe-timeout.txt`).

## Task checklist — examined, no defect

- **Fixture loading/pinning**: sha-pinned, Setup(exit 2) on missing/mismatch; model loaded from the counter's
  OWN lane (`:67`), never from `--repo`.
- **{A}..{D} substitution**: `names()` (`:119-127`) draws ASCII `[a-z0-9+-]` names, mutually non-substring;
  `subst` (`:129-137`) applies one table uniformly to configs, dump and expect lines; braces cannot occur in
  generated names, so no wrong-substitution or ordering hazard. The one escaping-sensitive fixture
  (`unicode-name`, literal `é`) has expect lines pre-escaped to the reference's `json.dumps` ensure_ascii form;
  since substituted names can never be non-ASCII, the placeholder/escaping interaction is closed.
- **BIG_CONFIG/BIG_DUMP**: both exercised (`setup-config-too-large` via `--config`, `setup-dump-too-large` via
  stdin), both expect `SETUP too_large` rc 2 and pass in baseline. The `@BIG`/`@BIGDUMP` sentinels could only
  collide with L1-authored fixture values, which are sha-pinned.
- **stdin path**: exercised by `host-stdin` and `setup-dump-too-large`; see F5 for the latent usage-branch bug.
- **env A/B**: exactly as docstring (`:260-269`); env_b's rng use (job prefix + signature) is deterministic per
  nonce.
- **Generated-case alignment (leak question)**: no leak. `gen_case` (`:157-234`) aligns dump fields to
  `model.expected_names(st, name)` where `st` is parsed from the very texts handed to the tool — the dump is a
  function of (texts, rng) only. The model runs in-process in the counter (`:105-111`), and the sandbox hides
  it (probe-hide). The oracle `want` is computed from the exact bytes the tool receives, so alignment errors
  could only reduce AGREE coverage, never fabricate fails; the zip order at `:227-228` matches the model's
  NAMES order. "Oracle is the reference" tautology is a declared residual.
- **Selftest parse**: strict on shape (3 tokens, N==N, N≥30); the crash case is F3.
- **Final verdict/exit codes**: conjunction matches the docstring clauses; exit 0/1/2 as declared; vacuity is
  F4; the uncaught-exception path (F3) is the one way to exit 1 without a verdict line.

## Residual risk and verification gaps

- I did not myself demonstrate AF_UNIX socket reachability or absolute-path hyprctl exec scoring TARGET_MET —
  those are SentTool-3's receipts (its F1/F2), which my F1/F2 code reading supports; cross-seat unification is
  the L1's call. My erase demo reaches `readonly=ok` but with verdict TARGET_MISSED (fixtures not forged); the
  two findings compose: a tool that erases the marker AND passes clauses f/g would be MET with a forbidden
  lookup — nothing in the frozen harness detects that composition.
- Clause-g distributional coverage was not re-derived beyond the controls' evidence (V01–V20 all MISSED per
  `receipts/ctl-c1.txt`; my baseline agrees).
- A v2 counter is being built in the lane (ConnCrossClaim broadcast): F1–F5 carry over verbatim to any v2 that
  keeps `sandbox()`, `hidden_paths()`, `make_fakebin()` or the clause-s env.
- No pacman or any package transaction was run; no tool installed; no host service touched; all live reads
  were `hyprctl`-free (fixtures only). Writes: this seat dir only; lane untouched; scratch deleted.
