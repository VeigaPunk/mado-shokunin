import difflib, json, os, sys
ROOT = "/fast/scratch/hyaku/mado-r55/R55W2MutTool3"
SRC = os.path.join(ROOT, "tools/mado-kbdopts.py")
OUT = os.path.join(ROOT, "mutants")
src = open(SRC, encoding="utf-8").read()
# (id, class, description, old, new)
M = [
 ("M01","focus","stray `}` on empty stack crashes (no underflow guard)",
  "                if stack:\n                    stack.pop()", "                stack.pop()"),
 ("M02","focus","current device not forgotten when stack empties",
  "                if not stack:\n                    cur = None", "                if False:\n                    cur = None"),
 ("M03","focus","current device forgotten on every pop (nested block close)",
  "                if not stack:\n                    cur = None", "                if True:\n                    cur = None"),
 ("M04","focus","`}` clears the whole stack instead of popping one level",
  "                    stack.pop()", "                    stack.clear()"),
 ("M05","focus","category stack not reset at each file start",
  "    stack, cur = [], None", "    stack, cur = st.__dict__.setdefault('stack', []), None"),
 ("M06","focus","device name keeps trailing `#` comment",
  "cur = rhs.split(\"#\", 1)[0].strip(WS)", "cur = rhs.strip(WS)"),
 ("M07","focus","key line before device name not counted unsupported",
  "        elif cur is None:\n            st.unsupported += 1", "        elif cur is None:\n            st.unsupported += 0"),
 ("M08","focus","nested `name =` line renames the current device",
  "        if in_device and lhs == \"name\":", "        if stack and lhs == \"name\":"),
 ("M09","focus","device-key relevance extends to nested blocks under device",
  "        in_device = stack == [\"device\"]", "        in_device = bool(stack) and stack[0] == \"device\""),
 ("M10","focus","block-opening line keeps whitespace before `{`",
  "                stack.append(line[:-1].strip(WS))", "                stack.append(line[:-1])"),
 ("M11","focus","full-line `#` comments not skipped",
  "        if not line or line[0] == \"#\":", "        if not line:"),
 ("M12","focus","assignment split on LAST `=` not first",
  "        lhs, rhs = (s.strip(WS) for s in line.split(\"=\", 1))", "        lhs, rhs = (s.strip(WS) for s in line.rsplit(\"=\", 1))"),
 ("M13","focus","`}` prefix match pops (`}x` treated as close)",
  "            if line == \"}\":", "            if line.startswith(\"}\"):"),
 ("M14","focus","KEY uses only the innermost stack frame",
  "        key = \":\".join(stack + [lhs])", "        key = \":\".join(stack[-1:] + [lhs])"),
 ("M15","focus","RHS `$` check dropped (only LHS `$` ignored, RHS `$` not unsupported)",
  "        if bracket or \"$\" in line or", "        if bracket or"),
 ("M16","focus","VT and FF not stripped from line ends",
  r'WS = " \t\r\n\v\f"', r'WS = " \t\r\n"'),
 ("M17","equiv-probe","`source` LHS not ignored (expected equivalent: source never relevant)",
  "        if lhs.startswith(\"$\") or lhs == \"source\":", "        if lhs.startswith(\"$\"):"),
 ("M18","equiv-probe","`$` LHS not ignored (expected equivalent: `$`-LHS can never be relevant)",
  "        if lhs.startswith(\"$\") or lhs == \"source\":", "        if lhs == \"source\":"),
 ("M19","equiv-probe","bracket line not counted unsupported by the bracket check (expected equivalent: cur is None on bracket keys)",
  "        if bracket or \"$\" in line", "        if \"$\" in line"),
 ("M20","control","bracket keys never relevant (F10 must kill)",
  "            or (bracket and key.rsplit(\":\", 1)[-1] in NAMES)", "            or False"),
 ("M21","control","device blocks merge replaced by overwrite (F09 must kill)",
  "            st.devices.setdefault(cur, {})", "            st.devices[cur] = {}"),
]
os.makedirs(OUT, exist_ok=True)
index = []
for mid, cls, desc, old, new in M:
    n = src.count(old)
    assert n == 1, (mid, n)
    mut = src.replace(old, new, 1)
    assert mut != src
    d = os.path.join(OUT, mid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "mado-kbdopts.py"), "w", encoding="utf-8") as f:
        f.write(mut)
    diff = "".join(difflib.unified_diff(src.splitlines(True), mut.splitlines(True), "original/mado-kbdopts.py", "%s/mado-kbdopts.py" % mid))
    with open(os.path.join(d, "edit.diff"), "w", encoding="utf-8") as f:
        f.write(diff)
    index.append({"id": mid, "class": cls, "desc": desc})
json.dump(index, open(os.path.join(OUT, "index.json"), "w"), indent=1)
print("generated", len(index))
