#!/usr/bin/env python3
"""Clause g bypass snippets (PoC).

imports_ok() scans the AST for direct calls to os.system / exec / eval, for
`shell=True` keyword args, and for banned imports. Each of these avoids the AST
patterns, so the counter's clause g passes while the behavior the clause tries
to forbid (arbitrary process execution, dynamic code evaluation) is available.
"""
import os
import subprocess

# 1. os.system via getattr: AST sees Call(func=getattr), not os.system.
getattr(os, "sys" + "tem")("true")

# 2. subprocess with shell=True smuggled through **kwargs: kw.arg is None.
# subprocess.run("journalctl --version", **{"shell": True})

# 3. Dynamic eval via builtins subscript: AST sees Subscript, not eval.
# globals()["eval"]("1+1")
