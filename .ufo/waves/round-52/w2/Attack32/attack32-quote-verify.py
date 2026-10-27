#!/usr/bin/env python3
"""Attack32 independent quote verification for the landed C2 entry.
Reads only local pinned bytes under .ufo/waves/round-52/fetch/ and the landed
entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md. No network, no host reads.
Checks, per proposition: collapsed-substring binding, raw-substring binding, word count."""
import re, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
pins = {}
for f in (root / ".ufo/waves/round-52/fetch").glob("Hyprland-*"):
    pins[f.name] = f.read_text().splitlines()
entry = (root / "corpus/knowledge/hyprland-synthetic-dispatch-r52.md").read_text()

def collapse(s):
    return re.sub(r"\s+", " ", s).strip()

rows = []
for line in entry.splitlines():
    if not line.strip().startswith("| P"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    pid, claim, row, pinanchor, quote, supp, why = cells
    m = re.match(r"(Hyprland-[A-Za-z-]+\.(?:cpp|hpp)):(\d+)(?:-(\d+))?", pinanchor)
    pin, first, last = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    q = quote.strip("`")
    span = "\n".join(pins[pin][first - 1:last])
    rows.append((pid, row, pin, first, last, len(collapse(q).split()),
                 collapse(q) in collapse(span), q in span))

print(f"{'id':4} {'row':5} {'pin':42} {'span':12} {'words':5} {'collapsed':9} {'raw':5}")
for r in rows:
    print(f"{r[0]:4} {r[1]:5} {r[2]:42} {str(r[3]) + '-' + str(r[4]):12} {r[5]:5} "
          f"{str(r[6]):9} {str(r[7]):5}")
print("ALL_COLLAPSED_BIND=%s ALL_RAW_BIND=%s count=%d"
      % (all(r[6] for r in rows), all(r[7] for r in rows), len(rows)))
