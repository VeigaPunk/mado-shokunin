import re, sys
KN = "/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
FET = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/fetch/"
want = {"K16","K17","E04","E05","E06","E07","E11"}
rows = {}
for line in open(KN, encoding="utf-8"):
    m = re.match(r"^\| ([KEH]\d\d) \| (.*?) \| (\S+) \| (\S+?):(\d+) \| `(.*)` \|$", line.rstrip("\n"))
    if m and m.group(1) in want:
        rows[m.group(1)] = dict(prop=m.group(2), src=m.group(3), file=m.group(4), line=int(m.group(5)), quote=m.group(6))
lines_cache = {}
for rid in sorted(rows):
    r = rows[rid]
    L = open(FET + r["file"], encoding="utf-8").read().split("\n")
    text = L[r["line"]-1]
    ok = r["quote"] in text
    print(f"{rid} file={r['file']} line={r['line']} quote_substring={ok}")
    print(f"   pin line : {text.strip()}")
    print(f"   prev     : {L[r['line']-2].strip()}")
    print(f"   next     : {L[r['line']].strip()}")
    if not ok:
        print("   !! quote not a substring")
# wl_keyboard interface span in the wayland pin
X = open(FET + "wayland-1.26.0-wayland.xml", encoding="utf-8").read().split("\n")
start = next(i+1 for i,l in enumerate(X) if '<interface name="wl_keyboard"' in l)
end = next(i+1 for i,l in enumerate(X) if i+1>start and l.strip()=="</interface>")
print("wl_keyboard interface lines", start, end, "E04 2732 inside:", start<=2732<=end, "K17 2741 inside:", start<=2741<=end)
