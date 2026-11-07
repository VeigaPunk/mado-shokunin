import importlib.util, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mado_mimeglob", os.path.join(here, "mado-mimeglob.py"))
mg = importlib.util.module_from_spec(spec); spec.loader.exec_module(mg)
gio = mg.ctypes.CDLL("libgio-2.0.so.0")
gio.g_content_type_guess.restype = mg.ctypes.c_char_p
gio.g_content_type_guess.argtypes = [mg.ctypes.c_char_p, mg.ctypes.c_void_p, mg.ctypes.c_size_t,
                                      mg.ctypes.POINTER(mg.ctypes.c_int)]
name = None
for i, a in enumerate(sys.argv):
    if a == "--name": name = sys.argv[i + 1]
files = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (name or "",)]
with open(files[-1], "rb") as fh: data = fh.read()
u = mg.ctypes.c_int(0)
t = gio.g_content_type_guess(os.fsencode(name) if name else None, data, len(data), mg.ctypes.byref(u))
print(json.dumps({"mode": "cache", "dirs": [], "results": [{"file": files[-1], "name": name,
      "type": t.decode(), "uncertain": 1 if u.value else 0, "sniffed": t.decode(), "prio": 0, "types": []}]}))
