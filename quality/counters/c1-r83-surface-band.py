#!/usr/bin/env python3
"""mado — PRED-C1-r83-v1: score every declared surface's client-allocation band.

Scores `tools/mado-barfoot.py` (the r83 generation) over a frozen case set: the
forty-seven round-82 cases carried unchanged plus eight cases on the class round 82 refused —
a *second* declared layer surface whose band axis is dynamic (`height = 0` on a horizontal
surface, `width = 0` on a vertical one). Round 82 resolved only the bar's band; round 83
resolves every declared surface's band from the same `--allocation` map, and refuses a
dynamic band that has no entry. Each case supplies a waybar config, a layers reply, a
monitors reply, an optional surfaces declaration and an optional allocation map; the counter
writes them into the caller's scratch root, runs the tool from the measured revision's bytes,
and compares its RESULT (and its ATTR lines) against expectations derived from the
layer-shell protocol's zero-size clause (S481), gtk-layer-shell `layer-surface.c:276`/`:282`
(S464) and Hyprland `Renderer.cpp`'s arrange/applyExclusive arithmetic — never from a tool
run.

Contract: MADO_R83_BARFOOT: cases=58 correct=58 mutants=38 killed=38 base_correct=52/58
carried=47/47 tool_selftest=p/n verdict=TARGET_MET rev=<hash> tool_sha256=<sha>
(rc 0 iff every clause holds).

Exit map: 0 target met · 1 target missed · 2 setup error (never a verdict).
Writes only inside the caller's scratch root; removes its generation directory.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CASES = 58
CARRIED = 47
MUTANTS = 39
BASE_EXPECT = 52

MUTATIONS = [
    ("opposite-margin-dropped",
     '    contribution = (extent + bar["margins"][OPPOSITE_EDGE[edge]]) if contained else 0',
     '    contribution = extent if contained else 0'),
    ("horizontal-margin-leak",
     '    contribution = (extent + bar["margins"][OPPOSITE_EDGE[edge]]) if contained else 0',
     '    contribution = (extent + bar["margins"]["left"] + bar["margins"]["right"]) '
     'if contained else 0'),
    ("level-bottom-swap",
     'LEVEL = {"background": 0, "bottom": 1, "top": 2, "overlay": 3}',
     'LEVEL = {"background": 0, "bottom": 2, "top": 2, "overlay": 3}'),
    ("right-extent-flip",
     '    return (usable["x"] + usable["w"]) - box["x"]',
     '    return (box["x"] - usable["x"]) + box["w"]'),
    ("per-side-margin-dropped",
     'sides[side] = value if isinstance(value, int) and not isinstance(value, bool) else 0',
     'sides[side] = 0'),
    ("negative-margin-accepted",
     'if any(value < 0 for value in margins.values()):',
     'if False:'),
    ("opposite-edge-wrong",
     'OPPOSITE_EDGE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}',
     'OPPOSITE_EDGE = {"top": "top", "bottom": "bottom", "left": "left", "right": "right"}'),
    ("static-dropped",
     '    expected = static[edge] + contribution',
     '    expected = contribution'),
    ("static-order-swapped",
     '            area = dict(zip(STATIC_SIDES, (max(0, int(v)) for v in values)))',
     '            area = dict(zip(("bottom", "top", "left", "right"), '
     '(max(0, int(v)) for v in values)))'),
    ("static-first-wins",
     '            slot = area if slot is not None else dict(ZERO_STATIC)',
     '            slot = dict(slot) if slot is not None else dict(ZERO_STATIC)'),
    ("static-box-unoffset",
     '    box = {"x": local["x"] + usable["x"], "y": local["y"] + usable["y"],',
     '    box = {"x": local["x"], "y": local["y"],'),
    ("static-selector-ignored",
     '        if selector != monitor:\n            continue',
     '        if False:\n            continue'),
    ("attr-edge-order",
     '    ("top", ANCHOR["top"], ANCHOR["left"] | ANCHOR["right"] | ANCHOR["top"]),',
     '    ("bottom", ANCHOR["top"], ANCHOR["left"] | ANCHOR["right"] | ANCHOR["top"]),'),
    ("running-bounds-ignored",
     '        if spec["exclusive"] == -1:\n            bounds = dict(full)\n        else:\n'
     '            bounds = dict(usable)',
     '        if spec["exclusive"] == -1:\n            bounds = dict(full)\n        else:\n'
     '            bounds = dict(original)'),
    ("exclusive-edge-ignored",
     '        if ((spec["exclusiveEdge"] == singular or spec["anchor"] == singular',
     '        if ((False or spec["anchor"] == singular'),
    ("edge-guard-dropped",
     '             or spec["anchor"] == triplet) and zone + spec["margins"][edge] > 0):',
     '             or spec["anchor"] == triplet)):'),
    ("invalid-area-kept",
     '    ls_valid = (usable["w"] > 0 and usable["h"] > 0 and contains_box(original, usable))',
     '    ls_valid = True'),
    ("full-box-uses-usable",
     '        if spec["exclusive"] == -1:\n            bounds = dict(full)\n',
     '        if spec["exclusive"] == -1:\n            bounds = dict(usable)\n'),
    ("empty-box-contributes",
     '        if box["w"] <= 0 or box["h"] <= 0:',
     '        if False:'),
    ("same-level-order-ignored",
     '                   key=lambda i: (surfaces[i]["level"], -surfaces[i]["order"], i))',
     '                   key=lambda i: (surfaces[i]["level"], i))'),
    ("zone-margin-not-added",
     '                amount = zone + spec["margins"][edge]',
     '                amount = zone'),
    ("attribution-not-summed",
     '        amount for (namespace, hit), amount in attribution.items() if hit == edge)',
     '        amount for (namespace, hit), amount in attribution.items() if False)'),
    ("tie-round-trunc",
     '    return math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)',
     '    return math.trunc(value)'),
    ("round-width-spec",
     '    nw = box["x"] + box["w"] - rx',
     '    nw = box["w"]'),
    ("auto-gate-open",
     '    # gtk-layer-shell sends no zone for a corner, a parallel pair or all four anchors\n'
     '    return 0',
     '    return spec["height"] + spec["margins"]["bottom"]'),
    ("auto-gate-and",
     '    if vert and not horiz:',
     '    if vert and horiz:'),
    ("auto-axis-swapped",
     '        zone = spec["width"]',
     '        zone = spec["height"]'),
    ("auto-dynamic-kept",
     '        if spec["height"] == 0:',
     '        if False:'),
    ("alloc-explicit-overridden",
     '    if spec[axis] > 0:\n        return spec[axis]',
     '    if False:\n        return spec[axis]'),
    ("alloc-zero-accepted",
     '    if band <= 0:\n        raise Unmodelled(',
     '    if band < 0:\n        raise Unmodelled('),
    ("alloc-axis-lost",
     '    height = band_of(bar, allocation) if pos in ("top", "bottom") else bar["height"]',
     '    height = bar["height"] if pos in ("top", "bottom") else bar["height"]'),
    ("alloc-negative-accepted",
     '        if value < 0:\n            raise Setup("the allocation for %r is negative" % name)',
     '        if False:\n            raise Setup("the allocation for %r is negative" % name)'),
    ("alloc-unknown-kept",
     '    unknown = sorted(set(allocation) - {bar["namespace"]})',
     '    unknown = []'),
    ("alloc-width-lost",
     '    width = band_of(bar, allocation) if pos in ("left", "right") else bar["width"]',
     '    width = bar["width"]'),
    ("box-verdict-blind",
     '            boxes.append("MATCH" if live_box == box else "DIFFER")',
     '            boxes.append("MATCH")'),
    ("box-verdict-blind-single",
     '    box_verdict = "MATCH" if live_box == box else "DIFFER"',
     '    box_verdict = "MATCH"'),
    ("extra-alloc-ignored",
     '        if spec[axis] == 0 and (spec["namespace"] in allocation or spec is bar_spec):',
     '        if False:'),
    ("bar-band-no-refusal",
     '        if spec[axis] == 0 and (spec["namespace"] in allocation or spec is bar_spec):',
     '        if spec[axis] == 0 and spec["namespace"] in allocation:'),
    ("alloc-resolved-set-bar-only",
     '    resolved = {bar["namespace"]} | {s["namespace"] for s in extras}',
     '    resolved = {bar["namespace"]}'),
]


class Setup(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, cwd, timeout=60):
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "LC_ALL": "C",
        "LANG": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
        # the tool's selftest uses tempfile; keep its throwaway dir inside caller scratch
        "TMPDIR": cwd,
    }
    try:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout, stdin=subprocess.DEVNULL)
        return (proc.returncode, proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        raise Setup("cannot run child: %s" % exc)


RESULT_RE = re.compile(
    r"^MADO_BARFOOT_RESULT: monitor=\S+ box=(\S+)"
    r"(?: boxes=(\S+))?"
    r"(?: reserved=(\S+))?"
    r"(?: band=(-?\d+) expected=(-?\d+))?"
    r"(?: attributed=(-?\d+))?"
    r"(?: gt=(-?[\d,]+))?"
    r"(?: attr=(-?[\d,]+))?"
    r"(?: ls=(\S+))?"
    r".*?verdict=(\S+)\s*$", re.M)

ATTR_RE = re.compile(
    r"^MADO_BARFOOT_ATTR: monitor=\S+ level=\d+ ns=(\S+) edge=(\S+) contribution=(-?\d+)", re.M)


def parse_result(stdout):
    """Every field the RESULT line can carry; absent fields are None."""
    m = RESULT_RE.search(stdout)
    if not m:
        return None
    box, boxes, reserved, band, expected, attributed, gt, attr, ls, verdict = m.groups()
    return {
        "box": box,
        "boxes": boxes,
        "reserved": reserved,
        "band": int(band) if band is not None else None,
        "expected": int(expected) if expected is not None else None,
        "attributed": int(attributed) if attributed is not None else None,
        "gt": gt,
        "attr": attr,
        "ls": ls,
        "verdict": verdict,
    }


def parse_attr(stdout):
    return dict((m.group(1), "%s:%s" % (m.group(2), m.group(3)))
                for m in ATTR_RE.finditer(stdout))


def case_files(case, outdir):
    os.makedirs(outdir, exist_ok=True)
    cfg = os.path.join(outdir, "config.json")
    with open(cfg, "w") as fh:
        json.dump(case["config"], fh)
    layers = os.path.join(outdir, "layers.json")
    if "layers_raw" in case:
        with open(layers, "w") as fh:
            fh.write(case["layers_raw"])
    else:
        with open(layers, "w") as fh:
            json.dump(case["layers"], fh)
    monitors = os.path.join(outdir, "monitors.json")
    with open(monitors, "w") as fh:
        json.dump(case["monitors"], fh)
    rules = None
    if "rules" in case:
        rules = os.path.join(outdir, "rules.conf")
        with open(rules, "w") as fh:
            fh.write(case["rules"])
    surfaces = None
    if "surfaces" in case:
        surfaces = os.path.join(outdir, "surfaces.json")
        with open(surfaces, "w") as fh:
            json.dump(case["surfaces"], fh)
    allocation = None
    if "allocation" in case:
        allocation = os.path.join(outdir, "allocation.json")
        with open(allocation, "w") as fh:
            json.dump(case["allocation"], fh)
    return cfg, layers, monitors, rules, surfaces, allocation


def expected_ok(case, rc, stdout):
    exp = case["expect"]
    if exp.get("error"):
        # a refusal pins its stage: a setup error must not satisfy a model refusal
        stage = exp.get("stage", "model")
        return rc == exp["rc"] and ("ERROR (stage=%s " % stage) in stdout
    got = parse_result(stdout)
    if got is None:
        return False
    got["rc"] = rc
    for key, want in exp.items():
        if key in ("error", "stage"):
            continue
        if key == "attr_ns":
            if parse_attr(stdout) != want:
                return False
            continue
        if got.get(key) != want:
            return False
    return True


def run_cases(tool, cases, workroot, label):
    correct = 0
    rows = []
    for index, case in enumerate(cases):
        outdir = os.path.join(workroot, "%s-%02d" % (label, index))
        cfg, layers, monitors, rules, surfaces, allocation = case_files(case, outdir)
        argv = [sys.executable, "-I", tool, "--config", cfg, "--layers", layers,
                "--monitors", monitors]
        if rules:
            argv += ["--rules", rules]
        if surfaces:
            argv += ["--surfaces", surfaces]
        if allocation:
            argv += ["--allocation", allocation]
        if case.get("monitor"):
            argv += ["--monitor", case["monitor"]]
        rc, stdout, stderr = run(argv, outdir)
        ok = expected_ok(case, rc, stdout)
        correct += 1 if ok else 0
        got = parse_result(stdout) or {}
        rows.append((case["name"], rc, got.get("box"), got.get("reserved"),
                     got.get("band"), got.get("expected"), got.get("verdict"), ok))
    return correct, rows


def apply_mutation(source, anchor, replacement, name):
    count = source.count(anchor)
    if count != 1:
        raise Setup("mutant %s anchor occurs %d times, not once" % (name, count))
    return source.replace(anchor, replacement)


def selftest():
    checks = total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_R83_BARFOOT_SELFTEST_FAIL: %s" % label)

    single = ("MADO_BARFOOT_RESULT: monitor=M1 box=MATCH reserved=EQ band=34 expected=34 "
              "verdict=CLEAN\n")
    got = parse_result(single)
    ok(got["box"] == "MATCH" and got["band"] == 34 and got["expected"] == 34
       and got["reserved"] == "EQ" and got["verdict"] == "CLEAN"
       and got["attributed"] is None and got["boxes"] is None,
       "parse the single-surface result")
    case = {"name": "self", "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 34,
                                       "expected": 34, "verdict": "CLEAN"}}
    ok(expected_ok(case, 0, single), "carried expectation accepted")
    ok(not expected_ok(case, 0, single.replace("band=34", "band=30")), "band mismatch refused")
    ok(not expected_ok(case, 0, single.replace("reserved=EQ", "reserved=GT")),
       "reserved mismatch refused")
    ok(not expected_ok(case, 0, single.replace("verdict=CLEAN", "verdict=DIFFER")),
       "verdict mismatch refused")

    composed = ("MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 "
                "box=0,0,1000,26\n"
                "MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=40 "
                "box=0,26,1000,40\n"
                "MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ "
                "band=66 expected=66 attributed=66 gt=0,66,0,0 attr=0,66,0,0 ls=VALID "
                "verdict=CLEAN\n")
    got = parse_result(composed)
    ok(got["boxes"] == "MATCH,MATCH" and got["attributed"] == 66 and got["attr"] == "0,66,0,0"
       and got["gt"] == "0,66,0,0" and got["ls"] == "VALID", "parse the composition result")
    ok(parse_attr(composed) == {"waybar": "top:26", "panel": "top:40"}, "parse ATTR lines")
    comp_case = {"name": "comp", "expect": {
        "rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ", "band": 66,
        "expected": 66, "attributed": 66, "gt": "0,66,0,0", "attr": "0,66,0,0",
        "ls": "VALID", "verdict": "CLEAN",
        "attr_ns": {"waybar": "top:26", "panel": "top:40"}}}
    ok(expected_ok(comp_case, 0, composed), "composition expectation accepted")
    ok(not expected_ok(comp_case, 0, composed.replace("attr=0,66,0,0", "attr=0,26,0,0")),
       "an attribution vector mismatch is refused")
    ok(not expected_ok(comp_case, 0,
                       composed.replace("ns=panel edge=top contribution=40",
                                        "ns=panel edge=top contribution=26")),
       "a per-surface attribution mismatch is refused")
    invalid = composed.replace("band=66 expected=66 attributed=66", "band=0 expected=0 attributed=2026") \
                      .replace("ls=VALID", "ls=INVALID")
    ok(expected_ok({"name": "inv", "expect": {"rc": 0, "band": 0, "expected": 0,
                                              "attributed": 2026, "ls": "INVALID"}}, 0, invalid),
       "the invalid-area shape is accepted where the case declares it")
    ok(not expected_ok({"name": "inv", "expect": {"ls": "VALID"}}, 0, invalid),
       "an invalid layer area is refused where the case expects a valid one")
    ok(expected_ok({"expect": {"error": True, "rc": 3, "stage": "model"}}, 3,
                   "MADO_BARFOOT: ERROR (stage=model x)\n"), "model refusal accepted")
    ok(not expected_ok({"expect": {"error": True, "rc": 3, "stage": "model"}}, 2,
                       "MADO_BARFOOT: ERROR (stage=setup x)\n"),
       "a setup error never satisfies a model refusal")
    ok(not expected_ok({"expect": {"error": True, "rc": 3}}, 0,
                       "MADO_BARFOOT: ERROR (stage=model x)\n"), "refusal rc mismatch refused")
    for name, anchor, repl in MUTATIONS:
        src = "a\n" + anchor + "\nb\n"
        ok(apply_mutation(src, anchor, repl, name) == "a\n" + repl + "\nb\n", "anchor %s" % name)
        try:
            apply_mutation("a\nb\n", anchor, repl, name)
            ok(False, "missing anchor refused %s" % name)
        except Setup:
            ok(True, "missing anchor refused %s" % name)
    ok(sha256(b"x") == sha256(b"x") and len(sha256(b"x")) == 64, "sha256 stable")
    print("MADO_R83_BARFOOT_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def extract(repo, rev, path, outdir):
    rc, source, err = run(["git", "-C", repo, "show", rev + ":" + path], outdir)
    if rc != 0:
        raise Setup("cannot extract %s at %s: %s" % (path, rev, err.strip()))
    return source


def resolve(repo, rev):
    rc, out, err = run(["git", "-C", repo, "rev-parse", rev], repo)
    full = out.strip()
    if rc != 0 or not full:
        raise Setup("cannot resolve revision %r" % rev)
    return full


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--controls")
    ap.add_argument("--carried")
    ap.add_argument("--scratch-root")
    ap.add_argument("--no-mutants", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.repo and args.rev and args.base_rev and args.controls and args.carried
            and args.scratch_root):
        print("MADO_R83_BARFOOT: ERROR (stage=setup usage)")
        return 2
    workroot = None
    try:
        repo = os.path.abspath(args.repo)
        if args.scratch_root == "/":
            raise Setup("refusing / as the scratch root")
        if os.path.islink(args.scratch_root):
            raise Setup("refusing a symlinked scratch root")
        os.makedirs(args.scratch_root, exist_ok=True)
        if not os.path.isdir(args.scratch_root):
            raise Setup("scratch root is not a directory")
        workroot = tempfile.mkdtemp(prefix="c1-r82-", dir=args.scratch_root)
        rev_full = resolve(repo, args.rev)
        base_full = resolve(repo, args.base_rev)

        source = extract(repo, args.rev, "tools/mado-barfoot.py", workroot)
        tool_path = os.path.join(workroot, "mado-barfoot.py")
        with open(tool_path, "w") as fh:
            fh.write(source)
        tool_sha = sha256(source.encode())

        base_source = extract(repo, args.base_rev, "tools/mado-barfoot.py", workroot)
        base_tool = os.path.join(workroot, "mado-barfoot-base.py")
        with open(base_tool, "w") as fh:
            fh.write(base_source)

        with open(args.controls) as fh:
            control = json.load(fh)
        cases = control["cases"]
        if len(cases) != CASES:
            raise Setup("control set carries %d cases, frozen target expects %d"
                        % (len(cases), CASES))
        with open(args.carried) as fh:
            carried = json.load(fh)["cases"]
        if len(carried) != CARRIED:
            raise Setup("carried set carries %d cases, frozen target expects %d"
                        % (len(carried), CARRIED))
        carried_ok = cases[:CARRIED] == carried
        if not carried_ok:
            raise Setup("the successor set does not carry the frozen round-82 cases unchanged")
        control_sha = sha256(open(args.controls, "rb").read())

        rc, out, _ = run([sys.executable, "-I", tool_path, "--selftest"], workroot)
        m = re.search(r"MADO_BARFOOT_SELFTEST: (\d+)/(\d+)", out)
        tool_selftest = "%s/%s" % (m.group(1), m.group(2)) if m else "0/0"
        selftest_ok = (rc == 0 and m is not None and int(m.group(1)) > 0
                       and m.group(1) == m.group(2))

        correct, rows = run_cases(tool_path, cases, workroot, "cand")
        for name, crc, box, reserved, band, expected, verdict, ok in rows:
            print("MADO_R83_CASE: name=%s rc=%d box=%s reserved=%s band=%s expected=%s "
                  "verdict=%s correct=%s"
                  % (name, crc, box, reserved, band, expected, verdict, "yes" if ok else "no"))

        killed = 0
        skipped = bool(args.no_mutants)
        for name, anchor, repl in (() if skipped else MUTATIONS):
            try:
                mutated = apply_mutation(source, anchor, repl, name)
            except Setup:
                print("MADO_R83_MUTANT: name=%s correct=0/%d killed=no reason=anchor-absent"
                      % (name, CASES))
                continue
            mutant_path = os.path.join(workroot, "mutant-%s.py" % name)
            with open(mutant_path, "w") as fh:
                fh.write(mutated)
            mcorrect, _ = run_cases(mutant_path, cases, workroot, "mut-" + name)
            dead = mcorrect < CASES
            killed += 1 if dead else 0
            print("MADO_R83_MUTANT: name=%s correct=%d/%d killed=%s"
                  % (name, mcorrect, CASES, "yes" if dead else "no"))
        if skipped:
            # --no-mutants is diagnostic: the kill clause is not exercised, never claimed
            print("MADO_R83_MUTANT: skipped=yes reason=--no-mutants (the kill clause is not "
                  "claimed by this run)")

        base_correct, base_rows = run_cases(base_tool, cases, workroot, "base")
        print("MADO_R83_BASE: correct=%d/%d rule=held-r82-model(bar-band-only) "
              "base_rev=%s base_sha256=%s"
              % (base_correct, CASES, base_full, sha256(base_source.encode())))
        print("MADO_R83_CONTROL: sha256=%s carried=%d/%d"
              % (control_sha, CARRIED if carried_ok else 0, CARRIED))
        if skipped:
            print("MADO_R83_BARFOOT: cases=%d correct=%d mutants=0 killed=0 base_correct=%d/%d "
                  "carried=%d/%d tool_selftest=%s verdict=MUTANTS_SKIPPED rev=%s "
                  "tool_sha256=%s"
                  % (CASES, correct, base_correct, CASES,
                     CARRIED if carried_ok else 0, CARRIED, tool_selftest, rev_full, tool_sha))
            return 0
        target = (correct == CASES and killed == MUTANTS and base_correct == BASE_EXPECT
                  and carried_ok and selftest_ok)
        print("MADO_R83_BARFOOT: cases=%d correct=%d mutants=%d killed=%d base_correct=%d/%d "
              "carried=%d/%d tool_selftest=%s verdict=%s rev=%s tool_sha256=%s"
              % (CASES, correct, MUTANTS, killed, base_correct, CASES,
                 CARRIED if carried_ok else 0, CARRIED, tool_selftest,
                 "TARGET_MET" if target else "TARGET_MISSED", rev_full, tool_sha))
        return 0 if target else 1
    except Setup as exc:
        print("MADO_R83_BARFOOT: ERROR (stage=setup %s)" % exc)
        return 2
    finally:
        if workroot:
            shutil.rmtree(workroot, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
