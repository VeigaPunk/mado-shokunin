#!/usr/bin/env python3
"""Round-92 C2 L1 mutants: each reverts or weakens one of the five round-92 fixes."""
import json, sys
M = [
 ("N01", "rev mode enumerates blobs only (F1 back)", '        return [p for p in list(self.sizes) + sorted(self.links) + sorted(self.others) if p.startswith(".ufo/waves/")]', '        return [p for p in self.sizes if p.startswith(".ufo/waves/")]'),
 ("N15", "rev mode ignores gitlinks and trees", '        return [p for p in list(self.sizes) + sorted(self.links) + sorted(self.others) if p.startswith(".ufo/waves/")]', '        return [p for p in list(self.sizes) + sorted(self.links) if p.startswith(".ufo/waves/")]'),
 ("N16", "worktree lists no dispatch-named directories", '            for f in files + [x for x in dirs if DISPATCH.match(', '            for f in files + [x for x in [] if DISPATCH.match('),
 ("N17", "a dispatch-named tree is not recorded in rev mode", '                if DISPATCH.match(prefix):\n                    self.others.add(prefix)', '                if False:\n                    self.others.add(prefix)'),
 ("N02", "rev dispatch symlink accepted", '        if path in self.links:\n            raise SetupError(f"{path}: dispatch is a symlink, not a regular file")\n        if path not in self.sizes:', '        if False:\n            raise SetupError(f"{path}: dispatch is a symlink, not a regular file")\n        if path not in self.sizes and path not in self.links:'),
 ("N03", "worktree dispatch symlink accepted", '        if os.path.islink(p):\n            raise SetupError(f"{path}: dispatch is a symlink, not a regular file")', '        if False:\n            raise SetupError(f"{path}: dispatch is a symlink, not a regular file")'),
 ("N04", "worktree dispatch type unchecked (F4 back)", '        if not stat.S_ISREG(st.st_mode):\n            raise SetupError(f"{path}: dispatch is not a regular file")', '        if False:\n            raise SetupError(f"{path}: dispatch is not a regular file")'),
 ("N05", "dispatch check never called", '            tree.check_dispatch(p)\n', '\n'),
 ("N06", "tokens printed raw (F2 back)", '    if s and all(33 <= ord(ch) <= 126 for ch in s) and not s.startswith(\'"\'):\n        return s', '    if True:\n        return s'),
 ("N07", "JSON tokens not ASCII-escaped", '    return json.dumps(s, ensure_ascii=True).replace(" ", "\\\\u0020")', '    return json.dumps(s, ensure_ascii=False).replace(" ", "\\\\u0020")'),
 ("N08", "spaces left inside JSON tokens", '    return json.dumps(s, ensure_ascii=True).replace(" ", "\\\\u0020")', '    return json.dumps(s, ensure_ascii=True)'),
 ("N09", "repeated --round counted again (F3 back)", '        rounds = sorted(set(rounds))  # a repeated --round counts once (r91 F3)', '        rounds = list(rounds)'),
 ("N10", "containment test always true (F5 back)", '        return r == self.real or r.startswith(self.real + os.sep)', '        return True'),
 ("N11", "report containment unchecked", '        return os.path.islink(os.path.join(self.repo, path)) or not self.inside(path)', '        return os.path.islink(os.path.join(self.repo, path))'),
 ("N12", "name never tokenised", '                name = tok(str(t.get("name", "?")) if isinstance(t, dict) else "?")', '                name = str(t.get("name", "?")) if isinstance(t, dict) else "?"'),
 ("N13", "path never tokenised for SR01/SR02", '                size = tree.size(rp)\n                rp = tok(rp)', '                size = tree.size(rp)'),
 ("N14", "prefix containment by string (sibling dir passes)", '        return r == self.real or r.startswith(self.real + os.sep)', '        return r.startswith(self.real)'),
]
s = open(sys.argv[1]).read()
out = []
for i, d, f, r in M:
    n = s.count(f)
    if n != 1:
        sys.exit(f"{i}: find occurs {n} times")
    out.append({"id": i, "what": d, "find": f, "replace": r})
json.dump({"mutants": out}, open(sys.argv[2], "w"), indent=1)
print(f"wrote {len(out)} mutants")
