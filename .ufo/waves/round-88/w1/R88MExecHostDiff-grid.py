#!/usr/bin/env python3
"""R88 host-config coverage receipt: base resolver vs round-88 c2 candidate.

Runs a fixed notification grid against the host's real mako configuration
(~/.config/mako/config and the files it includes) with two read-only tools:

  * base      -- the round-87 resolver committed at the round base revision
  * cand      -- .ufo/waves/round-88/build/mado-mako.c2.py, additionally given
                 --summary (the grid value), fixed --body/--category/
                 --desktop-entry/--app-icon and --actionable/--expiring false
  * cand-bare -- same candidate tool invoked exactly like the base tool, so a
                 refusal caused by an unsupplied input can be separated from a
                 refusal caused by an unsupported field

Grid: app-name {notify-send, Spotify, firefox} x urgency {low, normal,
critical} x modes {[], [do-not-disturb]} x summary {"Setup Wi-Fi", "hello"}.

The base tool has no notification-input flags, so summary cannot be passed to
it; the summary axis is a candidate-only input and a row label here.

Per input and per tool it records: rc, effective invisible / default-timeout /
layer / on-button-left, refusal count, and the deduplicated refusal texts.
It then prints a markdown table and a per-tool dedup refusal list, and writes
the full JSON record to --out.

Read-only: only reads the host config chain and executes the two tools.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

APPS = ["notify-send", "Spotify", "firefox"]
URGENCIES = ["low", "normal", "critical"]
MODE_SETS = [(), ("do-not-disturb",)]
SUMMARIES = ["Setup Wi-Fi", "hello"]
FIELDS = ("invisible", "default-timeout", "layer", "on-button-left")

# The candidate's extra inputs.  summary is the grid value; the rest are fixed
# so the only varying candidate input is the grid tuple.
FIXED_CAND = [
    "--body", "grid-body",
    "--category", "grid-category",
    "--desktop-entry", "grid-desktop-entry",
    "--app-icon", "grid-app-icon",
    "--actionable", "false",
    "--expiring", "false",
]

REFUSAL_RE = re.compile(r"^(?P<path>.+?):(?P<line>\d+): (?P<text>.*)$")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def invoke(tool, argv_tail):
    proc = subprocess.run([sys.executable, "-I", tool] + argv_tail,
                          capture_output=True, text=True)
    record = {"rc": proc.returncode}
    if proc.returncode != 0:
        record["error"] = (proc.stderr.strip().splitlines() or [""])[-1]
        record["effective"] = {field: None for field in FIELDS}
        record["refusals"] = []
        record["refusal_count"] = 0
        return record
    data = json.loads(proc.stdout)
    effective = data.get("effective", {})
    refusals = data.get("refusals", [])
    record["effective"] = {field: effective.get(field) for field in FIELDS}
    record["refusals"] = sorted(set(refusals))
    record["refusal_count"] = len(refusals)
    record["include_applied"] = any(str(item).startswith("include:")
                                    for item in data.get("applied", []))
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base (round-87) tool path")
    parser.add_argument("--candidate", required=True, help="c2 candidate tool path")
    parser.add_argument("--config", default=os.path.expanduser("~/.config/mako/config"))
    parser.add_argument("--home", default=os.path.expanduser("~"))
    parser.add_argument("--out", help="write the full JSON record here")
    args = parser.parse_args(argv)

    config = os.path.expanduser(args.config)
    home = os.path.expanduser(args.home)

    common = ["--config", config, "--home", home]
    grid = []
    for app in APPS:
        for urgency in URGENCIES:
            for modes in MODE_SETS:
                for summary in SUMMARIES:
                    base_argv = common + ["--app-name", app, "--urgency", urgency]
                    for mode in modes:
                        base_argv += ["--mode", mode]
                    cand_argv = list(base_argv) + ["--summary", summary] + FIXED_CAND
                    grid.append({
                        "input": {"app_name": app, "urgency": urgency,
                                  "modes": list(modes), "summary": summary},
                        "base": invoke(args.base, base_argv),
                        "candidate": invoke(args.candidate, cand_argv),
                        "candidate_bare": invoke(args.candidate, list(base_argv)),
                    })

    # Probes without notification inputs: show which host sections cannot be
    # decided at all (criteria whose input is absent).
    probes = {
        "base_no_inputs": invoke(args.base, common),
        "candidate_no_inputs": invoke(args.candidate,
                                      common + ["--summary", "hello"] + FIXED_CAND),
    }

    scope = {"base": args.base, "candidate": args.candidate, "grid_size": len(grid),
             "config": config, "config_realpath": os.path.realpath(config),
             "home": home,
             "sha256": {os.path.basename(p): sha256(p)
                        for p in (args.base, args.candidate)},
             "note": "summary is a candidate-only input; the base tool has no such flag"}
    tools = ("base", "candidate", "candidate_bare")
    dedup = {tool: sorted({text for row in grid for text in row[tool]["refusals"]})
             for tool in tools}
    # per-line histogram and message-only dedup
    lines = {tool: {} for tool in tools}
    for tool in tools:
        for text in dedup[tool]:
            match = REFUSAL_RE.match(text)
            if not match:
                lines[tool].setdefault("unparsed", []).append(text)
                continue
            entry = lines[tool].setdefault(match.group("line"), [])
            if match.group("text") not in entry:
                entry.append(match.group("text"))

    print("MADO_HOST_GRID: rows=" + str(len(grid)))
    print("| app | urgency | modes | summary | base rc | base invisible | base timeout | base layer | base on-button-left | base refusals | cand rc | cand invisible | cand timeout | cand layer | cand on-button-left | cand refusals |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for row in grid:
        item = row["input"]
        b = row["base"]
        c = row["candidate"]
        print("| {app} | {urgency} | {modes} | {summary} | {brc} | {bi} | {bt} | {bl} | {bobl} | {br} | {crc} | {ci} | {ct} | {cl} | {cobl} | {cr} |".format(
            app=item["app_name"], urgency=item["urgency"],
            modes=",".join(item["modes"]) or "-", summary=item["summary"],
            brc=b["rc"], bi=b["effective"]["invisible"], bt=b["effective"]["default-timeout"],
            bl=b["effective"]["layer"], bobl=b["effective"]["on-button-left"],
            br=b["refusal_count"], crc=c["rc"], ci=c["effective"]["invisible"],
            ct=c["effective"]["default-timeout"], cl=c["effective"]["layer"],
            cobl=c["effective"]["on-button-left"], cr=c["refusal_count"]))

    for tool in tools:
        print("\n=== dedup refusals: " + tool + " (" + str(len(dedup[tool])) + ") ===")
        for text in dedup[tool]:
            print(text)

    print("\n=== probes without notification inputs ===")
    for name, record in probes.items():
        print(name + ": rc=" + str(record["rc"]) + " refusals=" + str(record["refusal_count"]))
        for text in record["refusals"]:
            print("  " + text)

    payload = {"meta": scope, "grid": grid, "dedup": dedup, "by_line": lines,
               "probes": probes}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=1, sort_keys=True)
            handle.write("\n")
        print("\nMADO_HOST_GRID_JSON: " + args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
