import json, sys

H = 'import subprocess\n'
RUN = 'def run():\n    subprocess.run(["pacman", "-S", "%s"])\n'

C = {}
C["AugAssignGlobalList"] = H + 'hooks = []\n' + RUN % "r23x-augassign" + \
    'def register(callback):\n    global hooks\n    hooks += [callback]\nregister(run)\nhooks[0]()\n'
C["AugAssignAttrList"] = H + 'class Box:\n    pass\nbox = Box()\nbox.cbs = []\n' + RUN % "r23x-augattr" + \
    'def register(callback):\n    box.cbs += [callback]\nregister(run)\nbox.cbs[0]()\n'
C["AnnAssignAttr"] = H + 'class Box:\n    pass\nbox = Box()\n' + RUN % "r23x-annattr" + \
    'def register(callback):\n    box.cb: object = callback\nregister(run)\nbox.cb()\n'
C["AnnAssignSubscript"] = H + 'hooks = {}\n' + RUN % "r23x-annsub" + \
    'def register(callback):\n    hooks["k"]: object = callback\nregister(run)\nhooks["k"]()\n'
C["GlobalNameStore"] = H + 'saved = None\n' + RUN % "r23x-globalstore" + \
    'def register(callback):\n    global saved\n    saved = callback\nregister(run)\nsaved()\n'
C["ClosureStoredInDict"] = H + 'hooks = {}\n' + RUN % "r23x-closure-dict" + \
    'def register(callback):\n    def inner():\n        callback()\n    hooks["k"] = inner\nregister(run)\nhooks["k"]()\n'
C["DefaultArgClosureAppended"] = H + 'hooks = []\n' + RUN % "r23x-default-closure" + \
    'def register(callback):\n    def inner(cb=callback):\n        cb()\n    hooks.append(inner)\nregister(run)\nhooks[0]()\n'
C["ConditionalTrue"] = H + RUN % "r23x-cond-true" + \
    'def consume(callback, flag):\n    if flag:\n        callback()\nconsume(run, True)\n'
C["ConditionalCompare"] = H + RUN % "r23x-cond-cmp" + \
    'def consume(callback, n):\n    if n > 1:\n        callback()\nconsume(run, 2)\n'
C["ConditionalFalseSkips"] = H + RUN % "r23x-cond-false" + \
    'def consume(callback, flag):\n    if flag:\n        callback()\nconsume(run, False)\n'
C["TryExceptCall"] = H + RUN % "r23x-try" + \
    'def consume(callback):\n    try:\n        callback()\n    except Exception:\n        pass\nconsume(run)\n'
C["TryFinallyCall"] = H + RUN % "r23x-finally" + \
    'def consume(callback):\n    try:\n        pass\n    finally:\n        callback()\nconsume(run)\n'
C["TryExceptHandlerCall"] = H + RUN % "r23x-handler" + \
    'def consume(callback):\n    try:\n        raise ValueError("x")\n    except ValueError:\n        callback()\nconsume(run)\n'
C["DunderCallInvoke"] = H + RUN % "r23x-dunder-call" + \
    'def consume(callback):\n    callback.__call__()\nconsume(run)\n'
C["ForLoopOverTuple"] = H + RUN % "r23x-for-tuple" + \
    'def consume(callback):\n    for f in (callback,):\n        f()\nconsume(run)\n'
C["SubscriptListInvoke"] = H + RUN % "r23x-list-index" + \
    'def consume(callback):\n    [callback][0]()\nconsume(run)\n'
C["BoolOpInvoke"] = H + RUN % "r23x-boolop" + \
    'def consume(callback):\n    (callback or None)()\nconsume(run)\n'
C["YieldedCallback"] = H + RUN % "r23x-yield" + \
    'def gen(callback):\n    yield callback\nfor f in gen(run):\n    f()\n'
C["WhileLoopCall"] = H + RUN % "r23x-while" + \
    'def consume(callback):\n    n = 0\n    while n < 1:\n        callback()\n        n += 1\nconsume(run)\n'
C["LambdaImmediate"] = H + RUN % "r23x-lambda-now" + \
    'def consume(callback):\n    (lambda: callback())()\nconsume(run)\n'
C["NestedDefCalled"] = H + RUN % "r23x-nested" + \
    'def consume(callback):\n    def inner():\n        callback()\n    inner()\nconsume(run)\n'
C["StarArgsCall"] = H + RUN % "r23x-star" + \
    'def consume(callback):\n    callback(*())\nconsume(run)\n'
C["KeywordCallback"] = H + RUN % "r23x-kw" + \
    'def consume(callback, flag=False):\n    if flag:\n        callback()\nconsume(callback=run, flag=True)\n'
C["NonlocalStoreReturned"] = H + RUN % "r23x-nonlocal" + \
    'def make(callback):\n    saved = None\n    def setter():\n        nonlocal saved\n        saved = callback\n    setter()\n    def get():\n        return saved\n    return get\nmake(run)()()\n'
C["WalrusThenReturnHolder"] = H + 'hooks = {}\n' + RUN % "r23x-walrus" + \
    'def register(callback):\n    if (f := callback):\n        hooks["k"] = [f][0]\nregister(run)\nhooks["k"]()\n'
C["CallLaterViaStoredLocal"] = H + RUN % "r23x-later-local" + \
    'def consume(callback):\n    later = callback\n    for _ in range(1):\n        later()\nconsume(run)\n'
C["MatchCase"] = H + RUN % "r23x-match" + \
    'def consume(callback, mode):\n    match mode:\n        case "go":\n            callback()\nconsume(run, "go")\n'

json.dump(C, open(sys.argv[1], "w"), indent=1)
