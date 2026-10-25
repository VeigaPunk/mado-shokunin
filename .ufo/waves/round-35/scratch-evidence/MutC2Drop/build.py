#!/usr/bin/env python3
"""Build MutC2Drop mutants + fixtures for PRED-C2-r35-v1.

Contract: writes mutants m01..m24.py and fixtures/f*/ under this directory.
Every mutant is produced by exactly one exact-string replacement; the script
asserts each replacement applied and emits `diff -u` hunks for the report.
Run: python3 build.py
"""
import difflib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
SCRATCH = ROOT / ".ufo/waves/round-35/scratch/MutC2Drop"
SRC = (ROOT / ".ufo/waves/round-35/c2/count.py").read_text()

# name -> (old, new, description). Each applied exactly once, asserted.
MUTANTS = [
    ("m01-frozen-missing",
     '    if not frozen_path.is_file():\n        die("frozen-missing")',
     '    # dropped: frozen-missing guard',
     "drop frozen_path.is_file() guard"),
    ("m02-predicate-drift",
     '    if spec.get("predicate") != PREDICATE:\n        die("predicate-drift")',
     '    # dropped: predicate-drift guard',
     "drop predicate == PREDICATE check"),
    ("m03-target-drift",
     '    if spec.get("target") != EXPECTED_TARGET:\n        die("target-drift")',
     '    # dropped: target-drift guard',
     "drop target == EXPECTED_TARGET check"),
    ("m04-ledger-missing",
     '    if not ledger_path.is_file():\n        die("clause-ledger-missing")',
     '    # dropped: clause-ledger-missing guard',
     "drop clause-ledger is_file guard"),
    ("m05-nl-skip",
     "        nl = clause.get(\"not-load-bearing\")\n        if nl and nl.get(\"reason\"):\n            continue\n",
     "",
     "drop not-load-bearing+reason exemption"),
    ("m06-bare-clause",
     "        if not control:\n            uncovered += 1\n            continue",
     "        if not control:\n            continue  # dropped: bare clause counts as covered",
     "drop 'no control => uncovered' check"),
    ("m07-receipt-exists",
     "        if not receipt.is_file() or not MISSED.search(receipt.read_text()):",
     "        if not MISSED.search(receipt.read_text()):",
     "drop receipt.is_file() disjunct"),
    ("m08-receipt-missed",
     "        if not receipt.is_file() or not MISSED.search(receipt.read_text()):",
     "        if not receipt.is_file():",
     "drop MISSED.search disjunct"),
    ("m09-retired-absent",
     "        if clause[\"id\"] not in live_ids:",
     "        if True:  # dropped: retired id must be absent from live",
     "drop 'retired id absent from live' check"),
    ("m10-toctou-exact",
     "    toctou_declared = 1 if declared == [spec[\"toctou_clause\"]] else 0",
     "    toctou_declared = 1 if declared else 0  # dropped: exact singleton identity",
     "drop declared == [toctou_clause] equality"),
    ("m11-blobledger-exists",
     "    if ledger_doc.is_file():\n        text = ledger_doc.read_text()\n        if spec[\"r34_tip\"] in text:",
     "    if True:  # dropped: blob-ledger is_file guard\n        text = ledger_doc.read_text()\n        if spec[\"r34_tip\"] in text:",
     "drop blob-ledger is_file guard"),
    ("m12-tip-in-ledger",
     "        if spec[\"r34_tip\"] in text:",
     "        if True:  # dropped: r34 tip must appear in ledger text",
     "drop 'tip named in ledger doc' check"),
    ("m13-revparse-try",
     "                try:\n                    raw = subprocess.run(\n                        [\"git\", \"-C\", str(repo), \"rev-parse\", rev_path],\n                        capture_output=True,\n                        check=True,\n                        text=True,\n                    ).stdout.strip()\n                except subprocess.CalledProcessError:\n                    ok = False\n                    break",
     "                raw = subprocess.run(\n                    [\"git\", \"-C\", str(repo), \"rev-parse\", rev_path],\n                    capture_output=True,\n                    check=True,\n                    text=True,\n                ).stdout.strip()  # dropped: CalledProcessError catch",
     "drop rev-parse failure catch"),
    ("m14-blob-id-eq",
     "                if raw != blob[\"blob_id\"]:\n                    ok = False\n                    break",
     "                # dropped: blob id equality check",
     "drop rev-parse result == blob_id check"),
    ("m15-declared-reason",
     "    declared = [c[\"id\"] for c in live if (c.get(\"not-load-bearing\") or {}).get(\"reason\")]",
     "    declared = [c[\"id\"] for c in live if c.get(\"not-load-bearing\")]  # dropped: reason required",
     "drop 'reason' requirement in declared collection"),
    ("m16-nl-reason",
     "        if nl and nl.get(\"reason\"):\n            continue",
     "        if nl:\n            continue  # dropped: declaration must carry a reason",
     "drop 'reason' requirement in uncovered exemption"),
    ("m17-met-uncovered",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET if k != \"uncovered\")",
     "drop uncovered term from verdict conjunction"),
    ("m18-met-retired",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET if k != \"retired\")",
     "drop retired term from verdict conjunction"),
    ("m19-met-toctou",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET if k != \"toctou_declared\")",
     "drop toctou_declared term from verdict conjunction"),
    ("m20-met-tip",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET)",
     "    met = all(observed[k] == EXPECTED_TARGET[k] for k in EXPECTED_TARGET if k != \"ledger_tip_ok\")",
     "drop ledger_tip_ok term from verdict conjunction"),
    ("m21-toctou-len1",
     "    toctou_declared = 1 if declared == [spec[\"toctou_clause\"]] else 0",
     "    toctou_declared = 1 if len(declared) == 1 else 0  # dropped: clause identity",
     "drop identity of declared clause (len==1 suffices)"),
    ("m22-retired-get",
     "    retired = ledger.get(\"retired\", [])",
     "    retired = ledger[\"retired\"]  # dropped: absent-retired tolerance",
     "drop absent-'retired' key tolerance"),
    ("m23-revparse-check",
     "                        check=True,",
     "                        check=False,  # dropped",
     "drop subprocess check=True (fail => empty stdout instead of exception)"),
    ("m24-control-get",
     "        control = clause.get(\"control\")",
     "        control = clause[\"control\"]  # dropped: absent-control tolerance",
     "drop absent-'control' key tolerance"),
]

