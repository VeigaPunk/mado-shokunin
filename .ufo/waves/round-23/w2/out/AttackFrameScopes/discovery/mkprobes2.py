import json, sys
from pathlib import Path
H = "import subprocess\n"
PROBES = {
 "Q01CtlP11SingleInvocation": H + (
  "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
  'f = outer(["pacman", "-Q", "w2-q01-first"])\nf()\n'),
 "Q02CtlP13NoSiblingBinder": H + (
  'argv = ["pacman", "-S", "w2-q02-early"]\n'
  "def outer():\n    def inner():\n        subprocess.run(argv)\n    return inner\n"
  'f = outer()\nargv = ["pacman", "-Q", "w2-q02-late"]\nf()\n'),
 "Q03ConflationDirectCapture": H + (
  "def outer(argv):\n    def inner():\n        subprocess.run(argv)\n    return inner\n"
  'f = outer(["pacman", "-Q", "w2-q03-first"])\nouter(["pacman", "-S", "w2-q03-second"])\nf()\n'),
 "Q04ConflationMethodFrame": H + (
  "class Box:\n    def make(self, argv):\n        def leaf():\n            subprocess.run(argv)\n        def inner():\n            leaf()\n        return inner\n"
  'box = Box()\nf = box.make(["pacman", "-Q", "w2-q04-first"])\nbox.make(["pacman", "-S", "w2-q04-second"])\nf()\n'),
 "Q05ConflationSecondAssignedNeverCalled": H + (
  "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
  'f = outer(["pacman", "-Q", "w2-q05-first"])\ng = outer(["pacman", "-S", "w2-q05-second"])\nf()\n'),
 "Q06ConflationBothCalled": H + (
  "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
  'f = outer(["pacman", "-Q", "w2-q06-first"])\ng = outer(["pacman", "-Q", "w2-q06-second"])\nf()\ng()\n'),
 "Q07ConflationViaForwarder": H + (
  "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
  "def forward(cb):\n    argv = [\"pacman\", \"-S\", \"w2-q07-forward\"]\n    cb()\n"
  'f = outer(["pacman", "-Q", "w2-q07-first"])\nouter(["pacman", "-S", "w2-q07-second"])\nforward(f)\n'),
 "Q08NestedClassAttrBinderFreezesGlobal": H + (
  'argv = ["pacman", "-S", "w2-q08-early"]\n'
  "def outer():\n    class Cfg:\n        argv = [\"pacman\", \"-S\", \"w2-q08-classattr\"]\n    def inner():\n        subprocess.run(argv)\n    return inner\n"
  'f = outer()\nargv = ["pacman", "-Q", "w2-q08-late"]\nf()\n'),
 "Q09NestedForBinderFreezesGlobal": H + (
  'argv = ["pacman", "-S", "w2-q09-early"]\n'
  "def outer():\n    def other():\n        for argv in [[\"pacman\", \"-S\", \"w2-q09-loop\"]]:\n            pass\n    def inner():\n        subprocess.run(argv)\n    return inner\n"
  'f = outer()\nargv = ["pacman", "-Q", "w2-q09-late"]\nf()\n'),
 "Q10MatchCaptureNotOwn": H + (
  'argv = ["pacman", "-S", "w2-q10-module"]\n'
  "def outer():\n    match [\"pacman\", \"-Q\", \"w2-q10-match\"]:\n        case argv:\n            pass\n    def inner():\n        subprocess.run(argv)\n    inner()\n"
  "outer()\n"),
 "Q11WithAsNotOwn": H + (
  'argv = ["pacman", "-S", "w2-q11-module"]\n'
  "class Ctx:\n    def __enter__(self):\n        return [\"pacman\", \"-Q\", \"w2-q11-with\"]\n    def __exit__(self, *exc):\n        return False\n"
  "def outer():\n    with Ctx() as argv:\n        pass\n    def inner():\n        subprocess.run(argv)\n    inner()\n"
  "outer()\n"),
 "Q12NestedDefBinderNoRebind": H + (
  'argv = ["pacman", "-Q", "w2-q12-module"]\n'
  "def third(cb):\n    argv = [\"pacman\", \"-S\", \"w2-q12-third\"]\n    cb()\n"
  "def outer():\n    def other():\n        argv = [\"pacman\", \"-S\", \"w2-q12-other\"]\n    def inner():\n        subprocess.run(argv)\n    third(inner)\n"
  "outer()\n"),
 "Q13ConflationRecursiveShape": H + (
  "def outer(argv, again):\n    def leaf():\n        subprocess.run(argv)\n    if again:\n        outer([\"pacman\", \"-S\", \"w2-q13-inner-call\"], False)\n    leaf()\n"
  'outer(["pacman", "-Q", "w2-q13-outer-call"], True)\n'),
 "Q14ConflationSecondCallInsideOtherHelper": H + (
  "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
  "def warm():\n    outer([\"pacman\", \"-S\", \"w2-q14-warm\"])\n"
  'f = outer(["pacman", "-Q", "w2-q14-first"])\nwarm()\nf()\n'),
}
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for name, code in PROBES.items():
    rec = {"type": "message", "message": {"role": "assistant", "content": [{"type": "toolCall", "name": "eval", "id": name + "-0", "arguments": {"language": "py", "reset": False, "code": code}}]}}
    (out / (name + ".jsonl")).write_text(json.dumps(rec) + "\n")
