# C1 cheap controls beyond the registered 23 — seat `ExecDoNothingC1`, mado round 46 w1

Target: `tools/mado-devices.py` / `PRED-C1-r46`. Every control is one committed revision of a scratch clone of the
lane at base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, with the control blob at `tools/mado-devices.py`, scored by
the frozen counter (nothing in the lane is written; clones and work dirs under
`/fast/scratch/hyaku/mado-r46/ExecDoNothingC1/`, deleted at the end of the seat):

```
mkdir -p <work>
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r46-devices.py \
        --repo <clone> --rev HEAD --work <work> --nonce <N>
```

## Scores (counter stdout kept in `receipts/`, one file per control)

| control | what it does instead of acquiring the capability | rev | nonce | fixtures | generated | selftest | readonly | verdict |
|---|---|---|---|---|---|---|---|---|
| REF-COPY | the frozen reference itself, verbatim | `d574c1b` | 46 | 90/90 | 150/150 | ok | ok | **TARGET_MET** |
| **B2-STEAL** | imports the reference found *outside* the three hidden paths, pin-selected | `18806bd` | 46 | 90/90 | 150/150 | ok | ok | **TARGET_MET** |
| B2-STEAL, own copy removed | same, stealing only from the L1's own control clones | `18806bd` | 46 | 90/90 | 150/150 | ok | ok | **TARGET_MET** |
| A-LOOKUP | table of the 90 fixtures, device names rank-normalised | `9c2ea2d` | 20261026 | 90/90 | **0/150** | ok | ok | MISSED |
| C-MONITORS-SHIM | round-45 `mado-monitors.py` + 22-code-line patch | `8fcf4e0` | 46 | 32/90 | 2/150 | ok | ok | MISSED |
| D-AGREE-ALL | no config parsing at all; every device agrees | `8391d59` | 46 | 30/90 | 2/150 | ok | ok | MISSED |
| E2-ABSPATH | D + execs `/usr/bin/{hyprctl,libinput,journalctl,udevadm}` by absolute path | `027a3a9` | 46 | 29/90 | 2/150 | ok | **ok** | MISSED |
| E-HYPRCTL | execs `hyprctl`/`libinput` by bare name (PATH) | `c4841e2` | 46 | 1/90 | 0/150 | ok | **fail** | MISSED |
| B-READORACLE | reads the lane's reference/fixtures, walks for the oracle | `4929a6c` | 46 | 1/90 | 0/150 | ok | ok | MISSED |

Verdicts: `receipts/results.txt`. Per-control counter stdout: `receipts/out-<control>.txt`.

## F1 — `TARGET_MET` without the capability: the sandbox leaves the oracle readable (clause i)

`hidden_paths()` (`quality/counters/c1-r46-devices.py:241`) hides exactly `{repo, lane, dirname(lane)}`, and
`sandbox()` (`:251-252`) starts from `--ro-bind / /`. Everything else on the filesystem stays readable, so a scored
tool can import the reference from any copy that is not one of those three paths.

Evidence, both directions:

* `receipts/out-B2-STEAL.txt` — rev `18806bd353a9eb223f6e19923099cd9cd9640d5b`, nonce 46:
  `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`. The tool holds no
  model: it walks `/fast/scratch` for a file named `mado-devices.py` whose sha256 equals `MODEL_SHA256` — the pin
  the counter itself publishes at `quality/counters/c1-r46-devices.py:68` — imports it, and answers with
  `mod.run(argv)`.
* `receipts/out-B2-STEAL-l1only.txt` — same rev, nonce 46, with this seat's own reference copy renamed out of the
  way: still `verdict=TARGET_MET`. The oracle it used is the L1's own positive-control clone, not a copy I placed.
