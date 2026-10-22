#!/usr/bin/env python3
"""Write scratch probe fixtures in the repair-set JSONL shape."""
import json, sys
from pathlib import Path

H = "import subprocess\n"
PROBES = {
    # --- class body ---
    "P01ClassBodyHelperCalledInBody": H + (
        'argv = ["pacman", "-Q", "w2-p01-global"]\n'
        "class Box:\n"
        '    argv = ["pacman", "-S", "w2-p01-classattr"]\n'
        "    def helper():\n"
        "        subprocess.run(argv)\n"
        "    helper()\n"),
    "P02ClassMethodSkipsClassScope": H + (
        'argv = ["pacman", "-Q", "w2-p02-global"]\n'
        "class Box:\n"
        '    argv = ["pacman", "-S", "w2-p02-classattr"]\n'
        "    def go(self):\n"
        "        subprocess.run(argv)\n"
        "Box().go()\n"),
    "P03ClassInFunctionSkipsClassScope": H + (
        'argv = ["pacman", "-S", "w2-p03-module"]\n'
        "def make():\n"
        '    argv = ["pacman", "-Q", "w2-p03-enclosing"]\n'
        "    class Box:\n"
        '        argv = ["pacman", "-S", "w2-p03-classattr"]\n'
        "        def go(self):\n"
        "            subprocess.run(argv)\n"
        "    Box().go()\n"
        "make()\n"),
    # --- static/classmethod with caller shadow ---
    "P04StaticAndClassMethodCallerShadow": H + (
        'argv = ["pacman", "-Q", "w2-p04-global"]\n'
        "class Box:\n"
        "    @staticmethod\n"
        "    def stat():\n"
        "        subprocess.run(argv)\n"
        "    @classmethod\n"
        "    def klass(cls):\n"
        "        subprocess.run(argv)\n"
        "def caller():\n"
        '    argv = ["pacman", "-S", "w2-p04-caller"]\n'
        "    Box.stat()\n"
        "    Box.klass()\n"
        "caller()\n"),
    "P05StaticMethodCallerShadowsCallable": H + (
        "def launch():\n"
        '    subprocess.run(["pacman", "-Q", "w2-p05-module-launch"])\n'
        "class Box:\n"
        "    @staticmethod\n"
        "    def go():\n"
        "        launch()\n"
        "def caller():\n"
        "    def launch():\n"
        '        subprocess.run(["pacman", "-S", "w2-p05-caller-launch"])\n'
        "    Box.go()\n"
        "caller()\n"),
    "P06ClassMethodViaInstanceInFunctionShadow": H + (
        'argv = ["pacman", "-Q", "w2-p06-global"]\n'
        "class Box:\n"
        "    @classmethod\n"
        "    def klass(cls):\n"
        "        subprocess.run(argv)\n"
        "def caller():\n"
        '    argv = ["pacman", "-S", "w2-p06-caller"]\n'
        "    box = Box()\n"
        "    box.klass()\n"
        "caller()\n"),
    # --- nested two deep called from a third function ---
    "P07TwoDeepCallbackThirdShadow": H + (
        'argv = ["pacman", "-S", "w2-p07-module"]\n'
        "def third(cb):\n"
        '    argv = ["pacman", "-S", "w2-p07-third"]\n'
        "    cb()\n"
        "def outer(argv):\n"
        "    def mid():\n"
        "        def inner():\n"
        "            subprocess.run(argv)\n"
        "        third(inner)\n"
        "    mid()\n"
        'outer(["pacman", "-Q", "w2-p07-outer"])\n'),
    "P08TwoDeepMidShadows": H + (
        "def third(cb):\n"
        '    argv = ["pacman", "-S", "w2-p08-third"]\n'
        "    cb()\n"
        "def outer(argv):\n"
        "    def mid():\n"
        '        argv = ["pacman", "-Q", "w2-p08-mid"]\n'
        "        def inner():\n"
        "            subprocess.run(argv)\n"
        "        third(inner)\n"
        "    mid()\n"
        'outer(["pacman", "-S", "w2-p08-outer"])\n'),
    "P09TwoDeepReadsModuleThirdShadow": H + (
        'argv = ["pacman", "-Q", "w2-p09-module"]\n'
        "def third(cb):\n"
        '    argv = ["pacman", "-S", "w2-p09-third"]\n'
        "    cb()\n"
        "def outer():\n"
        "    def mid():\n"
        "        def inner():\n"
        "            subprocess.run(argv)\n"
        "        third(inner)\n"
        "    mid()\n"
        "outer()\n"),
    "P10TwoDeepReturnedCalledByThird": H + (
        'argv = ["pacman", "-S", "w2-p10-module"]\n'
        "def outer(argv):\n"
        "    def mid():\n"
        "        def inner():\n"
        "            subprocess.run(argv)\n"
        "        return inner\n"
        "    return mid()\n"
        "def third():\n"
        '    argv = ["pacman", "-S", "w2-p10-third"]\n'
        '    f = outer(["pacman", "-Q", "w2-p10-outer"])\n'
        "    f()\n"
        "third()\n"),
    # --- frame identity conflation (same def, two invocations) ---
    "P11FrameConflationSiblingHelper": H + (
        "def outer(argv):\n"
        "    def leaf():\n"
        "        subprocess.run(argv)\n"
        "    def inner():\n"
        "        leaf()\n"
        "    return inner\n"
        'f = outer(["pacman", "-Q", "w2-p11-first"])\n'
        'outer(["pacman", "-S", "w2-p11-second"])\n'
        "f()\n"),
    "P12FrameConflationCallbackLater": H + (
        "def outer(argv, sink):\n"
        "    def leaf():\n"
        "        subprocess.run(argv)\n"
        "    def inner():\n"
        "        leaf()\n"
        "    sink(inner)\n"
        "def call(cb):\n"
        "    cb()\n"
        "def drop(cb):\n"
        "    pass\n"
        'outer(["pacman", "-Q", "w2-p12-called"], call)\n'
        'outer(["pacman", "-S", "w2-p12-dropped"], drop)\n'),
    # --- own_names over-approximation (nested binders counted as own) ---
    "P13NestedDefBinderFreezesGlobal": H + (
        'argv = ["pacman", "-S", "w2-p13-early"]\n'
        "def outer():\n"
        "    def other():\n"
        '        argv = ["pacman", "-S", "w2-p13-other-local"]\n'
        "        return argv\n"
        "    def inner():\n"
        "        subprocess.run(argv)\n"
        "    return inner\n"
        "f = outer()\n"
        'argv = ["pacman", "-Q", "w2-p13-late"]\n'
        "f()\n"),
    "P14ComprehensionBinderFreezesGlobal": H + (
        'argv = ["pacman", "-S", "w2-p14-early"]\n'
        "def outer():\n"
        '    names = [argv for argv in [["pacman", "-S", "w2-p14-comp"]]]\n'
        "    def inner():\n"
        "        subprocess.run(argv)\n"
        "    return inner\n"
        "f = outer()\n"
        'argv = ["pacman", "-Q", "w2-p14-late"]\n'
        "f()\n"),
    "P15NestedDefBinderSiblingLeaf": H + (
        'argv = ["pacman", "-S", "w2-p15-early"]\n'
        "def outer():\n"
        "    def other():\n"
        '        argv = ["pacman", "-S", "w2-p15-other-local"]\n'
        "    def leaf():\n"
        "        subprocess.run(argv)\n"
        "    def inner():\n"
        "        leaf()\n"
        "    return inner\n"
        "f = outer()\n"
        'argv = ["pacman", "-Q", "w2-p15-late"]\n'
        "f()\n"),
    # --- module helper redefined after a forwarder captured it ---
    "P16RedefinedAfterDefaultCapture": H + (
        "def helper():\n"
        '    subprocess.run(["pacman", "-Q", "w2-p16-captured"])\n'
        "def forward(cb=helper):\n"
        "    cb()\n"
        "def helper():\n"
        '    subprocess.run(["pacman", "-S", "w2-p16-redefined"])\n'
        "forward()\n"),
    "P17RedefinedAfterFactoryCapture": H + (
        "def helper():\n"
        '    subprocess.run(["pacman", "-Q", "w2-p17-captured"])\n'
        "def make(cb):\n"
        "    def fwd():\n"
        "        cb()\n"
        "    return fwd\n"
        "fwd = make(helper)\n"
        "def helper():\n"
        '    subprocess.run(["pacman", "-S", "w2-p17-redefined"])\n'
        "fwd()\n"),
    "P18RedefinedGlobalNameLate": H + (
        "def helper():\n"
        '    subprocess.run(["pacman", "-S", "w2-p18-early-def"])\n'
        "def forward():\n"
        "    helper()\n"
        "saved = forward\n"
        "def helper():\n"
        '    subprocess.run(["pacman", "-Q", "w2-p18-late-def"])\n'
        "saved()\n"),
    "P19RedefinedAfterCaptureCallerShadow": H + (
        'argv = ["pacman", "-Q", "w2-p19-global"]\n'
        "def helper():\n"
        "    subprocess.run(argv)\n"
        "def make(cb):\n"
        "    def fwd():\n"
        '        argv = ["pacman", "-S", "w2-p19-fwd"]\n'
        "        cb()\n"
        "    return fwd\n"
        "fwd = make(helper)\n"
        "def helper():\n"
        '    subprocess.run(["pacman", "-S", "w2-p19-redefined"])\n'
        "fwd()\n"),
    "P20CallerLocalDefShadowsModuleHelper": H + (
        "def helper():\n"
        '    subprocess.run(["pacman", "-Q", "w2-p20-module-helper"])\n'
        "def forward():\n"
        "    helper()\n"
        "def caller():\n"
        "    def helper():\n"
        '        subprocess.run(["pacman", "-S", "w2-p20-caller-helper"])\n'
        "    forward()\n"
        "caller()\n"),
    # --- global statement ---
    "P21GlobalDeclReadCallerShadow": H + (
        'argv = ["pacman", "-Q", "w2-p21-global"]\n'
        "def helper():\n"
        "    global argv\n"
        "    subprocess.run(argv)\n"
        "def caller():\n"
        '    argv = ["pacman", "-S", "w2-p21-caller"]\n'
        "    helper()\n"
        "caller()\n"),
    "P22GlobalDeclAssignThenNestedRead": H + (
        'argv = ["pacman", "-S", "w2-p22-early"]\n'
        "def helper():\n"
        "    global argv\n"
        '    argv = ["pacman", "-Q", "w2-p22-set"]\n'
        "def reader():\n"
        "    subprocess.run(argv)\n"
        "def caller():\n"
        '    argv = ["pacman", "-S", "w2-p22-caller"]\n'
        "    helper()\n"
        "    reader()\n"
        "caller()\n"),
    "P23GlobalDeclInHelperClosureSibling": H + (
        'argv = ["pacman", "-S", "w2-p23-early"]\n'
        "def outer():\n"
        "    def setter():\n"
        "        global argv\n"
        '        argv = ["pacman", "-Q", "w2-p23-late"]\n'
        "    def inner():\n"
        "        subprocess.run(argv)\n"
        "    setter()\n"
        "    inner()\n"
        "outer()\n"),
    "P24GlobalDeclHelperThenFactoryLeaf": H + (
        'argv = ["pacman", "-S", "w2-p24-early"]\n'
        "def outer():\n"
        "    global argv\n"
        "    def inner():\n"
        "        subprocess.run(argv)\n"
        "    return inner\n"
        "f = outer()\n"
        'argv = ["pacman", "-Q", "w2-p24-late"]\n'
        "f()\n"),
    "P25GlobalDeclAssignedInOuterLeafLate": H + (
        'argv = ["pacman", "-S", "w2-p25-early"]\n'
        "def outer():\n"
        "    global argv\n"
        '    argv = ["pacman", "-S", "w2-p25-outer"]\n'
        "    def inner():\n"
        "        subprocess.run(argv)\n"
        "    return inner\n"
        "f = outer()\n"
        'argv = ["pacman", "-Q", "w2-p25-late"]\n'
        "f()\n"),
    # --- lambda first resolved in a foreign frame ---
    "P26InlineLambdaToShadowingThird": H + (
        'argv = ["pacman", "-S", "w2-p26-module"]\n'
        "def third(cb):\n"
        '    argv = ["pacman", "-S", "w2-p26-third"]\n'
        "    cb()\n"
        "def outer(argv):\n"
        "    third(lambda: subprocess.run(argv))\n"
        'outer(["pacman", "-Q", "w2-p26-outer"])\n'),
    "P27MethodNestedDefToThird": H + (
        'argv = ["pacman", "-S", "w2-p27-module"]\n'
        "def third(cb):\n"
        '    argv = ["pacman", "-S", "w2-p27-third"]\n'
        "    cb()\n"
        "class Box:\n"
        "    def go(self, argv):\n"
        "        def inner():\n"
        "            subprocess.run(argv)\n"
        "        third(inner)\n"
        'Box().go(["pacman", "-Q", "w2-p27-method"])\n'),
}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, code in PROBES.items():
        record = {"type": "message", "message": {"role": "assistant", "content": [
            {"type": "toolCall", "name": "eval", "id": name + "-0",
             "arguments": {"language": "py", "reset": False, "code": code}}]}}
        (out / (name + ".jsonl")).write_text(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
