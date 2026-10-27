#!/usr/bin/env python3
"""check102-wave-done.py — seat prototype for candidate QUALITY criterion 102 (round-49 D2).

A round report is committed only after every dispatched wave's results file exists with every
seat settled.

Inputs: `--round-dir` is a `.ufo/waves/round-N` directory holding `<wave>-dispatch.json` and,
after the dispatcher finalizes the wave, `<wave>-results.json` (the shape
`scripts/hyaku/inline-dispatcher.py` writes: `{lane, round, wave, seats, results:[{name, agent,
output, note}]}`).  `--report PATH [--rev REV]` proves the round report exists at REV
(`git cat-file -e REV:PATH`), or, without `--rev`, in the worktree (`test -f`, the integration
form the gate is applied in) and fails when any dispatched wave is not done.

Per seat: `SEAT wave=<w> name=<n> status=settled|settled_with_note|missing|empty`.
Per wave: `WAVE wave=<w> dispatched=<n> results=present|missing settled=<n> unsettled=<n>`.
Report:  `REPORT_COMMITTED rev=<r> path=<p> waves_done=<n>/<n>` or `REPORT_BEFORE_WAVE_DONE ...`.
Summary: `CHECK102: waves=<n> dispatched=<n> settled=<n> results_missing=<k> unsettled=<k>
report=<path|none> verdict=OK|FAIL`; exit 1 when a results file is missing, a seat is unsettled,
or a committed report precedes wave completion.
"""
import argparse
import glob
import json
import os
import subprocess
import sys


def load(path):
    with open(path, "r", errors="replace") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--round-dir", required=True)
    ap.add_argument("--report")
    ap.add_argument("--rev")
    ap.add_argument("--results-rev",
                    help="audit form: prove each <wave>-results.json at this revision of the round dir's own "
                         "repo (git cat-file -e REV:path), so a file written after closure cannot green a past run")
    a = ap.parse_args(argv)

    dispatches = sorted(glob.glob(os.path.join(a.round_dir, "*-dispatch.json")))
    if not dispatches:
        print(f"CHECK102: no dispatch file under {a.round_dir}", file=sys.stderr)
        return 2

    top = subprocess.run(("git", "-C", a.round_dir, "rev-parse", "--show-toplevel"),
                         capture_output=True, text=True)
    results_repo = top.stdout.strip() if top.returncode == 0 else None
    rd_rel = os.path.relpath(a.round_dir, results_repo) if results_repo else a.round_dir

    def results_present(wave):
        rel = os.path.join(rd_rel, f"{wave}-results.json")
        if a.results_rev:
            if not results_repo:
                return False
            return subprocess.run(("git", "-C", results_repo, "cat-file", "-e",
                                   f"{a.results_rev}:{rel}"), capture_output=True).returncode == 0
        return os.path.isfile(os.path.join(a.round_dir, f"{wave}-results.json"))

    waves = dispatched = settled = 0
    missing_files = unsettled_total = 0
    for dpath in dispatches:
        d = load(dpath)
        wave = d.get("wave") or os.path.basename(dpath).split("-dispatch")[0]
        tasks = [t["name"] for t in d.get("taskCall", {}).get("tasks", [])]
        rpath = os.path.join(a.round_dir, f"{wave}-results.json")
        waves += 1
        dispatched += len(tasks)
        if not results_present(wave):
            where = f"results_rev={a.results_rev}" if a.results_rev else "results=worktree"
            print(f"RESULTS_NOT_AT_REV wave={wave} {where} path={os.path.join(rd_rel, wave + '-results.json')}"
                  if a.results_rev else
                  f"WAVE wave={wave} dispatched={len(tasks)} results=missing settled=0 unsettled={len(tasks)}")
            missing_files += 1
            unsettled_total += len(tasks)
            continue
        if a.results_rev:
            blob = subprocess.run(("git", "-C", results_repo, "show",
                                   f"{a.results_rev}:{os.path.join(rd_rel, wave + '-results.json')}"),
                                  capture_output=True, text=True)
            r = json.loads(blob.stdout)
        else:
            r = load(rpath)
        rows = {row.get("name"): row for row in r.get("results", [])}
        ws = 0
        for name in tasks:
            row = rows.get(name)
            if row is None:
                status = "missing"
            elif row.get("output") is None and row.get("note") is None:
                status = "empty"
            elif row.get("output") is None:
                seat_report = os.path.join(a.round_dir, wave, f"{name}.md")
                status = "settled_with_note" if os.path.isfile(seat_report) else "note_no_report"
            else:
                status = "settled"
            if status in ("settled", "settled_with_note"):
                ws += 1
            print(f"SEAT wave={wave} name={name} status={status}")
        settled += ws
        unsettled_total += len(tasks) - ws
        print(f"WAVE wave={wave} dispatched={len(tasks)} results=present settled={ws} "
              f"unsettled={len(tasks) - ws}")

    report_state = "none"
    if a.report:
        if a.rev:
            rc = subprocess.run(("git", "-C", a.repo, "cat-file", "-e", f"{a.rev}:{a.report}"),
                                capture_output=True).returncode
        else:
            rc = 0 if os.path.isfile(os.path.join(a.repo, a.report)) else 1
        if rc != 0:
            report_state = "absent"
            print(f"REPORT_ABSENT rev={a.rev} path={a.report}")
        elif missing_files or unsettled_total:
            report_state = "before-wave-done"
            print(f"REPORT_BEFORE_WAVE_DONE rev={a.rev or 'worktree'} path={a.report} "
                  f"results_missing={missing_files} unsettled={unsettled_total}")
        else:
            report_state = "after-wave-done"
            print(f"REPORT_COMMITTED rev={a.rev or 'worktree'} path={a.report} "
                  f"waves_done={waves}/{waves}")

    fail = missing_files > 0 or unsettled_total > 0 or report_state == "before-wave-done"
    print(f"CHECK102: waves={waves} dispatched={dispatched} settled={settled} "
          f"results_missing={missing_files} unsettled={unsettled_total} "
          f"report={a.report or 'none'} verdict={'FAIL' if fail else 'OK'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
