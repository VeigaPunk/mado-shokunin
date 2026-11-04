import json, re, sys
ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
def scan(path):
    ids, seen, collisions = [], {}, []
    in_registry = False
    for n, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        line = line.rstrip("\n")
        if re.match(r"^ {0,3}##[ \t]", line):
            in_registry = line.lstrip(" ")[3:].strip() == "Registry"
            continue
        if re.match(r"^ {0,3}#[ \t]", line):
            in_registry = False
            continue
        if not in_registry:
            continue
        m = ROW.match(line)
        if not m:
            continue
        i = m.group(1)
        ids.append(i)
        if i in seen:
            collisions.append({"id": i, "lines": [seen[i], n]})
        else:
            seen[i] = n
    return ids, collisions
path = sys.argv[1]
ids, collisions = scan(path)
out = {"file": path, "rows": len(ids), "unique": len(set(ids)),
       "max_id": max(ids, key=lambda s: int(s[1:])) if ids else None,
       "collisions": collisions}
print(json.dumps(out, sort_keys=True))