GOLDEN_LEDGER = json.loads((ROOT / ".ufo/waves/round-35/c1/clauses.json").read_text())
GOLDEN_SPEC = json.loads((ROOT / ".ufo/waves/round-35/c2/frozen.json").read_text())
FIX = SCRATCH / "fixtures"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def spec_for(name: str, clause_ledger: str, blob_ledger: str, **extra) -> dict:
    spec = dict(GOLDEN_SPEC)
    spec["clause_ledger"] = clause_ledger
    spec["blob_ledger"] = blob_ledger
    spec.update(extra)
    return spec


def ledger(mut=None) -> dict:
    led = json.loads(json.dumps(GOLDEN_LEDGER))
    if mut:
        mut(led)
    return led


def strip_ctl(clause, drop_ctl=True, drop_nl=False):
    clause.pop("control", None)
    clause.pop("not-load-bearing", None)


def fixtures():
    P = ".ufo/waves/round-35/scratch/MutC2Drop/fixtures"

    def base(name):
        """Golden copy: committed ledger + committed blob ledger, spec pointed at both."""
        d = FIX / name
        write(d / "clauses.json", json.dumps(GOLDEN_LEDGER, indent=1) + "\n")
        return spec_for(name, f"{P}/{name}/clauses.json", ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")

    fx = {}

    fx["f00-golden"] = base("f00-golden")

    # f01: mirror of committed control c2-donothing — first clause loses its
    # control field, keeps everything else. Receipt parity fixture.
    def m01(led):
        strip_ctl(led["live"][0])
    fx["f01-donothing"] = spec_for("f01-donothing",
                                   f"{P}/f01-donothing/clauses.json",
                                   ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f01-donothing" / "clauses.json", json.dumps(ledger(m01), indent=1) + "\n")

    # f02: first clause's receipt points at a nonexistent path.
    def m02(led):
        led["live"][0]["control"]["receipt"] = ".ufo/waves/round-35/scratch/MutC2Drop/fixtures/f02-missing-receipt/no-such-receipt.txt"
    fx["f02-missing-receipt"] = spec_for("f02-missing-receipt",
                                         f"{P}/f02-missing-receipt/clauses.json",
                                         ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f02-missing-receipt" / "clauses.json", json.dumps(ledger(m02), indent=1) + "\n")

    # f03: first clause's receipt is golden.txt — exists, records TARGET_MET.
    def m03(led):
        led["live"][0]["control"]["receipt"] = ".ufo/waves/round-35/controls/golden.txt"
    fx["f03-clean-receipt"] = spec_for("f03-clean-receipt",
                                       f"{P}/f03-clean-receipt/clauses.json",
                                       ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f03-clean-receipt" / "clauses.json", json.dumps(ledger(m03), indent=1) + "\n")

    # f04: retired id also present in live (with a working MISSED control).
    def m04(led):
        led["live"].insert(0, {
            "id": "r34-word-bound-1-25",
            "why": "fixture: retired id reappearing in live",
            "control": {"tree": "controls/c1-digest",
                        "receipt": ".ufo/waves/round-35/controls/c1-digest.txt"},
        })
    fx["f04-retired-also-live"] = spec_for("f04-retired-also-live",
                                           f"{P}/f04-retired-also-live/clauses.json",
                                           ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f04-retired-also-live" / "clauses.json", json.dumps(ledger(m04), indent=1) + "\n")

    # f05: retired list empty.
    def m05(led):
        led["retired"] = []
    fx["f05-retired-empty"] = spec_for("f05-retired-empty",
                                       f"{P}/f05-retired-empty/clauses.json",
                                       ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f05-retired-empty" / "clauses.json", json.dumps(ledger(m05), indent=1) + "\n")

    # f06: second clause declared not-load-bearing with a reason.
    def m06(led):
        led["live"].append({
            "id": "extra-declared",
            "why": "fixture: a second declared clause",
            "not-load-bearing": {"reason": "fixture declaration"},
        })
    fx["f06-declared-extra"] = spec_for("f06-declared-extra",
                                        f"{P}/f06-declared-extra/clauses.json",
                                        ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f06-declared-extra" / "clauses.json", json.dumps(ledger(m06), indent=1) + "\n")

    # f07: extra clause with not-load-bearing but empty dict (no reason), no control.
    def m07(led):
        led["live"].append({
            "id": "extra-nl-no-reason",
            "why": "fixture: declaration without a reason and without a control",
            "not-load-bearing": {},
        })
    fx["f07-nl-no-reason-bare"] = spec_for("f07-nl-no-reason-bare",
                                           f"{P}/f07-nl-no-reason-bare/clauses.json",
                                           ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f07-nl-no-reason-bare" / "clauses.json", json.dumps(ledger(m07), indent=1) + "\n")

    # f08: the toctou clause keeps its not-load-bearing object but loses the
    # reason, and gains a working MISSED control.
    def m08(led):
        for c in led["live"]:
            if c["id"] == "o-nofollow-open":
                c["not-load-bearing"] = {}
                c["control"] = {"tree": "controls/c1-status-queued",
                                "receipt": ".ufo/waves/round-35/controls/c1-status-queued.txt"}
    fx["f08-nl-no-reason-with-control"] = spec_for(
        "f08-nl-no-reason-with-control",
        f"{P}/f08-nl-no-reason-with-control/clauses.json",
        ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f08-nl-no-reason-with-control" / "clauses.json", json.dumps(ledger(m08), indent=1) + "\n")

    # f09: blob ledger path does not exist.
    spec9 = base("f09-blobledger-absent")
    spec9["blob_ledger"] = f"{P}/f09-blobledger-absent/no-such-ledger.md"
    fx["f09-blobledger-absent"] = spec9

    # f10: blob ledger exists but never names the r34 tip.
    ledger_md = (ROOT / ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md").read_text()
    ledger_md_no_tip = ledger_md.replace("dff394109f3cc3d851309ad7c67dd3b35b46adf2", "0" * 40)
    write(FIX / "f10-tip-absent" / "RevFrozenBlobs-r35.md", ledger_md_no_tip)
    spec10 = base("f10-tip-absent")
    spec10["blob_ledger"] = f"{P}/f10-tip-absent/RevFrozenBlobs-r35.md"
    fx["f10-tip-absent"] = spec10

    # f11: one frozen blob_id wrong (flip last hex char).
    spec11 = base("f11-blob-id-wrong")
    spec11["frozen_blobs"] = [dict(b) for b in spec11["frozen_blobs"]]
    spec11["frozen_blobs"][0]["blob_id"] = spec11["frozen_blobs"][0]["blob_id"][:-1] + "0"
    fx["f11-blob-id-wrong"] = spec11

    # f12: one frozen blob path does not exist at the r34 tip.
    spec12 = base("f12-blob-path-missing")
    spec12["frozen_blobs"] = [dict(b) for b in spec12["frozen_blobs"]]
    spec12["frozen_blobs"][0]["path"] = ".ufo/waves/round-34/no-such-file.py"
    fx["f12-blob-path-missing"] = spec12

    # f13: predicate string drifted in the frozen spec.
    spec13 = base("f13-predicate-drift")
    spec13["predicate"] = spec13["predicate"].replace("uncovered=0", "uncovered<=0", 1)
    fx["f13-predicate-drift"] = spec13

    # f14: target object drifted in the frozen spec.
    spec14 = base("f14-target-drift")
    spec14["target"] = dict(spec14["target"], uncovered=5)
    fx["f14-target-drift"] = spec14

    # f15: --frozen path absent (no files needed; runner passes missing path).
    fx["f15-frozen-absent"] = None

    # f16: clause_ledger path does not exist.
    spec16 = spec_for("f16-ledger-absent",
                      f"{P}/f16-ledger-absent/no-such-clauses.json",
                      ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    fx["f16-ledger-absent"] = spec16

    # f17: a different single clause is declared (identity, not count).
    def m17(led):
        for c in led["live"]:
            if c["id"] == "o-nofollow-open":
                c.pop("not-load-bearing")
                c["control"] = {"tree": "controls/c1-entry-symlink",
                                "receipt": ".ufo/waves/round-35/controls/c1-entry-symlink.txt"}
        led["live"].append({
            "id": "other-declared",
            "why": "fixture: different declared clause",
            "not-load-bearing": {"reason": "fixture declaration"},
        })
    fx["f17-declared-other"] = spec_for("f17-declared-other",
                                        f"{P}/f17-declared-other/clauses.json",
                                        ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f17-declared-other" / "clauses.json", json.dumps(ledger(m17), indent=1) + "\n")

    # f18: ledger has no 'retired' key at all.
    def m18(led):
        del led["retired"]
    fx["f18-retired-key-absent"] = spec_for("f18-retired-key-absent",
                                            f"{P}/f18-retired-key-absent/clauses.json",
                                            ".ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md")
    write(FIX / "f18-retired-key-absent" / "clauses.json", json.dumps(ledger(m18), indent=1) + "\n")

    # spec files
    for name, spec in fx.items():
        if spec is not None:
            write(FIX / name / "frozen.json", json.dumps(spec, indent=1) + "\n")

    return fx


def main():
    mut_dir = SCRATCH / "mutants"
    diffs = []
    for name, old, new, desc in MUTANTS:
        n = SRC.count(old)
        if n != 1:
            print(f"FATAL {name}: pattern occurs {n}x", file=sys.stderr)
            sys.exit(2)
        mut = SRC.replace(old, new, 1)
        write(mut_dir / f"{name}.py", mut)
        d = difflib.unified_diff(
            SRC.splitlines(keepends=True), mut.splitlines(keepends=True),
            fromfile="count.py", tofile=f"{name}.py", n=1)
        diffs.append("".join(d))
    write(SCRATCH / "mutant-diffs.patch", "\n".join(diffs))
    fixtures()
    print(f"built {len(MUTANTS)} mutants, {len(list(FIX.glob('f*')))} fixtures")


if __name__ == "__main__":
    main()
