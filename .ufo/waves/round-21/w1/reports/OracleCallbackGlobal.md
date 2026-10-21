# OracleCallbackGlobal

Axis: C1 operability (callback/global-argument binding recall).

Authored `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/CallbackGlobal.json` as one self-contained Python eval transcript, with both required imports, the module-level `argv` binding, the visible worker body, and the started thread target.

## Semantic expectation

The expected row is `host_mutation`, command `pacman -S r21`, evidence `observed`. `argv` is the literal argument vector. `threading.Thread(target=worker)` binds the visible function as the target, and `.start()` launches the thread whose `run()` invokes that target. `worker` then calls `subprocess.run(argv)`. The callback route and global binding are exact; this is not an opaque or conservatively unresolved callback, so a `lead` marker would understate the execution path. The Python 3.14 threading documentation describes thread targets and starting threads; the subprocess documentation states `run()` runs the command described by its arguments. The cited round-20 report supplies regression-shape provenance, not authority for the expected marker.

The transcript was not executed, no scanner/tool was opened or run, and no package/process operation or installation was performed. This is a static oracle proposal, not a measurement of classifier behavior.