* `receipts/sandbox-probe-report.txt` (payload run inside the counter's own `sandbox()`):
  `stat .../l1-draft/mado-devices.py ENOENT(2)`, `listdir .../mado-shokunin = []` (the three hidden paths work) and
  `reference hits (15, pinned=5): [["/fast/scratch/hyaku/mado-r46/L1/pos/tools/mado-devices.py", 27743, true],
  ["/fast/scratch/hyaku/mado-r46/L1/pos2/.ufo/waves/round-46/l1-draft/mado-devices.py", 27743, true], ...]`. The
  same report lists a v2 reference (`.../ctl1v2/ctl-*/v2/mado-devices.py`, 32401 bytes) reachable too, so a v2
  counter that keeps `sandbox()`/`hidden_paths()` inherits this hole verbatim.
* `receipts/out-B-READORACLE.txt` (rev `4929a6c`) is the failing half: reading the *lane* paths only gives
  `fixtures=1/90` — clause i does what it says for the lane; the leak is the rest of the filesystem.

**Tightening (keeps the reference and the registered 23 controls MET).** Replace `--ro-bind / /` with a whitelist:
`--ro-bind /usr /usr`, `/bin`, `/lib`, `/lib64`, `/etc`, plus `--tmpfs /home --tmpfs /fast --tmpfs /tmp --tmpfs
/var --tmpfs /opt --tmpfs /srv --tmpfs /root --tmpfs /mnt --tmpfs /media`, then `--bind <this case dir> <same>` and
`--bind <marker dir> <marker dir>`. The reference reads only the paths it is handed (`--config`, `--devices`, stdin)
and starts no process, so it stays `90/90 150/150`; V01-V20/STUB never read the filesystem, so they stay MISSED.
If a whitelist is too large a change for a frozen v1, the minimum that kills F1 is `--tmpfs /fast` plus a bind of the
current `fx-*`/`job-*` case dir — but that leaves `/tmp`, `/var/tmp`, `$HOME` and any second scratch root; declare
those if you take the minimum.

Residual after the fix: a tool may still embed the reference (F2).

## F2 — `REF-COPY`: the cheapest `TARGET_MET` is transcription (declared residual)

`receipts/out-ref.txt` — rev `d574c1bc7fe5dab9ae0c8e56acbce355e17cc3a1`, nonce 46:
`fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`. One `cp` of
`.ufo/waves/round-46/l1-draft/mado-devices.py` to `tools/mado-devices.py` and one commit. No clause *should* catch
this — holding the contract is the capability the claim asks for — so this is the declared residual the registration
already carries ("a tool holding a model of the contract is an implementation of it"), now measured: C1's acquisition
cost at this freeze is **one file copy**, and the counter cannot separate "wrote an implementation" from "was handed
one". If the claim is meant to be about independent construction, the wave has to withhold the reference from the
implementing seat or attach a provenance artifact to `tools/mado-devices.py`; neither is mechanizable inside C1.

## F3 — clause r is unsound: only bare-name lookups are caught

`receipts/out-E2-ABSPATH.txt` — rev `027a3a9a923e2ee7bb74e44cbd5409172a984cc8`, nonce 46:
`fixtures=29/90 generated=2/150 selftest=ok readonly=ok`. That tool execs `/usr/bin/hyprctl`,
`/usr/bin/libinput`, `/usr/bin/journalctl` and `/usr/bin/udevadm` on **every** invocation and clause r still prints
`ok`. Inside the counter's own sandbox the same calls are real: `receipts/sandbox-probe-report.txt` lines
`abs-hyprctl ["/usr/bin/hyprctl", "version"] rc=4 out=75 err=0 marker_after=False`,
`abs-udevadm ... rc=0 out=4 marker_after=False`, `abs-libinput ... rc=0 out=7 marker_after=False`, followed by
`marker before bare-name call: False` and `path-hyprctl ["hyprctl", "version"] rc=0 out=0 marker_after=True` — i.e.
the fake bin fires only on the bare name. Compare `receipts/out-E-HYPRCTL.txt` (rev `c4841e2`): `readonly=fail`,
so clause r is exactly a PATH-lookup detector.

**Tightening.** `--ro-bind <fake bin>/<name> /usr/bin/<name>` (and `/usr/sbin`, `/bin`) for the four names, after the
`--ro-bind / /`, in both the run and the selftest sandbox; the selftest currently runs with `PATH=/usr/bin:/bin`
and no fake bin at all (`quality/counters/c1-r46-devices.py:375`), so give it the same `env_a` PATH. This keeps the
reference MET (it opens no process, so no fake is ever executed).

## F4 — the marker directory is a shared writable channel across all ~420 runs

`--bind <marker dir> <marker dir>` is one directory, writable, reused for the selftest, all 90 fixtures × 3 runs and
all 150 generated cases, and clause r only stats the single file named `marker` (`:400`). `B2-STEAL` uses it: the
first invocation walks and writes `.stolen-model`, the other 419 read it
(`A-lookup-emit.py`/`B2-steal.py`, `CACHE = ".stolen-model"`). A tool can therefore accumulate state — past inputs,
past own answers, a stolen path — across cases a clause intends to be independent.

**Tightening.** One fresh `mk-*` per case (or `--dir <marker dir>` giving an empty tmpfs instead of a bind), and
close clause r on *any* file appearing in it, not only `marker`. Reference stays MET (it writes nothing).

## F5 — clause f is fully memorizable; clause g is the only load-bearing anti-memorization clause

`receipts/out-A-LOOKUP.txt` — rev `9c2ea2d011569f323cdb60a40479abb919355b08`, nonce 20261026:
`fixtures=90/90 generated=0/150`. The tool carries no contract: it embeds the 90 fixtures, replaces device names by
their first-appearance rank (dump elements first, then names only configs carry), hashes the canonicalised
(dump, configs) pair and replays the stored `expect`/`rc`; on a miss it prints `SETUP unreadable`. It passes all
three tables — seed-46 A and B and the nonce table — because rank normalisation makes the nonce substitution
invisible. `generated=0/150` is what stops it: the nonce-generated cases are unbounded, so the table cannot answer
them. Tested locally at a second nonce too (`A-lookup-verify.py … 7` → `LOCAL: fixtures=90/90`).

**No tightening needed** — f is all-or-nothing (`fixtures_ok == len(fixtures)`) and g is the clause that carries the
work. **Declared residual:** `fixtures=K/90` is not by itself evidence of capability; the receipt should be read as
`f` *and* `g` together, and a v2 that weakens `g` (fewer cases, fixed seed, model-free oracle) loses C1 entirely.

## F6 — a zero-semantics tool is credited with a third of the fixture set

`receipts/out-D-AGREE-ALL.txt` — rev `8391d59837df3edf2e4611a4d06ee1b71db3e31b`, nonce 46:
`fixtures=30/90 generated=2/150 selftest=ok readonly=ok`. This tool parses **no** config: it prints every keyboard
AGREE with the dump's own names, every mouse AGREE with its own factor, `block=no`, `blocks=0`, `verdict=OK`.
30 fixtures pass anyway: `host`, `host-stdin`, `default-us`, `global-flat`, `global-empty-marker`, `later-file-wins`,
the four `comment-*`, the three `continuation*`, `crlf`, `isspace-trim`, `variable-elsewhere-ignored`,
`nested-not-input`, `inline-block-not-modelled`, `input-touchpad-kb-ignored`, `options-commas`, `multi-layout`,
`model-rules`, `extra-keys-ignored`, and 7 of the 10 `setup-*`. That is the generalisation of the spec's (d)
"host-only tool": the host's live run *is* the all-AGREE shape, so a host-shaped tool is this tool minus the
mice/keyboard generality. `C-MONITORS-SHIM` (round-45 tool + 22 code lines, `receipts/out-C-MONITORS-SHIM.txt`,
rev `8fcf4e0`) reaches 32/90 the same way: the two extra are the size/directory setup fixtures its inherited readers
already answer. The ≤30-line patch cannot get further because the round-45 tool's output vocabulary is
`MADO_MON_*`, and the semantic lines are the whole contract.

**Tightening (calibration, not a kill).** Print a no-op baseline in the receipt, e.g.
`clause=n noop=30/90 2/150` from the registered STUB family, so a fixture set that drifts toward "already correct at
zero semantics" is visible in the band instead of hiding inside `90/90`. No change is needed for the reference; it
is 90/90 *and* 150/150 while the no-op is 30/90 — the gap is the claim.

## Reproduction

```
bash .ufo/waves/round-46/w1/ExecDoNothingC1/run-all.sh    # all eight controls + the sandbox probe
python3 .ufo/waves/round-46/w1/ExecDoNothingC1/A-lookup-verify.py <tool.py> <nonce> # no-bwrap fixture check
```

`B2-STEAL` needs `receipts/out-B2-STEAL-l1only.txt`'s condition to be meaningful: any pinned reference copy outside
`{repo, lane, dirname(lane)}` is enough, and the L1's positive-control clones under `/fast/scratch/hyaku/mado-r46/L1/`
are exactly that.

## Files (sha256 of the artifacts in this directory)

```
16422478346168857e33d0d6305be397e3174ec653b9fa7ba44fb3b665bbe41e A-lookup-emit.py
cd77d2ccf5a814549dbcc7c349dd5dbefb39bc6184d5a850e73bfedbd5925d15 A-lookup-verify.py
b4f1085f32b9a898ee60f252c44df181421f1d6f9200a569cee6de226839cf7a B-readoracle.py
aa9d24d50ce648e94b7811c675cf40ed5f7acd7f763abf11401af747dd290567 B2-steal.py
b9fa44c97f0539105d15038ea3430586a6678843297ecebd77cbf70109ebce91 C-patch.py
12149d589053e563a5799f7d4cdd522317cab5263898d73f53900feb7256bdef D-agree-all.py
df7edf595c2016b9fb9155b8d0ef42757970ea30dbb97ef24938f3f1fdde132f E-hyprctl.py
25a6a106c735806a5d2a448a49593f76383366c632e3a579ffdc3aec3b775526 E2-abspath.py
f774638cf488c31441b3d223e2aaadf84ef2daef17853640ca416d828a770294 probe-payload.py
c146344ba38d745d95fd95273292659b79ffb2053f700344a209fab34bb320a8 probe-sandbox.py
ab30be7445b90dfdb1ade7a874bf06bfef28a704b340b9ed0089cc5b7a84c03e run-all.sh
```

`C-patch.py` is 22 code lines (the ≤30 budget). `A-lookup-emit.py` builds the A-LOOKUP tool from the frozen
fixtures only; no reference code is read or copied by it.
