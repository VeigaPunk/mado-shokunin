import hashlib, json, pathlib, re

S = pathlib.Path("/fast/scratch/hyaku/mado-r56/R56W2ScoutRows2")
entry_path = S / "pin/corpus/knowledge/hyprland-config-autoreload-r56.md"
sources_path = S / "pin/corpus/SOURCES.md"
tables = json.loads(pathlib.Path(
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/frozen-tables-v2.json"
).read_text(encoding="utf-8"))
frozen_k = {r["id"]: r for r in tables["c1"]["k"]}
pin_sha = tables["c1"]["pin_sha256"]

fetch_files = {
    "Hyprland-PropRefresher.cpp": S / "fetch/PropRefresher.cpp",
    "Hyprland-EventLoopManager.cpp": S / "fetch/EventLoopManager.cpp",
}
pins = {name: p.read_bytes() for name, p in fetch_files.items()}
pin_lines = {name: {i + 1: ln for i, ln in enumerate(blob.split(b"\n"))}
             for name, blob in pins.items()}

# --- registry rows S385, S386: parse 11 cells
reg = {}
for line in sources_path.read_text(encoding="utf-8").split("\n"):
    m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
    if m and m.group(1) in ("S385", "S386"):
        cells = [c for c in line.strip().strip("|").split(" | ")]
        reg[m.group(1)] = (line, cells)
for sid in ("S385", "S386"):
    line, cells = reg[sid]
    print(f"== {sid}: cells={len(cells)}")
    for i, c in enumerate(cells, 1):
        print(f"  cell{i}: {c[:160]!r}")
    # anchor parse
    anchor = cells[5]
    am = re.match(r"^(\S+\.cpp):([0-9,;-]+) @ ([0-9a-f]{40}); pin (\S+) (\d+) B sha256:([0-9a-f]{64})$", anchor)
    print("  anchor_struct_ok=", bool(am), "" if not am else am.groups())
    base, locs, rev, pinpath, size, sha = am.groups()
    pinname = pathlib.Path(pinpath).name
    ranges = []
    for part in locs.split(","):
        if "-" in part:
            a, b = part.split("-"); ranges.append((int(a), int(b)))
        else:
            v = int(part); ranges.append((v, v))
    maxloc = max(b for _, b in ranges)
    last = len(pins[pinname].split(b"\n")) - (1 if pins[pinname].endswith(b"\n") else 0)
    print(f"  anchor_max_locator={maxloc} pin_last_line={last} anchor_within_file={maxloc <= last}")
    print(f"  anchor_sha_matches_fetch={sha == hashlib.sha256(pins[pinname]).hexdigest()}")
    print(f"  anchor_sha_matches_frozen={sha == pin_sha[pinname]}")
    print(f"  anchor_size_matches_fetch={int(size) == len(pins[pinname])}")

# --- entry rows citing S385/S386
entry_lines = entry_path.read_text(encoding="utf-8").split("\n")
krow_re = re.compile(r"^\| (K\d{2}) \| (.+) \| (S\d{3}) \| (\S+\.cpp):(\d+) \| `([^`]*)` \|$")
anchor_of = {}
for sid, (line, cells) in reg.items():
    anchor_of[sid] = cells[5]
for ln_no, line in enumerate(entry_lines, 1):
    m = krow_re.match(line)
    if not m:
        continue
    kid, prop, sid, pinbase, lineno, quote = m.groups()
    if sid not in ("S385", "S386"):
        continue
    pinname = pinbase
    n = int(lineno)
    ups = pin_lines[pinname].get(n, b"").decode("utf-8")
    in_anchor = any(a <= n <= b for a, b in
                    [(int(x.split("-")[0]), int(x.split("-")[-1]))
                     for x in re.search(r":([0-9,;-]+) @", anchor_of[sid]).group(1).split(",")])
    fk = frozen_k.get(kid)
    print(f"== {kid} cites {sid} at entry_line={ln_no} pin={pinbase}:{n}")
    print(f"   cells5_ok=True quote_len={len(quote)}")
    print(f"   quote==frozen_table_quote={fk is not None and fk['quote'] == quote}")
    print(f"   frozen_table_line={fk['line'] if fk else None} matches_row_cell={fk is not None and str(fk['line']) == lineno and fk['pin'] == pinname}")
    print(f"   quote_substring_of_upstream_line={quote in ups}")
    print(f"   upstream_line={ups.strip()[:140]!r}")
    print(f"   line_inside_anchor_ranges={in_anchor} (anchor={anchor_of[sid].split(' @')[0]})")
    print(f"   proposition_len={len(prop)} tok_shared={any(t in quote for t in re.findall(r'[A-Za-z_][A-Za-z0-9_]{3,}', prop))}")

# --- any other mention of S385/S386 in the entry
for ln_no, line in enumerate(entry_lines, 1):
    if re.search(r"S38[56]", line) and not krow_re.match(line):
        print(f"other mention: entry_line={ln_no}: {line[:120]!r}")
