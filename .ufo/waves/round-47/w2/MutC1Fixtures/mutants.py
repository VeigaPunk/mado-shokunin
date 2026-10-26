"""Seat MutC1Fixtures: 22 one-rule mutants of the L1 reference mado-terminal.py.

Each entry is (id, old, new); the mutant is REF.replace(old, new, 1).
None duplicates the 17 V-* controls of ctl/run-c1-controls.py.
"""

MUTANTS = [
    ("I-SPLIT-IFS-TRAILING",
     '    parts = s.split(ch)\n    if parts[-1] == "":\n        parts.pop()\n    return parts',
     '    parts = s.split(ch)\n    return parts'),

    ("I-READSPLIT-APPID",
     '            appid = read_split(a.split("\\n", 1)[0], "=", 2)[1]',
     '            appid = a.split("=", 1)[1] if "=" in a else ""'),

    ("I-TOK-QUOTED-ESC-NONSPECIAL",
     '        if quoted and ch == "\\\\":\n            if rem == "":\n                return "".join(usep), False\n'
     '            usep.append(rem[0])\n            rem = rem[1:]\n            continue',
     '        if quoted and ch == "\\\\":\n            if rem == "":\n                return "".join(usep), False\n'
     '            if rem[0] not in \'"\\\\\':\n                usep.append("\\\\")\n'
     '            usep.append(rem[0])\n            rem = rem[1:]\n            continue'),

    ("I-EXPAND-UNKNOWN-KEEP",
     '        if c in mp and c != "":\n            out.append(mp[c])\n            rem = rem[1:]',
     '        if c in mp and c != "":\n            out.append(mp[c])\n            rem = rem[1:]\n'
     '        elif c != "":\n            out.append("\\\\")'),

    ("I-NOTSHOWIN-LISTED",
     '        if m(key, "NotShowIn*=*"):\n            if not de_checks:\n                return True, ""',
     '        if m(key, "NotShowIn*=*"):\n            if False:\n                return True, ""'),

    ("I-TRYEXEC-ABS-CWD",
     '        if "/" in name:\n            p = name if name.startswith("/") else os.path.join(self.cwd, name)\n'
     '            return self._execable(p)',
     '        if "/" in name:\n            return self._execable(os.path.join(self.cwd, name))'),

    ("I-PATH-EMPTY-SKIP",
     '        for d in path.split(":"):\n            base = d if d else self.cwd',
     '        for d in path.split(":"):\n            if not d:\n                continue\n            base = d'),

    ("I-ALIAS-EXCLUDED-UNREG",
     '        for path, eid in found:\n            self.aliases[eid] = path\n            if eid in self.excluded:\n'
     '                continue\n            self.fallback.insert(0, eid)',
     '        for path, eid in found:\n            if eid in self.excluded:\n                continue\n'
     '            self.aliases[eid] = path\n            self.fallback.insert(0, eid)'),

    ("I-CONTENT-LAST-NL",
     '        for line in read_lines(text, False):\n            out.append(line + "\\n")',
     '        ls = read_lines(text, False)\n        for line in ls[:-1]:\n            out.append(line + "\\n")\n'
     '        if ls:\n            out.append(ls[-1])'),

    ("I-TEST-WITH-PRINT",
     '    if not ("cmd" in pdata or not pdata):',
     '    if not ("cmd" in pdata or not pdata) and not test:'),

    ("I-PRINTCMD-EMPTY-DELIM",
     '            call_b(pcdelim if pcdelim != "" else "\\\\n")',
     '            call_b(pcdelim)'),

    ("I-READSPLIT-MULTI-TRAILING",
     '    if rest.endswith(ch) and ch not in rest[:-1]:\n        rest = rest[:-1]',
     '    if rest.endswith(ch):\n        rest = rest[:-1]'),

    ("I-ACTION-ID-UNDERSCORE",
     '    return all(c.isascii() and (c.isalnum() or c == "-") for c in s)',
     '    return all(c.isascii() and (c.isalnum() or c in "-_") for c in s)'),

    ("I-COMMANDV-FUNCTIONS",
     '        if name in self.aliases or name in SCRIPT_FUNCTIONS or name in BASH_BUILTINS or name in BASH_KEYWORDS:',
     '        if name in self.aliases or name in BASH_BUILTINS or name in BASH_KEYWORDS:'),

    ("I-EXPLAIN-CACHE-SWAP",
     '        cache = "present" if os.path.isfile(r.cache_file) else "absent"',
     '        cache = "absent" if os.path.isfile(r.cache_file) else "present"'),

    ("I-LIST-UNREADABLE-SKIP",
     '            except OSError:\n                self.t("list %s: unreadable -> the resolver exits 1 (errexit)" % p)\n'
     '                self.err("%s: Permission denied" % p)\n                raise Exit(1)',
     '            except OSError:\n                self.t("list %s: unreadable" % p)\n                continue'),

    ("I-TOK-SQUOTE-IN-DQUOTE",
     '        if quoted and (ch in SPACE or ch in "\'><~|&;*?#()"):',
     '        if quoted and (ch in SPACE or ch in "><~|&;*?#()"):'),

    ("I-EXECARG-EQ-ONLY",
     '        if a == "-e" or a == r.execarg:',
     '        if a == "-e":'),

    ("I-HOLD-IGNORE-FLAG",
     '    if r.holdarg and hold:',
     '    if r.holdarg:'),

    ("I-EXECARG-EMPTY-INSERT",
     '    if argv and r.execarg != "":\n        argv.insert(0, r.execarg)',
     '    if argv:\n        argv.insert(0, r.execarg)'),

    ("I-DESKTOP-ORDER-REV",
     '            for dk in self.desktops_lower:\n                self.configs.append(d + "/" + dk + "-xdg-terminals.list")',
     '            for dk in reversed(self.desktops_lower):\n                self.configs.append(d + "/" + dk + "-xdg-terminals.list")'),

    ("I-DIRECTIVE-LAST-WINS",
     '                if line == "/execarg_compat" or line == "/execarg_strict":\n'
     '                    if not self.compat_configured:\n'
     '                        self.compat = "true" if line == "/execarg_compat" else "false"\n'
     '                        self.compat_configured = True\n                    continue',
     '                if line == "/execarg_compat" or line == "/execarg_strict":\n'
     '                    self.compat = "true" if line == "/execarg_compat" else "false"\n                    continue'),
]
