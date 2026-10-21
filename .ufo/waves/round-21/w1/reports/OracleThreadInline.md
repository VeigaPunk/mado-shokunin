# ThreadInline oracle proposal

- **Axes:** C1 operability (callback recall and command binding) is the scope of this proposal; C2 calibration (independent registration-integrity assessment) is not assessed here.
- Added `.ufo/waves/round-21/w1/oracles/ThreadInline.json` with the minimal Python transcript and expected `package_query` / `pacman -Q r21` / `observed` finding.
- Semantics: `Thread.start()` starts the thread; its default `run()` invokes the supplied target. The inline lambda therefore reaches `subprocess.run` with the exact literal argv. This is an explicit callback path and exact binding, not a conservatively unresolved callback or recursive path, so `observed` is the expected evidence rather than `lead`. `pacman -Q` is a package-database query.
- Safety and limits: transcript is data only and was not executed. No scanner/tool was opened or run; no measurements or installations were performed. This records an independent C1 expectation, not detector verification or a C2 claim.

Sources: [Python `Thread.start`](https://docs.python.org/3.14/library/threading.html#threading.Thread.start), [Python `Thread.run`](https://docs.python.org/3.14/library/threading.html#threading.Thread.run), [Python `subprocess.run`](https://docs.python.org/3.14/library/subprocess.html#subprocess.run), [Arch pacman manual](https://man.archlinux.org/man/pacman.8.en.txt).
