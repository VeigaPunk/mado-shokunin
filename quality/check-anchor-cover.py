#!/usr/bin/env python3
"""Check QUALITY criterion 107 against immutable git objects at --rev."""
import argparse
import os
import re
import subprocess
import sys

ROW_START = re.compile(r"^ {0,3}\|")
ID_CELL = re.compile(r"S[0-9]{3,}")
REG_ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
URL = re.compile(r"https?://\S+")
PIN = re.compile(r"(?:^|\s)pin\s+([^\s]+)")
PIN_CELL = re.compile(r"([^:\s]+):([0-9]+)")
LOCATOR = re.compile(r"([0-9]+)(?:-([0-9]+))?")

class SetupError(Exception):
    pass

def git_blob(repo, rev, path, env):
    result = subprocess.run(["git", "-C", repo, "cat-file", "blob", f"{rev}:{path}"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if result.returncode:
        raise SetupError(f"absent {rev}:{path}")
    return result.stdout

def cells(line):
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]

def visible_table_lines(text):
    in_fence = False
    in_comment = False
    for number, line in enumerate(text.split("\n"), 1):
        cursor = 0
        visible = ""
        while cursor < len(line):
            if in_comment:
                end = line.find("-->", cursor)
                if end < 0:
                    cursor = len(line)
                else:
                    cursor = end + 3
                    in_comment = False
            else:
                start = line.find("<!--", cursor)
                if start < 0:
                    visible += line[cursor:]
                    break
                visible += line[cursor:start]
                cursor = start + 4
                in_comment = True
        if not in_comment and FENCE.match(visible):
            in_fence = not in_fence
            continue
        if not in_fence and not in_comment and ROW_START.match(visible):
            yield number, visible

def parse_registry(text):
    found = {}
    for raw in text.split("\n"):
        match = REG_ROW.match(raw)
        if match:
            row = cells(raw)
            found.setdefault(match.group(1), []).append(row)
    return found

def occurrences(anchor, name):
    # Prefix exclusion is identifier-only; slash and hyphen are valid boundaries.
    pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r":")
    for match in pattern.finditer(anchor):
        rest = anchor[match.end():]
        first = LOCATOR.match(rest)
        if not first:
            continue
        locs = [(int(first.group(1)), int(first.group(2) or first.group(1)))]
        pos = first.end()
        while pos < len(rest):
            next_item = re.match(r", ?([0-9]+)(?:-([0-9]+))?", rest[pos:])
            if not next_item:
                break
            locs.append((int(next_item.group(1)), int(next_item.group(2) or next_item.group(1))))
            pos += next_item.end()
        rendered = ",".join(str(lo) if lo == hi else f"{lo}-{hi}" for lo, hi in locs)
        yield locs, rendered

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--entry", required=True)
    parser.add_argument("--registry", default="corpus/SOURCES.md")
    parser.add_argument("--work", required=True)
    try:
        args = parser.parse_args(argv)
        os.makedirs(args.work, exist_ok=True)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": args.work,
               "TMPDIR": args.work, "LC_ALL": "C"}
        registry = parse_registry(git_blob(args.repo, args.rev, args.registry, env).decode("utf-8", "replace"))
        entry_bytes = git_blob(args.repo, args.rev, args.entry, env)
        entry = entry_bytes.decode("utf-8", "replace")
        pin_cache = {}
        out = []
        rows = 0
        covered = 0
        for line_no, raw in visible_table_lines(entry):
            row = cells(raw)
            if len(row) < 3 or not ID_CELL.fullmatch(row[2]):
                continue
            rows += 1
            row_id, sid = row[0] if row else "", row[2]
            pin_cell = row[3] if len(row) > 3 else ""
            pin_match = PIN_CELL.fullmatch(pin_cell)
            if pin_match is None:
                fallback = re.match(r"[^:\s]+:([0-9]+)", pin_cell)
                line = int(fallback.group(1)) if fallback else 0
                out.append(f"ANCHOR_COVER: row={row_id} sid={sid} line={line} name=- locators=none eof=unchecked verdict=MISS reason=malformed-pin")
                continue
            line = int(pin_match.group(2))
            records = registry.get(sid, [])
            if not records:
                out.append(f"ANCHOR_COVER: row={row_id} sid={sid} line={line} name=- locators=none eof=unchecked verdict=MISS reason=no-registry-row")
                continue
            if len(records) != 1:
                out.append(f"ANCHOR_COVER: row={row_id} sid={sid} line={line} name=- locators=none eof=unchecked verdict=MISS reason=dup-id")
                continue
            record = records[0]
            if len(record) < 6:
                raise SetupError(f"registry row {sid} has fewer than six cells")
            urls = URL.findall(record[1])
            name = urls[-1].rstrip(").,;").rsplit("/", 1)[-1] if urls else ""
            if not name or "#" in name or "?" in name:
                out.append(f"ANCHOR_COVER: row={row_id} sid={sid} line={line} name={name or '-'} locators=none eof=unchecked verdict=MISS reason=no-name")
                continue
            anchor = record[5]
            counted = list(occurrences(anchor, name))
            all_locs = [loc for locs, _ in counted for loc in locs]
            loc_text = ",".join(rendered for _, rendered in counted) if counted else "none"
            pin_match = PIN.search(anchor)
            eof = "unchecked"
            past_eof = False
            if pin_match:
                pin_path = pin_match.group(1).rstrip(".,;)")
                if pin_path not in pin_cache:
                    pin_cache[pin_path] = len(git_blob(args.repo, args.rev, pin_path, env).split(b"\n"))
                eof = "checked"
                past_eof = any(max(lo, hi) > pin_cache[pin_path] for lo, hi in all_locs)
            cover = any(lo <= hi and lo <= line <= hi for locs, _ in counted for lo, hi in locs)
            reason = "past-eof" if past_eof else ("no-cover" if not cover else "")
            ok = bool(cover and not past_eof)
            covered += int(ok)
            suffix = f" reason={reason}" if reason else ""
            out.append(f"ANCHOR_COVER: row={row_id} sid={sid} line={line} name={name} locators={loc_text} eof={eof} verdict={'OK' if ok else 'MISS'}{suffix}")
        for line in out:
            print(line)
        miss = rows - covered
        ok = rows > 0 and miss == 0
        print(f"CHECK107: rows={rows} covered={covered} miss={miss} verdict={'OK' if ok else 'FAIL'}")
        return 0 if ok else 1
    except (SetupError, OSError, UnicodeError) as error:
        print(f"check107: {error}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
