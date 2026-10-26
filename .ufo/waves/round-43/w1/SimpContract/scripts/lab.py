"""In-process harness for the reference tool (no sandbox, no host mutation)."""
import contextlib, importlib.util, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = LANE + "/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt"
CNT = LANE + "/quality/counters/c1-r42-geometry.py"

def load(name, path):
    from importlib.machinery import SourceFileLoader
    loader = SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(name, loader)
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m

ref = load("ref_tool", REF)

def cli(argv, stdin=b""):
    """Return (rc, stdout_bytes) exactly as `python3 mado-geometry.py <argv>` would."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = ref.run(list(argv), io.BytesIO(stdin))
    except ref.Setup as exc:
        return 2, ("MADO_GEOMETRY: SETUP %s\n" % exc).encode()
    return rc, buf.getvalue().encode()

def rep(clients, texts):
    """Pure report path: clients bytes/list + list of rule texts."""
    raw = clients if isinstance(clients, bytes) else json.dumps(clients).encode()
    if isinstance(texts, str):
        texts = [texts]
    try:
        lines, rc = ref.report(raw, texts)
    except ref.Setup as exc:
        return 2, ("MADO_GEOMETRY: SETUP %s\n" % exc).encode()
    return rc, ("\n".join(lines) + "\n").encode()

def summary(rc, out):
    last = out.decode("utf-8", "replace").splitlines()[-1] if out else ""
    return {"rc": rc, "last": last, "sha": __import__("hashlib").sha256(out).hexdigest()[:12],
            "lines": out.decode("utf-8", "replace").splitlines()}

def mk(dirpath, name, data):
    os.makedirs(dirpath, exist_ok=True)
    p = os.path.join(dirpath, name)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode())
    return p
