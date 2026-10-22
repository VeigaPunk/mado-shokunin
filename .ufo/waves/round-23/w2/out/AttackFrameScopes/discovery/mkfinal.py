import hashlib, json, sys
from pathlib import Path
H = "import subprocess\n"
CASES = [
 ("FrameReusedBySecondInvocation",
  H + "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
      'f = outer(["pacman", "-Q", "w2-afs-first-frame"])\nouter(["pacman", "-S", "w2-afs-second-frame"])\nf()\n',
  ["pacman -S w2-afs-second-frame"],
  "frame_scope keys a frame on id(def node); the second invocation of outer overwrites the view that the first closure's sibling leaf reads argv through."),
 ("FrameReusedBothClosuresCalled",
  H + "def outer(argv):\n    def leaf():\n        subprocess.run(argv)\n    def inner():\n        leaf()\n    return inner\n"
      'f = outer(["pacman", "-Q", "w2-afs-both-first"])\ng = outer(["pacman", "-Q", "w2-afs-both-second"])\nf()\ng()\n',
  [],
  "Same conflation as a silent miss: two live frames of outer, both closures run, the first frame's command disappears."),
 ("NestedBinderFreezesLateGlobal",
  H + 'argv = ["pacman", "-S", "w2-afs-early-global"]\n'
      "def outer():\n    def other():\n        argv = [\"pacman\", \"-S\", \"w2-afs-other-local\"]\n    def inner():\n        subprocess.run(argv)\n    return inner\n"
      'f = outer()\nargv = ["pacman", "-Q", "w2-afs-late-global"]\nf()\n',
  ["pacman -S w2-afs-early-global", "pacman -S w2-afs-other-local"],
  "own_names walks into nested def bodies, so a name bound only in sibling other() counts as owned by outer's frame and freezes the early module value (breaks S121 late binding)."),
 ("MatchCaptureBinderNotOwned",
  H + 'argv = ["pacman", "-S", "w2-afs-module-global"]\n'
      "def outer():\n    match [\"pacman\", \"-Q\", \"w2-afs-match-capture\"]:\n        case argv:\n            pass\n    def inner():\n        subprocess.run(argv)\n    inner()\n"
      "outer()\n",
  ["pacman -S w2-afs-module-global"],
  "own_names omits match-capture (and with-as) binders, so the frame view lacks argv and the scope chain falls through to the module global: base was an honest unparsed, tip is a false observed row."),
]
out = Path(sys.argv[1]); (out / "fixtures").mkdir(parents=True, exist_ok=True)
rows = []
for cid, code, forbid, why in CASES:
    rec = {"type": "message", "message": {"role": "assistant", "content": [{"type": "toolCall", "name": "eval", "id": cid + "-0", "arguments": {"language": "py", "reset": False, "code": code}}]}}
    p = out / "fixtures" / (cid + ".jsonl")
    p.write_text(json.dumps(rec) + "\n")
    rows.append(dict(id=cid, kind="exact", forbid_any=forbid, why=why, fixture="fixtures/" + cid + ".jsonl",
                     sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(out / "cases-draft.json").write_text(json.dumps(dict(schema="mado-r23-w2-attackframescopes-cases-v1", note="want filled from truth receipt", cases=rows), indent=1) + "\n")
