#!/usr/bin/env python3
"""Round-92 C1 L1 mutants of the candidate: each restores one wrong belief about xdg-mime 1.2.1."""
import json, sys
M = [
 ("M01", "lowercase of the desktop name skipped", 'prefix = bytes(c + 32 if 65 <= c <= 90 else c for c in desktop) + b"-" if desktop else b""', 'prefix = desktop + b"-" if desktop else b""'),
 ("M02", "plain mimeapps.list not tried after desktop files", 'for desktop in expand(ifs_split(xcd, b":"), self.cwd) + [b""]:', 'for desktop in expand(ifs_split(xcd, b":"), self.cwd):'),
 ("M03", "other group header does not end [Default Applications]", '                elif ln.startswith(b"["):\n                    indefault = False', '                elif ln.startswith(b"[") and False:\n                    indefault = False'),
 ("M04", "header must equal the line", 'if ln.startswith(b"[Default Applications]"):', 'if ln == b"[Default Applications]":'),
 ("M05", "last matching line in a file wins", 'elif result is None and indefault and ln.startswith(pre):', 'elif indefault and ln.startswith(pre):'),
 ("M06", "key compared after stripping leading space", 'elif result is None and indefault and ln.startswith(pre):', 'elif result is None and indefault and ln.lstrip().startswith(pre):'),
 ("M07", "vendor is the text before the first dash", 'vendor = desktop[:desktop.rfind(b"-")]', 'vendor = desktop[:desktop.find(b"-")]'),
 ("M08", "no subdirectory search", 'indirs = [d + b"/applications/"] + self.subdirs(d + b"/applications/") + [d + b"/applnk/"] + \\', 'indirs = [d + b"/applications/"] + [d + b"/applnk/"] + \\'),
 ("M09", "builtins resolved through PATH", 'if s in KEYWORDS or s in BUILTINS or s in FUNCTIONS:', 'if s in KEYWORDS or s in FUNCTIONS:'),
 ("M10", "Exec[locale]= lines not matched", 'EXEC = re.compile(rb"^Exec(\\[[^]=]*\\])?=")', 'EXEC = re.compile(rb"^Exec=")'),
 ("M11", "read without backslash processing", '        if c == 0x5C:\n            if i + 1 >= len(text):', '        if c == 0x5C and False:\n            if i + 1 >= len(text):'),
 ("M12", "echo options not honoured", '    if re.fullmatch(rb"-[neE]+", arg):', '    if False:'),
 ("M13", "slash names need no execute bit", 'return name if (os.access(q, os.X_OK) and not os.path.isdir(q)) else b""', 'return name if os.path.exists(q) else b""'),
 ("M14", "PATH search accepts non-executable files", 'if os.path.isfile(q) and os.access(q, os.X_OK):', 'if os.path.isfile(q):'),
 ("M15", "a resolved name always exists", 'return cmd != b"" and os.path.exists(self.p(cmd))', 'return cmd != b""'),
 ("M16", "a bad first desktop file does not stop the search", '                cmd = self.command_v(read_first(text))\n                return self.exists_path(cmd)', '                cmd = self.command_v(read_first(text))\n                if self.exists_path(cmd):\n                    return True\n                file_path = b""'),
 ("M17", "XDG_MENU_PREFIX ignored", 'for prefix in (self.get("XDG_MENU_PREFIX"), b""):', 'for prefix in (b"",):'),
 ("M18", "cut takes the last = field", 'v = parts[1] if len(parts) > 1 else first', 'v = parts[-1] if len(parts) > 1 else first'),
 ("M19", "dot is literal in the type", '        if c == b".":\n            out += b"."', '        if c == b".":\n            out += b"\\\\."'),
 ("M20", "grep anchored at line start", 'return [ln for ln in lines_of(data) if rx.search(ln)]', 'return [ln for ln in lines_of(data) if rx.match(ln)]'),
 ("M21", "an empty cache value stops the search", '                if v:\n                    return echo_out(v)', '                return echo_out(v) if v else b""'),
 ("M22", "InitialPreference ties go to the last file", 'if v is not None and v > preference:', 'if v is not None and v >= preference:'),
 ("M23", "test integers take no trailing whitespace", 'm = re.fullmatch(rb"[ \\t\\n\\r\\x0b\\x0c]*([+-]?)([0-9]+)[ \\t\\n\\r\\x0b\\x0c]*", s)', 'm = re.fullmatch(rb"[ \\t\\n\\r\\x0b\\x0c]*([+-]?)([0-9]+)", s)'),
 ("M24", "only InitialPreference= at line start counts", 'if b"InitialPreference=" in ln:', 'if ln.startswith(b"InitialPreference="):'),
 ("M25", "LXQt answered like any session", '            return None, 3', '            pass'),
 ("M26", "flatpak-info not considered", 'if os.path.isfile(self.p(self.get("XDG_RUNTIME_DIR") + b"/flatpak-info")):', 'if False:'),
 ("M27", "a type without slash is queried", 'if mime == b"" or mime.startswith(b"-") or b"/" not in mime:', 'if mime == b"" or mime.startswith(b"-"):'),
 ("M29", "CR stripped from mimeapps values", 'result = cmdsub(result + b"\\n") if result is not None else b""', 'result = cmdsub(result.rstrip(b"\\r") + b"\\n") if result is not None else b""'),
 ("M30", "hidden subdirectories searched", 'out = [prefix + n + b"/" for n in names if not n.startswith(b".") and os.path.isdir(os.path.join(base, fs(n)))]', 'out = [prefix + n + b"/" for n in names if os.path.isdir(os.path.join(base, fs(n)))]'),
 ("M31", "basename accepts a leading dash", '    if s.startswith(b"-") and s != b"-":\n        return b""', '    if False:\n        return b""'),
 ("M32", "unquoted words are not globbed", '    if not re.search(rb"(?:^|[^\\\\])(?:\\\\\\\\)*[*?[]", word):\n        return [word]', '    if True:\n        return [word]'),
 ("M33", "no recursion into applications subdirectories for MimeType scan", '            if os.path.isdir(self.p(sub)):\n                out += self.search_desktop_file(rx, sub)', '            if False:\n                out += self.search_desktop_file(rx, sub)'),
 ("M34", "hidden .desktop files scanned", 'out = [prefix + n for n in names if not n.startswith(b".") and n.endswith(b".desktop")]', 'out = [prefix + n for n in names if n.endswith(b".desktop")]'),
 ("M35", "file names split only on newline", '            for x in expand(ws_split(self.search_desktop_file(rx2, d + b"/applications")), self.cwd):', '            for x in expand([y for y in self.search_desktop_file(rx2, d + b"/applications").split(b"\\n") if y], self.cwd):'),
 ("M37", "defaults.list answer needs no '=' cut", 'parts = first.split(b"=")', 'parts = [b"", first.split(b":", 1)[-1].split(b"=", 1)[-1]]'),
 ("M38", "applnk not searched", '                elif readable(self.p(d + b"/applnk/" + vendor + b"/" + rest)):', '                elif False:'),
 ("M39", "a data dir must hold applications/ (applnk alone not enough)", 'if not ((d != b"" and os.path.isdir(self.p(d + b"/applications"))) or os.path.isdir(self.p(d + b"/applnk"))):', 'if not (d != b"" and os.path.isdir(self.p(d + b"/applications"))):'),
 ("M40", "Exec's first word split on spaces only after unescaping nothing (quotes stripped)", '    return cmdsub(echo_out(bytes(first)))', '    return cmdsub(echo_out(bytes(first).strip(b\'"\')))'),
]
tool = open(sys.argv[1]).read()
out = []
for i, d, f, r in M:
    n = tool.count(f)
    if n != 1:
        sys.exit(f"{i}: find occurs {n} times")
    out.append({"id": i, "what": d, "find": f, "replace": r})
json.dump({"mutants": out}, open(sys.argv[2], "w"), indent=1)
print(f"wrote {len(out)} mutants")
