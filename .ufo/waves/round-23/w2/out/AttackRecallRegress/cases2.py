import json, sys

H = 'import subprocess\n'
RUN = 'def run():\n    subprocess.run(["pacman", "-S", "%s"])\n'
RUNA = 'def run(arg):\n    subprocess.run(["pacman", "-S", "%s"])\n'

C = {}
C["EarlyReturnThenCall"] = H + RUN % "r23y-early-return" + \
    'def consume(callback, flag):\n    if flag:\n        return\n    callback()\nconsume(run, False)\n'
C["RaiseCaughtThenCall"] = H + RUN % "r23y-raise-caught" + \
    'def consume(callback):\n    try:\n        raise ValueError("x")\n    except ValueError:\n        return callback()\nconsume(run)\n'
C["TryElseCall"] = H + RUN % "r23y-try-else" + \
    'def consume(callback):\n    try:\n        pass\n    except Exception:\n        pass\n    else:\n        callback()\nconsume(run)\n'
C["TryUnboundableThenHandler"] = H + RUN % "r23y-try-int" + \
    'def consume(callback):\n    try:\n        int("a")\n    except ValueError:\n        callback()\nconsume(run)\n'
C["WhileTrueBreak"] = H + RUN % "r23y-while-break" + \
    'def consume(callback):\n    while True:\n        callback()\n        break\nconsume(run)\n'
C["ConditionalOnCallableTest"] = H + RUN % "r23y-callable-test" + \
    'def consume(callback):\n    if callable(callback):\n        callback()\nconsume(run)\n'
C["ConditionalIsNotNone"] = H + RUN % "r23y-not-none" + \
    'def consume(callback=None):\n    if callback is not None:\n        callback()\nconsume(run)\n'
C["ConditionalTryDunder"] = H + RUN % "r23y-try-dunder" + \
    'def consume(callback):\n    try:\n        callback.__call__()\n    except TypeError:\n        pass\nconsume(run)\n'
C["DictDispatchInvoke"] = H + RUN % "r23y-dict-dispatch" + \
    'def consume(callback):\n    {"a": callback}["a"]()\nconsume(run)\n'
C["ComprehensionInvoke"] = H + RUN % "r23y-comprehension" + \
    'def consume(callback):\n    [callback() for _ in "x"]\nconsume(run)\n'
C["DecoratorInvoke"] = H + RUNA % "r23y-decorator" + \
    'def consume(callback):\n    @callback\n    def f():\n        pass\nconsume(run)\n'
C["ClassBodyInvoke"] = H + RUN % "r23y-class-body" + \
    'def consume(callback):\n    class K:\n        callback()\nconsume(run)\n'
C["SecondCallUnfollowedArg"] = H + RUNA % "r23y-unbound-arg" + \
    'def consume(callback, items):\n    for item in items:\n        callback(item)\nconsume(run, ["a"])\n'
C["SecondCallDunderAfterCall"] = H + RUN % "r23y-second-dunder" + \
    'def first():\n    pass\ndef consume(a, b):\n    a()\n    b.__call__()\nconsume(first, run)\n'
C["StoredSecondConsumerCalled"] = H + 'hooks = {}\n' + RUN % "r23y-two-consumers" + \
    'def register(callback):\n    hooks.update(k=callback)\ndef fire(callback):\n    callback()\nfire(lambda: None)\nregister(run)\nhooks["k"]()\n'
C["AugAssignConditional"] = H + 'class Box:\n    pass\nbox = Box()\nbox.cbs = []\n' + RUN % "r23y-aug-cond" + \
    'def register(callback, flag):\n    if flag:\n        box.cbs += [callback]\nregister(run, True)\nfor f in box.cbs:\n    f()\n'
C["AnnAssignInTry"] = H + 'class Box:\n    pass\nbox = Box()\n' + RUN % "r23y-ann-try" + \
    'def register(callback):\n    try:\n        box.cb: object = callback\n    except Exception:\n        pass\nregister(run)\nbox.cb()\n'
C["GlobalStoreViaSecondHelper"] = H + 'saved = None\n' + RUN % "r23y-global-second" + \
    'def keep(callback):\n    global saved\n    saved = callback\ndef register(callback):\n    keep(callback)\nregister(run)\nsaved()\n'

json.dump(C, open(sys.argv[1], "w"), indent=1)
