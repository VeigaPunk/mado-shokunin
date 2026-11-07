#!/usr/bin/env python3
"""Round-94 C2 counter - do the frozen kill-sets make the round-93 selftest-strength gate guard mado-xdgmime and mado-mime?

Frozen predicate PRED-C2-r94-v1 (the same sentence as the declaration and the receipt label):
  TARGET_MET iff, at <rev>, the gate is the round-93 frozen gate (sha256 == --expect-gate-sha256) and both
  kill-sets are the frozen candidates (sha256 == --expect-kills-sha256 xdgmime,mime), and:
  (i) the gate on each unmodified tool with its kill-set prints OK and exits 0 (positive=VERDICT:rc per tool),
      and each kill-set's tool_sha256 equals the tool's sha256 at <rev> (tool_pin);
  (ii) for every selftest check of each tool (the labels of its checks tuples at <rev>, as many as its result
      line's checks=N: 12 + 17 = 29), the tool with that one check forced to pass makes the gate print WEAK and
      exit 1 (neutralised_flagged == 29);
  (iii) every frozen hand weakening of the panel (the selftest stays green) makes the gate print WEAK and exit 1
      (hand_flagged == hand);
  (iv) every frozen neutral edit of the panel (strength-preserving byte change, selftest still green) leaves the
      gate at OK, exit 0 (neutral_ok == neutrals);
  (v) controls: the do-nothing instrument (flag a variant iff its selftest result line changes) flags fewer than
      (ii)+(iii); an always-OK gate flags none of the weakenings; an always-WEAK gate fails (i) on both tools; a
      sha-diff gate fails (iv) (flags some neutral edit);
  (vi) the gate's --selftest exits 0.
  Frozen amendment before any measurement (round-94 w1 R94MCritic C2-F1/F4, R94MReviewC2 §3, R94MMutC2 §2, folded
  in by the L1): (vii) the round's first-draft kill-sets (--control-kills, sha256-pinned; 12 + 15 kills, the ones
  the wave's mutation tester escaped 46 times) flag strictly fewer hand weakenings than the frozen kill-sets
  (control_hand_flagged < hand), so the panel discriminates kill-sets and a union-covering forgery is visible.
  The count of labels with a singleton kill (must_fail exactly that one label) is printed, not a conjunct.  The
  "before" of the claim is the do-nothing instrument's count over the 29 neutralisations (the counter itself
  stops SETUP_ERROR where the kill-sets are absent).

A check is forced to pass by replacing the tool's single
"    failed = [n for n, ok in checks if not ok]" line with
"    failed = [n for n, ok in checks if not ok and n != <label>]".  Labels are derived from the checks tuples at
<rev> (the checks += [("label", ...)] list entries and the checks.append(("label", ...)) calls in mado-xdgmime;
the chk("label", ...) calls in mado-mime); a label named in several arms (if/else append pairs) is one check, so
the unique labels in order are taken and their count must equal the result line's checks=N.

Variants are checked green before use (python3 -I tool --selftest exits 0 with the unmodified tool's result line,
checks=N failed=0), else SETUP_ERROR.  The gate runs as python3 -I <gate> --tool <variant> --kills <kill-set>
--allow-sha-drift for variants and without the flag for (i).  Every verdict is compared as VERDICT:rc, never the
word alone.  All work lives under --scratch-root.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (--draft-kills XDGMIME,MIME; prints DRAFT_*).
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

PRED = "PRED-C2-r94-v1"
GATE = "quality/check-selftest-strength.py"
TOOLS = ("tools/mado-xdgmime.py", "tools/mado-mime.py")
KILLS = ("quality/selftest-kills/mado-xdgmime.json", "quality/selftest-kills/mado-mime.json")
RESULT_PREFIX = ("MADO_XDGMIME_SELFTEST: ", "MADO_MIME_SELFTEST: ")
NEEDLE = "    failed = [n for n, ok in checks if not ok]"
VERDICT_RE = re.compile(r"^SELFTEST_STRENGTH: (OK|WEAK|SETUP_ERROR)\b")
ALWAYS_OK = "import sys\nprint('SELFTEST_STRENGTH: OK tool=stub kills=0 held=0 survived=0 wrong_check=0')\nsys.exit(0)\n"
ALWAYS_WEAK = "import sys\nprint('SELFTEST_STRENGTH: WEAK tool=stub kills=0 held=0 survived=0 wrong_check=0')\nsys.exit(1)\n"
SHA_DIFF = (
    "import hashlib, json, sys\n"
    "a = sys.argv\n"
    "tool = a[a.index('--tool') + 1]; kills = a[a.index('--kills') + 1]\n"
    "want = json.load(open(kills))['tool_sha256']\n"
    "got = hashlib.sha256(open(tool, 'rb').read()).hexdigest()\n"
    "v = 'OK' if got == want else 'WEAK'\n"
    "print(f'SELFTEST_STRENGTH: {v} tool=stub kills=0 held=0 survived=0 wrong_check=0')\n"
    "sys.exit(0 if v == 'OK' else 1)\n")


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


def labels_of(text: str, tool_idx: int) -> list[str]:
    body = text[text.index("def selftest("):]
    pats = (r'^[ \t]+\("((?:[^"\\]|\\.)*)", ', r'checks\.append\(\("((?:[^"\\]|\\.)*)"') if tool_idx == 0 \
        else (r'chk\("((?:[^"\\]|\\.)*)"',)
    out: list[str] = []
    for p in pats:
        for lb in re.findall(p, body, re.M):
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--expect-panel-sha256", required=True)
    ap.add_argument("--expect-gate-sha256", required=True, help="the round-93 frozen gate's sha256")
    ap.add_argument("--expect-kills-sha256", required=True, help="comma pair: xdgmime,mime frozen candidate sha256")
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--control-kills", required=True, help="comma pair: the first-draft kill-sets (xdgmime,mime)")
    ap.add_argument("--expect-control-kills-sha256", required=True, help="comma pair of their sha256")
    ap.add_argument("--draft-kills", help="DRAFT only: comma pair of kill-set files instead of <rev>: (xdgmime,mime)")
    a = ap.parse_args()
    draft = bool(a.draft_kills)
    sys.stdout.reconfigure(line_buffering=True)
    tag = "DRAFT_" if draft else ""
    expect_kills = [s.strip() for s in a.expect_kills_sha256.split(",")]

    def setup(msg: str) -> int:
        print(f"MADO_SELFTEST_KILLS: SETUP_ERROR pred={PRED} {msg}")
        return 2

    if len(expect_kills) != 2:
        return setup("--expect-kills-sha256 must be a comma pair xdgmime,mime")
    panel_b = open(a.panel, "rb").read()
    if sha(panel_b) != a.expect_panel_sha256:
        return setup(f"panel sha256 {sha(panel_b)} != pinned")
    try:
        panel = json.loads(panel_b)
        panel_h = {t: [w for w in panel["hand"] if w["tool"] == t] for t in TOOLS}
        panel_n = {t: [w for w in panel["neutral"] if w["tool"] == t] for t in TOOLS}
    except (ValueError, KeyError, TypeError) as e:
        return setup(f"panel JSON unusable: {e}")
    gate_b = git_show(a.repo, a.rev, GATE)
    tools_b = [git_show(a.repo, a.rev, t) for t in TOOLS]
    if draft:
        parts = a.draft_kills.split(",")
        if len(parts) != 2:
            return setup("--draft-kills must be a comma pair xdgmime,mime")
        try:
            kills_b = [open(p, "rb").read() for p in parts]
        except OSError as e:
            return setup(f"cannot read --draft-kills: {e}")
    else:
        kills_b = [git_show(a.repo, a.rev, k) for k in KILLS]
    if gate_b is None or any(t is None for t in tools_b) or any(k is None for k in kills_b):
        which = [n for n, b in (("gate", gate_b), *zip(TOOLS, tools_b), *zip(KILLS, kills_b)) if b is None]
        return setup(f"absent at {a.rev}: {', '.join(which)} (kill-set paths pinned as {KILLS[0]}, {KILLS[1]})")
    try:
        kills = [json.loads(k.decode("utf-8")) for k in kills_b]
    except (ValueError, UnicodeDecodeError) as e:
        return setup(f"kill-set JSON unusable: {e}")
    try:
        ctl_b = [open(p, "rb").read() for p in a.control_kills.split(",")]
    except OSError as e:
        return setup(f"cannot read --control-kills: {e}")
    if len(ctl_b) != 2 or [sha(x) for x in ctl_b] != [x.strip() for x in a.expect_control_kills_sha256.split(",")]:
        return setup("control kill-sets missing or sha256 != pinned")
    gate_pin = sha(gate_b) == a.expect_gate_sha256
    kills_pin = [sha(kills_b[i]) == expect_kills[i] for i in (0, 1)]
    tool_pin = [kills[i].get("tool_sha256") == sha(tools_b[i]) for i in (0, 1)]
    os.makedirs(a.scratch_root, exist_ok=True)
    root = tempfile.mkdtemp(prefix="c2r94-", dir=a.scratch_root)
    run = Run(root, a.timeout)
    try:
        base, labels = [], []
        for i in (0, 1):
            tt = tools_b[i].decode("utf-8")
            rc, line = run.selftest_line(tt, RESULT_PREFIX[i])
            m = re.match(r"^" + re.escape(RESULT_PREFIX[i]) + r"checks=(\d+) failed=0$", line)
            if rc != 0 or not m:
                return setup(f"{TOOLS[i]} selftest at <rev> not green: rc={rc} {line!r}")
            lbs = labels_of(tt, i)
            n = int(m.group(1))
            if len(lbs) != n or len(set(lbs)) != n:
                return setup(f"{TOOLS[i]}: labels enumerated {len(lbs)} (unique {len(set(lbs))}) != checks={n}")
            base.append((tt, line, n))
            labels.append(lbs)
        variants = []  # (tool_idx, kind, id, text)
        try:
            for i in (0, 1):
                tt = base[i][0]
                for lb in labels[i]:
                    variants.append((i, "N", lb, neutralise(tt, lb)))
                for w in panel_h[TOOLS[i]]:
                    variants.append((i, "W", w["id"], apply(tt, w)))
                for z in panel_n[TOOLS[i]]:
                    variants.append((i, "Z", z["id"], apply(tt, z)))
        except ValueError as e:
            return setup(str(e))
        with ThreadPoolExecutor(a.workers) as ex:
            vlines = list(ex.map(lambda v: run.selftest_line(v[3], RESULT_PREFIX[v[0]]), variants))
        for (i, kind, vid, _), (rc, ln) in zip(variants, vlines):
            if rc != 0 or ln != base[i][1]:
                return setup(f"variant T{i + 1} {kind}:{vid} does not keep the selftest green: rc={rc} {ln!r}")
        jobs, pos_j, weak_j, neut_j, nonw_j = [], [], [], [], []
        for i in (0, 1):
            kt = kills_b[i].decode("utf-8")
            pos_j.append(len(jobs))
            jobs.append((f"T{i + 1} pos", base[i][0], kt, False))
            for (j, kind, vid, txt) in variants:
                if j != i:
                    continue
                jobs.append((f"T{i + 1} {kind}:{vid}", txt, kt, True))
                k = len(jobs) - 1
                if kind in ("N", "W"):
                    weak_j.append(k)
                    if kind == "N":
                        neut_j.append(k)
                else:
                    nonw_j.append(k)

        def vector(gtext: str) -> list[str]:
            with ThreadPoolExecutor(a.workers) as ex:
                return list(ex.map(lambda jb: run.gate(gtext, jb[1], jb[2], jb[3]), jobs))

        vec = vector(gate_t := gate_b.decode("utf-8"))
        for jb, v in zip(jobs, vec):
            print(f"probe {jb[0]} {v}")
        pos = [vec[k] for k in pos_j]
        nflag = sum(vec[k] == "WEAK:1" for k in neut_j)
        hflag = sum(vec[k] == "WEAK:1" for k in weak_j if k not in neut_j)
        zok = sum(vec[k] == "OK:0" for k in nonw_j)
        # controls: do-nothing instrument (flag iff the selftest result line changes) over the weakening variants
        dn = sum(vlines[k][1] != base[variants[k][0]][1] for k in range(len(variants)) if variants[k][1] in ("N", "W"))
        ok_v = vector(ALWAYS_OK)
        aok = sum(ok_v[k] == "WEAK:1" for k in weak_j)
        aw = [run.gate(ALWAYS_WEAK, base[i][0], kills_b[i].decode("utf-8"), False) for i in (0, 1)]
        sd_v = vector(SHA_DIFF)
        ctl_jobs = [(jb[0], jb[1], ctl_b[int(jb[0][1]) - 1].decode("utf-8"), jb[2] is not None and jb[3]) for jb in jobs]
        with ThreadPoolExecutor(a.workers) as ex:
            ctl_v = list(ex.map(lambda jb: run.gate(gate_t, jb[1], jb[2], jb[3]), ctl_jobs))
        ctl_h = sum(ctl_v[k] == "WEAK:1" for k in weak_j if k not in neut_j)
        singles = []
        for i in (0, 1):
            ss = set()
            for kk in kills[i].get("kills", []):
                mf = kk.get("must_fail")
                mf = [mf] if isinstance(mf, str) else (mf or [])
                if len(mf) == 1:
                    ss.add(mf[0])
            singles.append(sum(1 for lb in labels[i] if lb in ss))
        sd_zok = sum(sd_v[k] == "OK:0" for k in nonw_j)
        d = run.dir()
        gp = os.path.join(d, "gate.py")
        with open(gp, "w", encoding="utf-8") as fh:
            fh.write(gate_t)
        gs = subprocess.run([sys.executable, "-I", gp, "--selftest"], capture_output=True, text=True,
                            timeout=600, cwd=d, env={"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d})
        gs_ok = gs.returncode == 0
    finally:
        shutil.rmtree(root, ignore_errors=True)
    checks = base[0][2] + base[1][2]
    weak_total = len(weak_j)
    met = (gate_pin and all(kills_pin) and all(tool_pin) and all(p == "OK:0" for p in pos)
           and nflag == len(neut_j) and hflag == weak_total - len(neut_j) and zok == len(nonw_j)
           and dn < weak_total and aok < weak_total and all(v != "OK:0" for v in aw)
           and sd_zok < len(nonw_j) and gs_ok and ctl_h < weak_total - len(neut_j))
    word = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"MADO_SELFTEST_KILLS: {tag}{word} pred={PRED} rev={'draft' if draft else a.rev} "
          f"gate_pin={'ok' if gate_pin else 'FAIL'} "
          f"kills_pin={','.join('ok' if x else 'FAIL' for x in kills_pin)} tools=2 checks={checks} "
          f"positive={','.join(pos)} neutralised_flagged={nflag}/{len(neut_j)} "
          f"hand_flagged={hflag}/{weak_total - len(neut_j)} neutral_ok={zok}/{len(nonw_j)} "
          f"do_nothing_flagged={dn} always_ok_flagged={aok} "
          f"always_weak_positive={','.join(aw)} shadiff_neutral_ok={sd_zok}/{len(nonw_j)} "
          f"gate_selftest={'ok' if gs_ok else 'FAIL'} control_hand_flagged={ctl_h}/{weak_total - len(neut_j)} "
          f"singleton_labels={singles[0] + singles[1]}/{checks} "
          f"tool_pin={','.join('ok' if x else 'FAIL' for x in tool_pin)} "
          f"kill_paths={KILLS[0]},{KILLS[1]} gate_sha256={sha(gate_b)} "
          f"kills_sha256={sha(kills_b[0])},{sha(kills_b[1])}")
    if draft:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
