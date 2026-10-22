#!/usr/bin/env python3
"""Tabulate drive.py receipts: exit, timeout, elapsed, RSS, verdict, findings."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    rows = []
    for path in sorted(Path(argv[0]).glob("*.json")):
        try:
            r = json.loads(path.read_text())
        except ValueError as exc:
            rows.append({"receipt": path.name, "unreadable": str(exc)})
            continue
        s = r.get("summary", {})
        rows.append({
            "receipt": path.name,
            "exit": r["exit"],
            "timed_out": r["timed_out"],
            "elapsed_s": round(r["elapsed_seconds"], 3),
            "maxrss_mib": None if r["wait4_ru_maxrss_kib"] is None else round(r["wait4_ru_maxrss_kib"] / 1024, 1),
            "verdict_exit": s.get("verdict_exit"),
            "error": s.get("error"),
            "file_errors": s.get("file_errors"),
            "unparsed": [s.get("eval_unparsed"), s.get("unparsed_spawns")],
            "findings": s.get("findings"),
            "stderr_tail": r["stderr"]["text"][-300:],
            "stdout_sha256": r["stdout"]["sha256"],
            "tool_sha256": r["tool_sha256_before"][:8],
        })
    json.dump(rows, sys.stdout, indent=1, default=list)
    print()
    for row in rows:
        if "unreadable" in row:
            print(row["receipt"], "UNREADABLE")
            continue
        print("%-58s exit=%-4s to=%-5s %7.3fs %6s MiB vexit=%s err=%s ferr=%s unp=%s find=%s" % (
            row["receipt"], row["exit"], row["timed_out"], row["elapsed_s"], row["maxrss_mib"],
            row["verdict_exit"], row["error"], row["file_errors"], row["unparsed"], row["findings"]),
            file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
