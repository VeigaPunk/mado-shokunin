import hashlib, json, re, sys

WORK = "/fast/scratch/hyaku/mado-r56/R56W2ScoutRows5/work"
FETCH = "/fast/scratch/hyaku/mado-r56/R56W2ScoutRows5/fetch"
OUT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2ScoutRows5"

pins = {
    "man7-inotify.7.html": f"{FETCH}/man7-inotify.7.html",
    "Hyprland-PropRefresher.hpp": f"{FETCH}/Hyprland-PropRefresher.hpp",
}

blob_info = {}
for name, path in pins.items():
    b = open(path, "rb").read()
    lines = b.split(b"\n")
    blob_info[name] = {
        "sha256": hashlib.sha256(b).hexdigest(),
        "bytes": len(b),
        "wc_minus_l": b.count(b"\n"),
        "ends_with_newline": b.endswith(b"\n"),
        "split_line_count (E3 bound len(blob.split(chr(10))))": len(lines),
    }

src = open(f"{WORK}/corpus/SOURCES.md", encoding="utf-8").read().split("\n")
entry = open(f"{WORK}/corpus/knowledge/hyprland-config-autoreload-r56.md", encoding="utf-8").read().split("\n")

def cell(line, idx):
    parts = line.split(" | ")
    return parts[idx].strip(" |") if idx < len(parts) else None

rows = {}
for ln in src:
    s = ln.strip()
    if s.startswith("| S390 |") or s.startswith("| S391 |"):
        rid = s.split(" | ")[0].lstrip("| ").strip()
        cells = [c.strip() for c in s.strip().strip("|").split("|")]
        # header: id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by
        rows[rid] = {
            "kind": cells[2], "tier": cells[3], "scope": cells[4],
            "anchor": cells[5], "teaches": cells[6], "status": cells[7],
            "opened": cells[8], "recheck": cells[9], "used_by": cells[10],
        }

anchor_sha = {"S390": None, "S391": None}
for rid, r in rows.items():
    m = re.search(r"sha256:([0-9a-f]{64})", r["anchor"])
    anchor_sha[rid] = m.group(1) if m else None
    locs = re.findall(r"([A-Za-z0-9._-]+):([0-9]+(?:-[0-9]+)?(?:,[0-9]+(?:-[0-9]+)?)*)", r["anchor"])
    r["anchor_locators"] = locs

# anchor sha cross-check with fetched bytes
for rid, r in rows.items():
    pin = "man7-inotify.7.html" if rid == "S390" else "Hyprland-PropRefresher.hpp"
    r["anchor_sha_matches_fetch"] = anchor_sha[rid] == blob_info[pin]["sha256"]

# entry K/E rows citing S390/S391
checks = []
for ln in entry:
    s = ln.strip()
    m = re.match(r"\| (K\d+|E\d+) \| (.+) \| (S390|S391) \| ([^|]+) \| `(.*)` \|", s)
    if not m:
        continue
    kid, prop, rid, loc, quote = m.group(1), m.group(2), m.group(3), m.group(4).strip(), m.group(5)
    base, _, linenum = loc.rpartition(":")
    pin = "man7-inotify.7.html" if rid == "S390" else "Hyprland-PropRefresher.hpp"
    b = open(pins[pin], "rb").read()
    lines = b.split(b"\n")
    qb = quote.encode("utf-8")
    claimed = int(linenum)
    at_claimed = qb in lines[claimed - 1]
    occurrences = [i + 1 for i, l in enumerate(lines) if qb in l]
    # anchor ranges for this row
    ranges = []
    for lb, ls in rows[rid]["anchor_locators"]:
        if lb == base or base.endswith(lb) or lb.endswith(base):
            for part in ls.split(","):
                if "-" in part:
                    a, z = part.split("-")
                    ranges.append((int(a), int(z)))
                else:
                    ranges.append((int(part), int(part)))
    in_anchor = any(a <= claimed <= z for a, z in ranges)
    within_eof = claimed <= len(lines)
    checks.append({
        "entry_row": kid, "row": rid, "locator": loc, "locator_basename": base,
        "locator_line": claimed, "quote": quote,
        "quote_at_claimed_line": at_claimed,
        "quote_found_on_lines": occurrences,
        "quote_len_chars": len(quote),
        "anchor_ranges_for_basename": ranges,
        "quote_line_inside_anchor_range": in_anchor,
        "locator_within_split_line_count": within_eof,
        "proposition": prop,
    })

frozen = json.load(open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/frozen-tables-v2.json"))
pinmap = frozen["c1"]["pin_sha256"]
frozen_status = {
    "S390": {"pin_in_frozen_c1_map": "man7-inotify.7.html" in pinmap,
             "frozen_sha": pinmap.get("man7-inotify.7.html"),
             "matches_fetch": pinmap.get("man7-inotify.7.html") == blob_info["man7-inotify.7.html"]["sha256"],
             "in_new_row_ids": "S390" in frozen["c1"]["new_row_ids"]},
    "S391": {"pin_in_frozen_c1_map": "Hyprland-PropRefresher.hpp" in pinmap,
             "frozen_sha": pinmap.get("Hyprland-PropRefresher.hpp"),
             "matches_fetch": pinmap.get("Hyprland-PropRefresher.hpp") == blob_info["Hyprland-PropRefresher.hpp"]["sha256"],
             "in_new_row_ids": "S391" in frozen["c1"]["new_row_ids"]},
}

receipt = {"blob_info": blob_info, "rows": rows, "anchor_cell_sha": anchor_sha, "entry_checks": checks, "frozen_c1_status": frozen_status}
with open(f"{OUT}/receipt-s390-s391.json", "w", encoding="utf-8") as f:
    json.dump(receipt, f, indent=2, ensure_ascii=False)

print(json.dumps(receipt, indent=1, ensure_ascii=False))
