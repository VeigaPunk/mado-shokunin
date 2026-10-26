#!/usr/bin/env python3
"""MutC2V2Gates: single-edit mutation battery against PRED-C2-r41-v2's own gates.

Extracts the frozen v2 counter (byte-exact, from the v2 freeze), applies ONE
exact textual edit per mutant, and runs the committed control harness
(.ufo/waves/round-41/ctl/run-c2-v2-controls.py -- imported by path, never
edited) with its module-global COUNTER repointed at the mutant. A mutant is
NOTICED iff any committed control deviates from its expected verdict
(control=P must stay admitted=1/1; every mutant fixture must stay 0/1);
otherwise the mutant SURVIVES = coverage gap of the control battery.

Usage:
  python3 mutrun.py                # baseline + all mutants
  python3 mutrun.py --only NAME   # single mutant (reproduction)
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo", "waves", "round-41", "w2", "MutC2V2Gates")
FREEZE = "294c667901a8c7b7165ba849d03cba9a24c14fa4"
CTR_REL = "quality/counters/c2-r41-focus-entry-v2.py"
RUNNER = os.path.join(LANE, ".ufo", "waves", "round-41", "ctl",
                      "run-c2-v2-controls.py")
PRISTINE = os.path.join(SEAT, "c2-frozen-pristine.py")
MUTDIR = os.path.join(SEAT, "mutants")
TMPROOT = "/tmp/mutc2v2gates-tmp"
RESULTS = os.path.join(SEAT, "results.json")

# (name, gate attacked, old exact substring, new substring, predicted notice)
MUT = [
    ("M01-ghost-refusal-drop", "b ghost-id refusal",
     "and window == 0 and not ghosts)", "and window == 0)",
     "W03"),
    ("M02-window-refusal-drop", "b header window (source/verified-at/recheck past line 20)",
     "and window == 0 and not ghosts)", "and not ghosts)",
     "W04"),
    ("M03-min-ids-4-to-1", "b minimum 4 distinct sources",
     "int(len(ids) >= 4 and va", "int(len(ids) >= 1 and va",
     "none (survives)"),
    ("M04-verified-at-any", "b verified-at must equal OPENED",
     "cl[\"b\"] = int(len(ids) >= 4 and va == OPENED and recheck_ok(rc)",
     "cl[\"b\"] = int(len(ids) >= 4 and va is not None and recheck_ok(rc)",
     "N11"),
    ("M05-header-recheck-shape", "b header recheck validated",
     "and recheck_ok(rc)", "and (rc is not None)",
     "none (survives)"),
    ("M06-pin-check-drop", "d PINS trust root for NEW ids",
     "            pin_ok = True\n"
     "            if i in new_ids:\n"
     "                pin_ok = PINS.get(os.path.basename(path)) == digest \\\n"
     "                    and path == FETCH + os.path.basename(path)",
     "            pin_ok = True",
     "F1 F2 F3 F5 Z1"),
    ("M07-pin-path-drop", "d pinned receipt path must be FETCH+basename",
     "and path == FETCH + os.path.basename(path)", "and True",
     "F5"),
    ("M08-mode-accept-120000", "d receipt must be regular file (100644)",
     "and ls_mode(repo, rev, path) == \"100644\"",
     "and ls_mode(repo, rev, path) in (\"100644\", \"120000\")",
     "none predicted (W14 also pin-killed)"),
    ("M09-provenance-floor-8", "d receipt >= 512 bytes",
     "MIN_RECEIPT = 512", "MIN_RECEIPT = 8",
     "none (survives)"),
    ("M10-new-ids-3-to-1", "c at least 3 new ids",
     "cl[\"c\"] = int(rows_ok and len(new_ids) >= 3)",
     "cl[\"c\"] = int(rows_ok and len(new_ids) >= 1)",
     "N07"),
    ("M11-staged-drop-both", "i ADMIT/REFUSE name STAGED package files",
     "    staged_ok = lambda p: os.path.basename(p) in STAGED",
     "    staged_ok = lambda p: True",
     "A06 A07"),
    ("M12-staged-drop-refuse", "i REFUSE names STAGED package file",
     "    ref = [m for m in refuses if staged_ok(m.group(1))",
     "    ref = [m for m in refuses if True",
     "A07"),
    ("M13-quote-exclusivity-drop", "d quote in no OTHER cited receipt (2nd loop)",
     "        for j in receipts:", "        for j in []:",
     "none predicted (W15 also killed by seen_quote)"),
    ("M14-quote-binding-drop", "d quote occurs in its own receipt",
     "and nq in norm_receipt(blob)):", "and True):",
     "N04 W16 W17"),
    ("M15-sha-binding-drop", "d receipt sha256 equals GATE sha256",
     "and hashlib.sha256(blob).hexdigest() == digest", "and True",
     "N03"),
    ("M16-quote-word-window", "d quote 3-25 words",
     "and 3 <= len(quote.split()) <= 25",
     "and 1 <= len(quote.split()) <= 999",
     "N05"),
    ("M17-sessions-floor-1", "h >= 2 sessions",
     "jc[0] >= 2", "jc[0] >= 1",
     "J02 if its tail keeps a boot line"),
    ("M18-adverts-floor-8", "h >= 40 adverts",
     "jc[1] >= 40", "jc[1] >= 8",
     "none (survives)"),
    ("M19-distinct-floor-2", "h >= 20 distinct interfaces",
     "jc[2] >= 20", "jc[2] >= 2",
     "none (survives)"),
    ("M20-ascending-drop", "h session firsts distinct and ascending",
     "and jc[3] >= 1 and jc[4] and jc[5])", "and jc[3] >= 1 and jc[4])",
     "J17"),
    ("M21-loglevel-loosen", "h ADVERT grammar [LOG] only",
     "\\[LOG\\]  \\|", "(?:\\[LOG\\]|\\[ERR\\])  \\|",
     "J11"),
    ("M22-census-anchor-drop", "h census line anchored",
     "JOURNAL_RE = re.compile(r\"^journal sessions=",
     "JOURNAL_RE = re.compile(r\"journal sessions=",
     "X03"),
    ("M23-cited-case-drop", "b ghost scan covers lowercase ids",
     "cited = set(re.findall(r\"\\b[Ss]\\d{3,}\\b\", \"\\n\".join(lines)))",
     "cited = set(re.findall(r\"\\bS\\d{3,}\\b\", \"\\n\".join(lines)))",
     "W02"),
    ("M24-window-20-to-200", "b 20-line header window",
     "            if k < 20:", "            if k < 200:",
     "W01 W04"),
    ("M25-clause-e-drop", "e location uniqueness + receipt-name kinship",
     "cl[\"e\"] = int(e_ok and bool(new_ids))",
     "cl[\"e\"] = int(bool(new_ids))",
     "N09 W13"),
    ("M26-admit-drop", "i ADMIT line required",
     "cl[\"i\"] = int(bool(adm) and bool(ref) and not bad)",
     "cl[\"i\"] = int(bool(ref) and not bad)",
     "A01 A03"),
    ("M27-badloc-drop", "i BAD_LOC localized-channel scan",
     "bad |= any(b_ in row_text for b_ in BAD_LOC)", "bad |= False",
     "A05 F4"),
    ("M28-refuse-target-distinct-drop", "i REFUSE target != every ADMIT target",
     "and all(m.group(1) != a.group(1) for a in adm)]", "]",
     "A08"),
    ("M29-reason-floor-1", "i REFUSE reason >= 4 distinct words",
     "and len(set(m.group(2).lower().split())) >= 4",
     "and len(set(m.group(2).lower().split())) >= 1",
     "A04 A09"),
    ("M30-usedby-drop", "c used-by lists the entry",
     "good = cells[7] == \"mined\" and entry in items \\",
     "good = cells[7] == \"mined\" and True \\",
     "N16 W10 X05"),
    ("M31-held-byte-eq-drop", "c held row cells 1-9 byte-equal to BASE",
     "and old[0][:9] == cells[:9] and recheck_ok(cells[9]) is not None",
     "and recheck_ok(cells[9]) is not None",
     "N08"),
    ("M32-status-drop", "c status mined",
     "good = cells[7] == \"mined\" and entry", "good = True and entry",
     "N13"),
    ("M33-opened-drop", "c new id opened 2026-10-25",
     "good &= cells[8] == OPENED and (\"/\" in loc and \".\" in loc)",
     "good &= \"/\" in loc and \".\" in loc",
     "X14"),
    ("M34-index-ge-1", "f exactly one index row",
     "if pat.match(l)) == 1)", "if pat.match(l)) >= 1)",
     "none predicted (X07 has zero unfenced rows)"),
    ("M35-dup-rows-allowed", "c exactly one registry row per id",
     "if len(rows) != 1 or len(rows[0]) != 11:",
     "if len(rows) < 1 or len(rows[0]) != 11:",
     "none (survives)"),
    ("M36-base-precond-drop", "main precondition entry absent at BASE",
     "        if show(repo, base, e) is not None:\n"
     "            raise Setup(\"precondition_failed entry_present_at_base %s\" % e)",
     "        pass",
     "none (survives)"),
    ("M37-opened-const-shift", "OPENED constant (over-strict probe)",
     "OPENED = \"2026-10-25\"", "OPENED = \"2026-10-26\"",
     "control=P fails (over-strict)"),
]


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def extract_pristine():
    out = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (FREEZE, CTR_REL)],
                         capture_output=True, check=True).stdout
    with open(PRISTINE, "wb") as fh:
        fh.write(out)
    wt = open(os.path.join(LANE, CTR_REL), "rb").read()
    return out, wt


def build_mutants(src):
    made = []
    for name, gate, old, new, pred in MUT:
        n = src.count(old.encode())
        if n != 1:
            raise SystemExit("MUTANT %s: old substring count=%d (need 1)"
                             % (name, n))
        mut = src.replace(old.encode(), new.encode(), 1)
        try:
            compile(mut, name, "exec")
        except SyntaxError as exc:
            raise SystemExit("MUTANT %s: syntax error %s" % (name, exc))
        path = os.path.join(MUTDIR, name + ".py")
        with open(path, "wb") as fh:
            fh.write(mut)
        made.append({"name": name, "gate": gate, "predicted": pred,
                     "path": path, "sha256": hashlib.sha256(mut).hexdigest(),
                     "delta_bytes": len(mut) - len(src)})
    return made


def run_one(tag, counter_path):
    """Run the committed harness once with COUNTER repointed; return report."""
    os.makedirs(TMPROOT, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="run-", dir=TMPROOT)
    tempfile.tempdir = scratch
    t0 = time.time()
    modname = "c2ctl_%d_%d" % (os.getpid(), int(time.time() * 1000) % 100000)
    spec = importlib.util.spec_from_file_location(modname, RUNNER)
    mod = importlib.util.module_from_spec(spec)
    buf = io.StringIO()
    try:
        spec.loader.exec_module(mod)
        mod.COUNTER = counter_path
        with contextlib.redirect_stdout(buf):
            rc = mod.main()
        status, err = rc, None
    except Exception as exc:  # noqa: BLE001 - record any harness/counter crash
        status, err = "CRASH", "%s: %s" % (type(exc).__name__, exc)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    out = buf.getvalue()
    failing = [l for l in out.splitlines()
               if l.startswith("control=") and l.endswith("ok=0")]
    summary = next((l for l in out.splitlines()
                    if l.startswith("CTL_C2V2:")), "NO-SUMMARY")
    return {"tag": tag, "status": status, "error": err, "seconds": round(
        time.time() - t0, 1), "failing": failing, "summary": summary,
        "tail": out.strip().splitlines()[-4:]}


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    os.makedirs(MUTDIR, exist_ok=True)
    src, wt = extract_pristine()
    same = src == wt
    pre = {"freeze": FREEZE, "counter_rel": CTR_REL,
           "frozen_sha256": hashlib.sha256(src).hexdigest(),
           "worktree_sha256": hashlib.sha256(wt).hexdigest(),
           "worktree_equals_freeze": same,
           "runner_sha256": sha256_file(RUNNER),
           "frozen_bytes": len(src)}
    print("PRISTINE", json.dumps(pre))

    made = build_mutants(src)
    print("MUTANTS-BUILT", len(made))

    jobs = [("BASELINE-pristine", PRISTINE)]
    jobs += [(m["name"], m["path"]) for m in made if only in (None, m["name"])]
    results = []
    with ProcessPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(run_one, tag, path) for tag, path in jobs]
        for fut in futs:
            results.append(fut.result())

    base = results[0]
    base_ok = base["status"] == 0 and not base["failing"]
    print("BASELINE", "OK" if base_ok else "FAILED",
          base["summary"], "%.1fs" % base["seconds"])
    verdicts = []
    for r in results[1:]:
        if r["status"] == "CRASH":
            verdict = "NOTICED-CRASH"
        elif base_ok and r["status"] == 0 and not r["failing"]:
            verdict = "SURVIVED"
        elif base_ok:
            verdict = "NOTICED"
        else:
            verdict = "INCONCLUSIVE"
        r["verdict"] = verdict
        verdicts.append(r)
        print("RESULT %-34s %-13s %s | noticed-by: %s" % (
            r["tag"], verdict, r["summary"],
            "; ".join(x.split(" expected=")[0] for x in r["failing"]) or "-"))

    # restoration evidence: nothing tracked may have changed
    post = {"counter_sha256": sha256_file(os.path.join(LANE, CTR_REL)),
            "runner_sha256": sha256_file(RUNNER),
            "pristine_copy_sha256": sha256_file(PRISTINE)}
    post["counter_unchanged"] = post["counter_sha256"] == pre["worktree_sha256"]
    post["runner_unchanged"] = post["runner_sha256"] == pre["runner_sha256"]
    print("POST", json.dumps(post))

    with open(RESULTS, "w") as fh:
        json.dump({"pre": pre, "post": post, "baseline_ok": base_ok,
                   "mutants": made, "runs": results}, fh, indent=1)
    shutil.rmtree(TMPROOT, ignore_errors=True)
    return 0 if base_ok else 2


if __name__ == "__main__":
    sys.exit(main())
