#!/usr/bin/env python3
"""Build the w2 C1 attack mutants from the FROZEN tool (l1-draft/mado-terminal.py, sha256 1dfde36c...).
Each mutant is the frozen tool with ONE anchored change; every anchor must occur exactly once."""
import hashlib
import os
import sys

TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/mado-terminal.py"
OUT = "/fast/scratch/hyaku/mado-r48/RevC1Counter/mut"
src = open(TOOL, "rb").read().decode()

P = {}
P["trust-any"] = (
    "        if self.gen_hash() != fields[0] or not self.command_v(fields[1]):\n",
    "        if not self.command_v(fields[1]):\n")
P["no-line-limit"] = (
    "            if n == 50:\n"
    "                self.t(\"cache: %s invalid (line limit 50)\" % p)\n"
    "                return \"invalid\"\n",
    "")
P["delegate-ls"] = (
    "        listing = ls_lRL(operands)\n",
    "        import shutil, subprocess\n"
    "        _e = {\"LC_ALL\": \"C\", \"LANG\": \"C\", \"PATH\": self.env.get(\"PATH\", \"/usr/bin:/bin\")}\n"
    "        _ls = shutil.which(\"ls\") or \"/usr/bin/ls\"\n"
    "        listing = subprocess.run([_ls, \"-LRl\"] + operands, capture_output=True, env=_e).stdout\n")
P["explain-cmd-const"] = (
    "    print(\"MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s\" % (sel, path, argv0, cache, verdict))\n",
    "    print(\"MADO_TERM: selected=%s path=%s cmd=%s cache=%s verdict=%s\" % (sel, path, \"-\", cache, verdict))\n")
P["writes-cache"] = (
    "        self.read_config_paths()\n"
    "        self.find_entry_paths()\n"
    "        return self.find_entry()\n",
    "        self.read_config_paths()\n"
    "        self.find_entry_paths()\n"
    "        ok = self.find_entry()\n"
    "        if ok and check_bool(self.cache_enabled, self.err):\n"
    "            self._save_cache()\n"
    "        return ok\n"
    "\n"
    "    def _save_cache(self):\n"
    "        \"\"\"CONTROL writes-cache: save_cache (x:300-340) reproduced - this tool writes the cache file.\"\"\"\n"
    "        try:\n"
    "            with open(self.cache_file, \"wb\") as fh:\n"
    "                fh.write(b\"0\" * 32 + b\"\\nfoot\\n\" + CACHE_END.encode() + b\"\\n\")\n"
    "        except OSError:\n"
    "            pass\n")
P["content-cold"] = (
    "    if \"content\" in pdata:\n"
    "        if not first:\n"
    "            call_b(pdelim)\n"
    "        try:\n"
    "            text = read_file(r.entry_path)\n",
    "    if \"content\" in pdata:\n"
    "        if not first:\n"
    "            call_b(pdelim)\n"
    "        _cpath = r.entry_path\n"
    "        if r.cache == \"hit\":\n"
    "            # CHEAP VARIANT: content ignores the cached entry; it is read from the cold selection\n"
    "            _cold = Resolver(dict(env, XTE_CACHE_ENABLED=\"false\"), cwd)\n"
    "            try:\n"
    "                if _cold.select():\n"
    "                    _cpath = _cold.entry_path\n"
    "            except Exit:\n"
    "                pass\n"
    "        try:\n"
    "            text = read_file(_cpath)\n")

P["content-cold2"] = (
    "    if \"content\" in pdata:\n"
    "        if not first:\n"
    "            call_b(pdelim)\n"
    "        try:\n"
    "            text = read_file(r.entry_path)\n",
    "    if \"content\" in pdata:\n"
    "        if not first:\n"
    "            call_b(pdelim)\n"
    "        _cpath = r.entry_path\n"
    "        if r.cache == \"hit\" and os.path.exists(r.entry_path):\n"
    "            # CHEAP VARIANT 2: a LIVE cached path, content still taken from the cold selection\n"
    "            _cold = Resolver(dict(env, XTE_CACHE_ENABLED=\"false\"), cwd)\n"
    "            try:\n"
    "                if _cold.select():\n"
    "                    _cpath = _cold.entry_path\n"
    "            except Exit:\n"
    "                pass\n"
    "        try:\n"
    "            text = read_file(_cpath)\n")

os.makedirs(OUT, exist_ok=True)
for name, (old, new) in P.items():
    n = src.count(old)
    if n != 1:
        sys.exit("ANCHOR %s occurs %d times" % (name, n))
    out = src.replace(old, new)
    p = os.path.join(OUT, name + ".py")
    with open(p, "wb") as fh:
        fh.write(out.encode())
    os.chmod(p, 0o755)
    print("%-18s %s lines=%d" % (name, hashlib.sha256(out.encode()).hexdigest(), out.count("\n") + 1))
