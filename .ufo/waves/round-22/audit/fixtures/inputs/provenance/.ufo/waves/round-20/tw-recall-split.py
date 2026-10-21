#!/usr/bin/env python3
"""Round-20 evidence split for the frozen round-18 tripwire incidents.

Usage: tw-recall-split.py REV -> one JSON object on stdout; exit 0 on scan,
2 when the pinned corpus or requested revision cannot be evaluated.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PIN_REV = "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d"
FROZEN = ".ufo/waves/round-18/frozen"
EVIDENCE = ("observed", "lead", "unmarked")


def show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"],
                       capture_output=True)
    if p.returncode != 0:
        raise ValueError(f"git show {rev}:{path} rc={p.returncode}")
    return p.stdout


def main():
    if len(sys.argv) != 2:
        print("usage: tw-recall-split.py REV", file=sys.stderr)
        return 2
    rev = sys.argv[1]
    p = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify",
                        rev + "^{commit}"], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"could_not_evaluate: rev {rev}", file=sys.stderr)
        return 2
    commit = p.stdout.strip()
    try:
        exp = json.loads(show(PIN_REV, f"{FROZEN}/expected.json"))
        incident = sorted({(f["file"], f["line"]) for f in exp["expected_findings"]}
                          | {(m["file"], m["line"])
                             for m in exp.get("known_misses", [])})
        tool = show(rev, "tools/mado-tripwire.py")
        input_line_keys = set()
        with tempfile.TemporaryDirectory(prefix="mado-r20-recall-split-") as td:
            os.makedirs(os.path.join(td, "inputs"))
            paths = []
            for inp in exp["inputs"]:
                path = inp["path"]
                data = show(PIN_REV, f"{FROZEN}/{path}")
                if hashlib.sha256(data).hexdigest() != inp["sha256"]:
                    raise ValueError(f"digest {path}")
                with open(os.path.join(td, path), "wb") as fh:
                    fh.write(data)
                input_line_keys.update((path, n)
                                       for n in range(1, len(data.splitlines()) + 1))
                paths.append(path)
            with open(os.path.join(td, "tool.py"), "wb") as fh:
                fh.write(tool)
            if not set(incident) <= input_line_keys:
                raise ValueError("incident line outside pinned inputs")
            control = input_line_keys - set(incident)
            if len(incident) != 6 or len(control) != 20:
                raise ValueError(f"pinned denominator incident={len(incident)} control={len(control)}")

            r = subprocess.run([sys.executable, "-I", "tool.py", "--scan", *paths],
                               cwd=td, capture_output=True, text=True)
            lines = r.stdout.splitlines()
            if r.returncode not in (0, 1) or len(lines) < 2:
                raise ValueError(f"scan rc={r.returncode}")
            verdict = json.loads(lines[1])
            findings = verdict.get("findings", [])
            if not isinstance(findings, list):
                raise ValueError("scan findings is not a list")

        by_line = defaultdict(list)
        finding_totals = Counter()
        control_findings = 0
        for finding in findings:
            key = (finding.get("file"), finding.get("line"))
            if key not in input_line_keys:
                raise ValueError(f"finding outside pinned inputs: {key!r}")
            evidence = finding.get("evidence", "unmarked")
            if evidence not in EVIDENCE:
                raise ValueError(f"unexpected evidence marker {evidence!r} at {key!r}")
            finding_totals[evidence] += 1
            item = {"class": finding.get("class"),
                    "rule": finding.get("rule"),
                    "evidence": evidence}
            if key in control:
                control_findings += 1
            else:
                by_line[key].append(item)

        rows = []
        line_totals = Counter()
        undetected = 0
        for file_name, line_number in incident:
            line_findings = by_line[(file_name, line_number)]
            if not line_findings:
                undetected += 1
            for evidence in {f["evidence"] for f in line_findings}:
                line_totals[evidence] += 1
            rows.append({"file": file_name,
                         "line": line_number,
                         "findings": line_findings})

        print(json.dumps({
            "schema": "mado-tw-recall-split-r20-v1",
            "rev": rev,
            "commit": commit,
            "tool_sha256": hashlib.sha256(tool).hexdigest(),
            "pin_rev": PIN_REV,
            "incident_lines": len(incident),
            "totals": {
                "detected_observed": line_totals["observed"],
                "detected_lead": line_totals["lead"],
                "detected_unmarked": line_totals["unmarked"],
                "undetected": undetected,
            },
            "finding_totals": {
                "observed": finding_totals["observed"],
                "lead": finding_totals["lead"],
                "unmarked": finding_totals["unmarked"],
            },
            "control_lines": len(control),
            "control_findings": control_findings,
            "rows": rows,
        }, indent=1))
        return 0
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"could_not_evaluate: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
