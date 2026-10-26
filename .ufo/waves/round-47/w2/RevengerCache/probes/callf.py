import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("c2", "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r47-terminal-entry.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
repo, rev, base = sys.argv[1], sys.argv[2], sys.argv[3]
text = m.show(repo, rev, m.ENTRY).decode("utf-8", "replace")
lines = m.unfenced(text)
print("ENTRY lines scanned:", len(lines))
print("clause_f returned:", m.clause_f(repo, rev, base, lines, "xdg-terminal-selection-r47.md"))
