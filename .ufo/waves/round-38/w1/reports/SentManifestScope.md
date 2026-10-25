# SentManifestScope — round-38 w1: adversarial read of the discrimination manifest sandbox

Scope: `quality/check-r38-discrimination.py` — the `apply_writes` env, the `py` op, and
`_read`/`_write`/`_append`/`delete` path handling — against the frozen manifest
`.ufo/waves/round-38/controls/manifest.json` (`MANIFEST-r38-v1`, 19 controls, working-tree
sha256 `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`, git blob
`ec347320`, committed in `58e55ec`, amended post-freeze in `b6c1d31`). Read-only on the
lane; all PoC artifacts in `/tmp/mado38-SentManifestScope/`. No installs were needed.

## Verdict

**NEEDS REMEDIATION — path sanitization + py-op isolation. Severity: HIGH (verifier-side,
local).** Dropping `subprocess`/`os` from the env dict alone is security theater (F2): the
`py` op is unconfineable in-process, and the file primitives escape the sandbox with or
without it. The current frozen manifest is benign in *effect* (F7) but the *mechanism* is
defective, and the manifest's own snippets already demonstrate two of the escape primitives.

## Findings

### F1 — `_write` does not sanitize paths (FAIL, high)

`quality/check-r38-discrimination.py:114-119`:

```python
def _write(sb, rel, data):
    p = os.path.join(sb, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
```

`os.path.join` semantics: an absolute `rel` discards `sb` entirely; `..` traverses. Same
unsanitized join in `_read` (:110-111), `_append` (:122-124), the env `delete`/`read`
lambdas (:59-60), the `delete` branch (:80), `tool_run`'s ss read (:92, :94), and the
`file` op's `src` join against `controls_dir` (:76). `_write`'s `os.makedirs` (:116) will
create attacker-chosen directories anywhere the user can write.

