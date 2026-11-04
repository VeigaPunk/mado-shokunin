import importlib.util, os, subprocess, json
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r70/R70MutBattery"
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
pris = load(LANE + "/quality/counters/c1-r70-landing-controls.py", "pris")
me = load(S + "/mut/c1h-e/c1-r70-landing-controls.py", "me")
mf = load(S + "/mut/c1h-f/c1-r70-landing-controls.py", "mf")
out = {}
line = "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed (interrupted)"
out["c1h-e"] = {"probe": "summary_shows_failure(%r)" % line,
                "pristine": pris.summary_shows_failure(line),
                "mutant": me.summary_shows_failure(line)}
def probe_sha(mod):
    def fake_run(argv, env, cwd=None, input_bytes=None, timeout=900):
        a = [str(x) for x in argv]
        if "--verify" in a:
            return subprocess.CompletedProcess(a, 0, b"zz" + b"a" * 40 + b"zz\n", b"")
        if "--show-toplevel" in a:
            return subprocess.CompletedProcess(a, 0, os.fsencode(cwd or "."), b"")
        return subprocess.CompletedProcess(a, 1, b"", b"")
    mod.run = fake_run
    try:
        return {"returns": mod.resolve_rev(".", "HEAD", "/scratch/home")}
    except Exception as exc:
        return {"raises": type(exc).__name__, "msg": str(exc)[:90]}
out["c1h-f"] = {"probe": 'resolve_rev with rev-parse emitting "zz"+40*"a"+"zz"',
                "pristine": probe_sha(pris), "mutant": probe_sha(mf)}
out["c1h-g"] = {"probe": "same predicate at the fixture-rev call site (build_r_fixture, line 389)",
                "note": "identical guard expression; same flip input as c1h-f"}
print(json.dumps(out, indent=1))
open(S + "/probes.json", "w").write(json.dumps(out, indent=1) + "\n")
