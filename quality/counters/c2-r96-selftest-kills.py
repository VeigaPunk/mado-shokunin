#!/usr/bin/env python3
"""Round-96 C2 counter - does the frozen kill-set make the round-93 selftest-strength gate guard the
changed receipt-presence check, and does the round-90 main-path leg stay green at <rev>?

Frozen predicate PRED-C2-r96-v1 (the same sentence as the declaration and the receipt label):
  TARGET_MET iff, at <rev>, the gate is the round-93 frozen gate (gate_sha256 ==
  --expect-gate-sha256) and quality/selftest-kills/check-receipt-presence.json is the frozen candidate
  (kills_sha256 == --expect-kills-sha256), with the kill-set's tool_sha256 equal to the tool's sha256 at
  <rev> (tool_pin=ok), and: (i) the gate on the unmodified tool prints OK and exits 0 and the tool's
  selftest is checks=6 with the six declared labels; (ii) forcing each of the 6 checks to pass
  (neutralisation) makes the gate print WEAK and exit 1, neutralised_flagged == 6/6; (iii) every frozen
  hand weakening of the panel (>= 30 green weakenings, --panel) makes the gate print WEAK and exit 1
  (hand_flagged == hand); (iv) every frozen neutral edit (>= 4 strength-preserving byte changes, selftest
  still green) leaves the gate at OK, exit 0 (neutral_ok == neutrals); (v) controls: the do-nothing
  instrument (flag a variant iff its selftest result line changes) flags fewer than (ii)+(iii); an
  always-OK gate flags none of (iii); an always-WEAK gate fails (i); the round's first-draft tool/kill-set
  (--control-kills, sha-pinned) flags strictly fewer hand weakenings (control_hand_flagged < hand); (vi)
  every one of the 6 labels has a singleton kill; (vii) the gate's --selftest exits 0; and (viii) the
  main-path leg: the round-90 C2 counter (--r90-argv, sha-pinned, --rev substituted) prints
  MADO_RECEIPT_PRESENCE: TARGET_MET at <rev>.

A check is forced to pass by replacing the tool's single
"    failed = [n for n, ok in checks if not ok]" line with
"    failed = [n for n, ok in checks if not ok and n != <label>]".  Labels are derived from the checks
tuples in the selftest at <rev> and must be exactly the six declared labels (OK-rc, OK-lines, MISSING-rc,
MISSING-lines, SETUP-rc, SETUP-lines); the unmutated result line must read checks=6 failed=0.  The
selftest block sits after main() in the changed tool (L1 amendment), so the gate's mutable prefix holds
the whole main path and all six labels have reachable singleton kills.

Variants are checked green before use (python3 -I tool --selftest exits 0 with the unmodified result
line, checks=6 failed=0), else SETUP_ERROR.  The gate runs as python3 -I <gate> --tool <variant> --kills
<kill-set> --allow-sha-drift --scratch-root <fresh> for variants and without --allow-sha-drift for (i).
Every verdict is compared as VERDICT:rc, never the word alone (a hand weakening may surface as
WRONG_CHECK or SURVIVED; both are WEAK:1).

The r90 leg materialises quality/counters/c2-r90-receipt-presence.py from <rev> and runs it with the
--r90-argv JSON's "argv" array from the repo directory: @REV@ becomes <rev>, @BASE_REV@ becomes the
JSON's "base_rev" (5041acf9..., the round-90 base where quality/check-receipt-presence.py is absent;
every tip replay since round-91 pins it - harm-final-r91..r95.txt - and the r90 counter's base control
needs a tool-absent rev), @SCRATCH@ becomes a fresh scratch dir.  The leg holds only on exit 0 with a
non-draft MADO_RECEIPT_PRESENCE: TARGET_MET line (DRAFT_TARGET_MET does not count).
All work lives under --scratch-root.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (--draft-tool / --draft-kills; prints DRAFT_*).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

PRED = "PRED-C2-r96-v1"
GATE = "quality/check-selftest-strength.py"
TOOL = "quality/check-receipt-presence.py"
KILLS = "quality/selftest-kills/check-receipt-presence.json"
R90_COUNTER = "quality/counters/c2-r90-receipt-presence.py"
RESULT_PREFIX = "RECEIPT_PRESENCE_SELFTEST: "
DECLARED_LABELS = ("OK-rc", "OK-lines", "MISSING-rc", "MISSING-lines", "SETUP-rc", "SETUP-lines")
NEEDLE = "    failed = [n for n, ok in checks if not ok]"
LABEL_RE = re.compile(r'^[ \t]+\("((?:[^"\\]|\\.)*)", ', re.M)
VERDICT_RE = re.compile(r"^SELFTEST_STRENGTH: (OK|WEAK|SETUP_ERROR)\b")
R90_LINE_RE = re.compile(r"^MADO_RECEIPT_PRESENCE: (?!DRAFT)(TARGET_MET|TARGET_MISSED|SETUP_ERROR)\b")
MIN_NEUTRAL = 4
ALWAYS_OK = "import sys\nprint('SELFTEST_STRENGTH: OK tool=stub kills=0 held=0 survived=0 wrong_check=0')\nsys.exit(0)\n"
ALWAYS_WEAK = "import sys\nprint('SELFTEST_STRENGTH: WEAK tool=stub kills=0 held=0 survived=0 wrong_check=0')\nsys.exit(1)\n"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def apply(text: str, edit: dict) -> str:
    n = text.count(edit["find"])
    if n == 0 or (n != 1 and not edit.get("all")):
        raise ValueError(f"{edit['id']}: find occurs {n} times")
    return text.replace(edit["find"], edit["replace"]) if edit.get("all") else text.replace(edit["find"], edit["replace"], 1)


def neutralise(text: str, label: str) -> str:
    if text.count(NEEDLE) != 1:
        raise ValueError("neutralisation needle does not occur once")
    return text.replace(NEEDLE, f"    failed = [n for n, ok in checks if not ok and n != {label!r}]", 1)


def labels_of(text: str) -> list[str]:
    body = text[text.index("def selftest("):]
    out: list[str] = []
    for lb in LABEL_RE.findall(body):
        if lb not in out:
            out.append(lb)
    return out


class Run:
    def __init__(self, root: str, timeout: float):
        self.root, self.timeout = root, timeout

    def dir(self) -> str:
        return tempfile.mkdtemp(prefix="p", dir=self.root)

    def selftest_line(self, tool_text: str, result_prefix: str) -> tuple[int | None, str]:
        d = self.dir()
        try:
            p = os.path.join(d, "tool.py")
            with open(p, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(tool_text)
            env = {"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d, "LC_ALL": "C.UTF-8"}
            try:
                r = subprocess.run([sys.executable, "-I", p, "--selftest"], capture_output=True, text=True,
                                   timeout=self.timeout, cwd=d, env=env)
            except subprocess.TimeoutExpired:
                return None, ""
            res = [ln for ln in r.stdout.splitlines() if ln.startswith(result_prefix)]
            return r.returncode, (res[-1] if res else "")
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def gate(self, gate_text: str, tool_text: str, kills_text: str, drift: bool) -> str:
        """Return 'VERDICT:rc' (VERDICT = OK|WEAK|SETUP_ERROR|NONE); compared as a whole, never the word alone."""
        d = self.dir()
        try:
            g, t, k = (os.path.join(d, n) for n in ("gate.py", "tool.py", "kills.json"))
            for path, body in ((g, gate_text), (t, tool_text), (k, kills_text)):
                with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
                    fh.write(body)
            argv = [sys.executable, "-I", g, "--tool", t, "--kills", k, "--scratch-root", os.path.join(d, "s"),
                    "--timeout", "60"] + (["--allow-sha-drift"] if drift else [])
            env = {"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d, "LC_ALL": "C.UTF-8"}
            try:
                r = subprocess.run(argv, capture_output=True, text=True, timeout=1800, cwd=d, env=env)
            except subprocess.TimeoutExpired:
                return "NONE:timeout"
            v = [m.group(1) for m in (VERDICT_RE.match(ln) for ln in r.stdout.splitlines()) if m]
            return f"{v[-1] if v else 'NONE'}:{r.returncode}"
        finally:
            shutil.rmtree(d, ignore_errors=True)


def r90_extras(line: str) -> str:
    def g(p: str, d: str = "?") -> str:
        m = re.search(p, line)
        return m.group(1) if m else d

    return (f"r90_met={g(r'met=(\d+)')}/{g(r'expectations=(\d+)')} "
            f"r90_killed={g(r'killed=(\d+)')}/{g(r'mutants=(\d+)')} "
            f"r90_check_sha256={g(r'check_sha256=([0-9a-f]{64})', '-')}")


def r90_leg(repo: str, rev: str, argv_doc: dict, scratch: str) -> tuple[str, str]:
    """Run the round-90 C2 counter materialised from <rev>; return (leg, last MADO_RECEIPT_PRESENCE line)."""
    src = git_show(repo, rev, R90_COUNTER)
    if src is None:
        return "SETUP_ERROR", f"{R90_COUNTER} absent at {rev}"
    sub = {"@REV@": rev, "@SCRATCH@": tempfile.mkdtemp(prefix="r90-", dir=scratch),
           "@BASE_REV@": argv_doc.get("base_rev")}
    argv = []
    for t in argv_doc.get("argv", []):
        if t in sub:
            if sub[t] is None:
                return "SETUP_ERROR", f"{t} unresolved by the --r90-argv JSON"
            t = sub[t]
        argv.append(t)
    if "--rev" not in argv or "--scratch-root" not in argv:
        return "SETUP_ERROR", "r90 argv lacks --rev/--scratch-root after substitution"
    p = os.path.join(scratch, "r90-counter.py")
    with open(p, "wb") as fh:
        fh.write(src)
    try:
        r = subprocess.run([sys.executable, "-I", p, *argv], capture_output=True, text=True,
                           timeout=2400, cwd=os.path.realpath(repo))
    except subprocess.TimeoutExpired:
        return "SETUP_ERROR", "r90 counter timed out"
    lines = [ln for ln in r.stdout.splitlines() if R90_LINE_RE.match(ln)]
    verdict = R90_LINE_RE.match(lines[-1]).group(1) if lines else ""
    if r.returncode == 0 and verdict == "TARGET_MET":
        return "TARGET_MET", lines[-1]
    if verdict in ("TARGET_MISSED", "TARGET_MET"):
        return "TARGET_MISSED", lines[-1]
    tail = r.stderr.strip()[-200:] if r.stderr else ""
    return "SETUP_ERROR", f"r90 counter rc={r.returncode} no usable line; stderr: {tail}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--expect-panel-sha256", required=True)
    ap.add_argument("--expect-gate-sha256", required=True, help="the round-93 frozen gate's sha256")
    ap.add_argument("--expect-kills-sha256", required=True, help="the frozen kill-set's sha256")
    ap.add_argument("--control-kills", required=True, help="the round's first-draft kill-set file")
    ap.add_argument("--expect-control-sha256", required=True, help="its sha256")
    ap.add_argument("--r90-argv", required=True, help="the r90-c2-argv JSON (placeholders @REV@/@BASE_REV@/@SCRATCH@)")
    ap.add_argument("--expect-r90-argv-sha256", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--draft-tool", help="DRAFT only: score this tool file instead of <rev>:" + TOOL)
    ap.add_argument("--draft-kills", help="DRAFT only: score this kill-set file instead of <rev>:" + KILLS)
    a = ap.parse_args()
    draft = bool(a.draft_tool or a.draft_kills)
    sys.stdout.reconfigure(line_buffering=True)
    tag = "DRAFT_" if draft else ""

    def setup(msg: str) -> int:
        print(f"MADO_SELFTEST_KILLS: SETUP_ERROR pred={PRED} {msg}")
        return 2

    try:
        panel_b = open(a.panel, "rb").read()
    except OSError as e:
        return setup(f"cannot read --panel: {e}")
    if sha(panel_b) != a.expect_panel_sha256:
        return setup(f"panel sha256 {sha(panel_b)} != pinned")
    try:
        panel = json.loads(panel_b)
    except ValueError as e:
        return setup(f"panel JSON unusable: {e}")
    if isinstance(panel, dict) and isinstance(panel.get("hand"), list) and isinstance(panel.get("neutral"), list):
        hand, neut = panel["hand"], panel["neutral"]
    elif isinstance(panel, list):
        hand = [w for w in panel if isinstance(w, dict) and w.get("kind") == "hand"]
        neut = [w for w in panel if isinstance(w, dict) and w.get("kind") == "neutral"]
        if len(hand) + len(neut) != len(panel):
            return setup("panel list holds entries without kind hand|neutral")
    else:
        return setup("panel JSON neither a {id,kind,find,replace} list nor {hand,neutral}")
    for w in hand + neut:
        if not isinstance(w, dict) or not all(isinstance(w.get(f), str) and w[f] for f in ("id", "find", "replace")):
            return setup(f"panel entry {w.get('id', '?') if isinstance(w, dict) else w!r} lacks id/find/replace strings")

    gate_b = git_show(a.repo, a.rev, GATE)
    try:
        tool_b = open(a.draft_tool, "rb").read() if a.draft_tool else git_show(a.repo, a.rev, TOOL)
        kills_b = open(a.draft_kills, "rb").read() if a.draft_kills else git_show(a.repo, a.rev, KILLS)
    except OSError as e:
        return setup(f"cannot read draft bytes: {e}")
    absent = [n for n, b in (("gate", gate_b), (TOOL, tool_b), (KILLS, kills_b)) if b is None]
    if absent:
        return setup(f"absent at {a.rev}: {', '.join(absent)} (kill-set path pinned as {KILLS})")
    try:
        kills = json.loads(kills_b.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        return setup(f"kill-set JSON unusable: {e}")
    try:
        ctl_b = open(a.control_kills, "rb").read()
    except OSError as e:
        return setup(f"cannot read --control-kills: {e}")
    if sha(ctl_b) != a.expect_control_sha256:
        return setup(f"control kill-set sha256 {sha(ctl_b)} != pinned")
    try:
        argv_doc_b = open(a.r90_argv, "rb").read()
    except OSError as e:
        return setup(f"cannot read --r90-argv: {e}")
    if sha(argv_doc_b) != a.expect_r90_argv_sha256:
        return setup(f"r90-argv sha256 {sha(argv_doc_b)} != pinned")
    try:
        argv_doc = json.loads(argv_doc_b.decode("utf-8"))
        if not isinstance(argv_doc.get("argv"), list) or not all(isinstance(t, str) for t in argv_doc["argv"]):
            raise ValueError("argv is not a string list")
    except (ValueError, UnicodeDecodeError) as e:
        return setup(f"r90-argv JSON unusable: {e}")

    gate_pin = sha(gate_b) == a.expect_gate_sha256
    kills_pin = sha(kills_b) == a.expect_kills_sha256
    tool_pin = kills.get("tool_sha256") == sha(tool_b)
    os.makedirs(a.scratch_root, exist_ok=True)
    root = tempfile.mkdtemp(prefix="c2r96-", dir=a.scratch_root)
    run = Run(root, a.timeout)
    try:
        tt = tool_b.decode("utf-8")
        rc, line = run.selftest_line(tt, RESULT_PREFIX)
        m = re.match(r"^" + re.escape(RESULT_PREFIX) + r"checks=(\d+) failed=0$", line)
        if rc != 0 or not m:
            return setup(f"{TOOL} selftest at <rev> not green: rc={rc} {line!r}")
        checks = int(m.group(1))
        if checks != 6:
            return setup(f"{TOOL} selftest reports checks={checks}; the declared change is checks=6")
        if tt.count(NEEDLE) != 1:
            return setup("neutralisation needle does not occur exactly once in the tool")
        try:
            labels = labels_of(tt)
        except ValueError:
            return setup("tool has no def selftest(")
        if len(labels) != 6 or set(labels) != set(DECLARED_LABELS):
            return setup(f"selftest labels enumerated {labels!r} != the six declared {list(DECLARED_LABELS)}")
        variants = []  # (kind, id, text): N neutralisation, W hand weakening, Z neutral edit
        try:
            for lb in labels:
                variants.append(("N", lb, neutralise(tt, lb)))
            for w in hand:
                variants.append(("W", w["id"], apply(tt, w)))
            for z in neut:
                variants.append(("Z", z["id"], apply(tt, z)))
        except ValueError as e:
            return setup(str(e))
        with ThreadPoolExecutor(a.workers) as ex:
            vlines = list(ex.map(lambda v: run.selftest_line(v[2], RESULT_PREFIX), variants))
        for (kind, vid, _), (vrc, vln) in zip(variants, vlines):
            if vrc != 0 or vln != line:
                return setup(f"variant {kind}:{vid} does not keep the selftest green: rc={vrc} {vln!r}")
        kills_t = kills_b.decode("utf-8")
        gate_t = gate_b.decode("utf-8")
        jobs, weak_j, neut_j, hand_j, nonw_j = [("pos", tt, kills_t, False)], [], [], [], []
        for k, (kind, vid, txt) in enumerate(variants, start=1):
            jobs.append((f"{k} {kind}:{vid}", txt, kills_t, True))
            if kind in ("N", "W"):
                weak_j.append(k)
                if kind == "N":
                    neut_j.append(k)
                else:
                    hand_j.append(k)
            else:
                nonw_j.append(k)

        def vector(gtext: str, idxs: list[int]) -> dict[int, str]:
            sel = [jobs[k] for k in idxs]
            with ThreadPoolExecutor(a.workers) as ex:
                vs = list(ex.map(lambda jb: run.gate(gtext, jb[1], jb[2], jb[3]), sel))
            return dict(zip(idxs, vs))

        vec = vector(gate_t, list(range(len(jobs))))
        for jb, v in zip(jobs, (vec[k] for k in sorted(vec))):
            print(f"probe {jb[0]} {v}")
        pos = vec[0]
        nflag = sum(vec[k] == "WEAK:1" for k in neut_j)
        hflag = sum(vec[k] == "WEAK:1" for k in hand_j)
        zok = sum(vec[k] == "OK:0" for k in nonw_j)
        dn = sum(vlines[k - 1][1] != line for k in weak_j)  # do-nothing instrument: flag iff the result line changes
        ok_v = vector(ALWAYS_OK, hand_j)
        aok = sum(ok_v[k] == "WEAK:1" for k in hand_j)
        aw = run.gate(ALWAYS_WEAK, tt, kills_t, False)
        ctl_txt = ctl_b.decode("utf-8")
        with ThreadPoolExecutor(a.workers) as ex:
            ctl_v = list(ex.map(lambda k: run.gate(gate_t, jobs[k][1], ctl_txt, True), hand_j))
        ctl_h = sum(v == "WEAK:1" for v in ctl_v)
        singles_set: set[str] = set()
        covered_set: set[str] = set()
        for kk in kills.get("kills", []):
            if not isinstance(kk, dict):
                continue
            mf = kk.get("must_fail")
            mf = [mf] if isinstance(mf, str) else (mf or [])
            covered_set.update(mf)
            if len(mf) == 1:
                singles_set.add(mf[0])
        singles = sum(1 for lb in labels if lb in singles_set)
        covered = sum(1 for lb in labels if lb in covered_set)
        d = run.dir()
        gp = os.path.join(d, "gate.py")
        with open(gp, "w", encoding="utf-8") as fh:
            fh.write(gate_t)
        gs = subprocess.run([sys.executable, "-I", gp, "--selftest"], capture_output=True, text=True,
                            timeout=600, cwd=d, env={"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d})
        gs_ok = gs.returncode == 0
        shutil.rmtree(d, ignore_errors=True)
        r90v, r90line = r90_leg(a.repo, a.rev, argv_doc, root)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    met = (gate_pin and kills_pin and tool_pin and pos == "OK:0" and checks == 6
           and nflag == len(neut_j) and hflag == len(hand_j) and zok == len(nonw_j)
           and dn < len(weak_j) and aok == 0 and aw != "OK:0" and gs_ok
           and ctl_h < len(hand_j) and singles == 6 and r90v == "TARGET_MET"
           and len(neut) >= MIN_NEUTRAL)
    word = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"MADO_SELFTEST_KILLS: {tag}{word} pred={PRED} rev={'draft' if draft else a.rev} "
          f"gate_pin={'ok' if gate_pin else 'FAIL'} kills_pin={'ok' if kills_pin else 'FAIL'} "
          f"tool_pin={'ok' if tool_pin else 'FAIL'} checks={checks} labels={len(labels)}/6 "
          f"labels_covered={covered}/6 singleton_labels={singles}/6 positive={pos} "
          f"neutralised_flagged={nflag}/{len(neut_j)} hand_flagged={hflag}/{len(hand_j)} "
          f"neutral_ok={zok}/{len(nonw_j)} do_nothing_flagged={dn} always_ok_flagged={aok} "
          f"always_weak_positive={aw} gate_selftest={'ok' if gs_ok else 'FAIL'} "
          f"control_hand_flagged={ctl_h}/{len(hand_j)} r90_leg={r90v} {r90_extras(r90line)} "
          f"tool_path={TOOL} kill_path={KILLS} gate_sha256={sha(gate_b)} kills_sha256={sha(kills_b)} "
          f"tool_sha256={sha(tool_b)} control_sha256={sha(ctl_b)}")
    if draft:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