PoC (gate's own helpers, sandbox `d` inside `/tmp/mado38-SentManifestScope/`):

```
join(d,'/etc/hostname')  = /etc/hostname
join(d,'../escape.txt')  = /tmp/mado38-SentManifestScope/poc-sb-fjng_khm/../escape.txt
abs-escape landed outside sandbox dir: True
trav-escape landed outside sandbox dir: True
abs-read outside sandbox: _read(d,'/etc/hostname') -> 9 bytes
```

### F2 — the `py` op is arbitrary code execution in the gate process; env reduction is cosmetic (FAIL, critical)

`:104-105`: `elif kind == "py": exec(step["code"], env)`. The env dict (:55-70) exposes
`subprocess` (:66), `os` (:64), `sys` (:67), `counters` (:69) — but it is not a boundary:

- CPython injects the **real builtins** into an exec globals dict lacking `__builtins__`,
  so `__import__`/`open` work regardless. The frozen manifest proves this itself:
  `c1-quotefloor`'s py snippet does `import re as _re` inside exec'd code.
- `sys` in env → `sys.modules['__main__']` **is the gate module** — scoring state
  (`observed` :127, `VERDICT` :41, `LANE` :37, `sh` :44) is reachable from manifest data.

End-to-end PoC against the real gate (2-control manifest in scratch, instrument = a garbage
counter that prints no verdict):

```
--- gate exit: 0
control=poc-a instrument=c1 expected=TARGET_MET observed=TARGET_MET ok=1
control=poc-b instrument=c1 expected=TARGET_MISSED observed=TARGET_MISSED ok=1
MADO_R38_DISCRIMINATION: controls=2 correct=2/2 verdict=TARGET_MET
--- counter file after run: "print('instrument replaced by manifest data')\n"
PWNED-abs-write.txt exists: True | content: manifest py op wrote outside the sandbox
PWNED-inproc-patch exists: True | content: py op used builtin open on a host path
PWNED-subprocess exists: True | content:
```

The py ops (a) wrote outside the sandbox via the gate's own `write` lambda with an absolute
path, (b) used builtin `open` on a host path, (c) ran `subprocess.run`, and (d) patched
`sys.modules['__main__'].observed` per control — forcing both verdicts. A `literal` op with
an absolute path overwrote the instrument file on the host mid-run. **Receipt lines are
indistinguishable from a green run.** So: no, dropping `subprocess`/`os` from env does not
close anything — the exec itself must be isolated or removed.

### F3 — the frozen manifest already reads a host absolute path (FAIL as mechanism, benign today)

`c1-r28-verbatim` writes[0] py, quoted verbatim from the manifest:

```python
pkg = open('/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-queue-host-measurement-r28.md').read()
```

Raw builtin `open` on a hard-coded host path (not even the sandbox `read` lambda). Intent
is benign (package text for a verbatim-refused fixture; registration declares shokuknow
read-only and the snippet only reads), but manifest *data* executing host-path `open` is
exactly the F1/F2 primitive in lane-committed form.

### F4 — manifest integrity is unenforced (FAIL, high)

`:144`: `manifest = json.load(open(a.manifest))` — working-tree bytes, any path, no digest
or id check; the summary line (:186) carries no `manifest_sha256`; `git grep 96965518 HEAD`
over the committed tree → **no hits** (no digest pin anywhere; `MANIFEST-r38-v1` appears in
neither committed SCORECARD.md nor LOG.md — lane precedent exists: SCORECARD.md:1624 pins
the round-24 manifest sha256). The manifest was already amended post-freeze (`b6c1d31`).
Consequence: a crib-supplied manifest (or an uncommitted edit) is executed verbatim and,
because the F2 patch travels inside the manifest, **every re-run reproduces the forgery
self-consistently** — only a digest diff against the registration-pinned blob reveals it.

### F5 — instrument overwrite from manifest data (FAIL, high)

PoC above: `{"op":"literal","path":"<absolute path to the instrument>"}` replaced the
counter file on the host before the gate invoked it (:172-174 runs the counter by host
path after `apply_writes`). Against a real run, py code reaches the same target without
knowing any path: env :69 exposes `counters` → `ctx["counters"]["c1"].__file__` is the host
path of `LANE/quality/counters/*.py` — overwrite is a destructive write to lane production
files plus a rubber-stamped gate.

### F6 — incidental: `load_counter` executes counter top-level in-process (note, low)

`:47-51` `spec.loader.exec_module(mod)` runs the counter module in the gate process (used
for `counter_fixture` attr extraction). My first PoC counter had top-level `sys.exit(0)`:
the gate died with **exit 0, empty stderr**, stdout = only the counter's print — silent
early exit. Counters are declared code (lower severity), but it is the same in-process
channel as F2 and a counter could patch the gate identically.

### F7 — current frozen manifest content audit (PASS as content)

Census: 19 controls; ops `py`=12, `literal`=4, `append`=1, `counter_fixture`=1,
`tool_run`=1; **no** `path`/`src`/`ss` value is absolute or contains `..`. All 12 py
snippets are sandbox-relative fixture manipulation via `write`/`read`/`digest`/`re`
(selfreceipt, quotefloor, duprow, nolineage, token-stub, clause-b; lagconst, missall,
onepass, docconn patch `tools/mado-eventq.py` in-clone) except the one absolute read (F3).
No snippet calls `subprocess`/`os.system`. The frozen manifest is benign in effect today;
the mechanism (F1-F5) is the defect.

## Threat model — real or not?

**Real.** Exploit paths, in order of severity:

1. **Scoring subversion (proven, F2/F5):** a crib authors a manifest whose py ops patch
   `sys.modules['__main__'].observed` per control (or overwrite the instrument at its host
   path) → any garbage instrument scores `TARGET_MET` with normal-looking receipt lines,
   and re-runs by verifiers reproduce the forgery. This defeats the one thing the gate
   exists to do: the controls pin what a counter may print, and the py op unpins it.
   Counters cannot do this from their own process; only manifest data can.
2. **Verifier-side host execution (F1/F2/F3):** anyone asked to run a manifest (the lane's
   own workflow does this — `.ufo/waves/round-38/w1-dispatch.json:282` instructs the
   mutation-tester to score "against a scratch copy of the manifest") executes its py ops
   with full user privileges: write anywhere, `subprocess.run` anything, arbitrary
   read/delete (`delete('/…/LOG.md')`).
3. **Lane damage:** absolute-path literal/delete against `quality/counters/*.py`, `LOG.md`,
   or any lane file — the sandbox boundary is fictional for every file op.

Mitigating context (why HIGH, not CRITICAL): the operator already executes arbitrary
*declared* code — counters are imported in-process (:47-51) and run as subprocesses
(:174), and `tool_run` executes the clone's `tools/mado-eventq.py` (:98). The py op's
novelty is converting declared **data** into undeclared **code** and defeating control
pinning; the gate's docstring and the registration's separability story ("C1 reads only
quality/ instruments, the frozen manifest and sandbox clones") treat the manifest as inert.

## Smallest remediation

1. **Path containment (~10 lines):** a `_confine(root, rel)` helper —
   `p = os.path.realpath(os.path.join(os.path.realpath(root), rel))`; reject unless
   `os.path.commonpath([p, root]) == root` — used by `_read`/`_write`/`_append`/`delete`,
   the env lambdas, `tool_run`'s `step["ss"]` read, and the `file` op's `src` (confined to
   `controls_dir`). Catches absolute paths, `..`, and symlink escapes.
2. **Isolate the `py` op (keep it — 12 frozen controls depend on it):** run each snippet in
   a child `python3 -I` helper process that exposes the same callables over a narrow shim,
   so gate state (`observed`, `correct`, `controls`, `ENV`, `LANE`) is unreachable and a
   crashing snippet cannot take down the gate; document in the docstring that py ops are
   code. In-process `exec` can never be confined (builtins injection + `sys.modules`), so
   dropping `subprocess`/`os` from env is hygiene only, worth doing after isolation.
3. **Pin the manifest digest:** print `manifest_sha256=` in the summary (:186) and each
   receipt line, and pin the digest in the registration — makes crib manifests attributable
   and re-runs comparable (round-24 precedent at SCORECARD.md:1624).

## Commands run

- Op/path census of the manifest (python3 -c, read-only) — output quoted in F7.
- `sha256sum` + `git ls-tree HEAD` + `git log --oneline -2` + `git status --porcelain` on
  the manifest — digest/blob/commits quoted above; working tree clean.
- `git grep 96965518 HEAD` / `git grep -n MANIFEST-r38-v1 HEAD -- SCORECARD.md LOG.md` —
  no hits (F4).
- PoC part 1: imported the gate module, called its `_write`/`_read` with absolute and `..`
  rels — output quoted in F1.
- PoC part 2: `python3 -I quality/check-r38-discrimination.py --c1 <scratch garbage
  counter> --c2 <same> --manifest /tmp/mado38-SentManifestScope/poc-manifest.json --rev
  HEAD --sandbox-root /tmp/mado38-SentManifestScope/sb-root` — output quoted in F2;
  sandbox clones deleted after; evidence files kept under `/tmp/mado38-SentManifestScope/`.

## Bounds compliance

No lane file mutated (git usage read-only: ls-tree/log/status/grep); PoC confined to
`/tmp/mado38-SentManifestScope/` (sandbox clones removed; scratch clones committed only
inside themselves, as the gate designs); no compositor/config/service/package touched, no
socket connected; no subagent dispatch; no tool installs (none needed).
