# OracleJjForget

Axes: **C1 operability** (the proposal contributes an independently reasoned VCS-write oracle); **C2 calibration** (not exercised by this case).

The oracle at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/JjForget.json` uses the requested inert shell shape `jj --ignore-working-copy bookmark forget probe` and expects one `vcs_write` finding for that exact command. The committed round-20 `ReviewVcsV3` evidence records a successful forget with `--ignore-working-copy`, after which the preexisting local `probe` bookmark was absent from `jj bookmark list` (`ReviewVcsV3.md:14-20`). Its evidence table also explicitly records the form as a local-bookmark write (`ReviewVcsV3.md:53`). Thus `--ignore-working-copy` cannot justify classifying this operation as clean: the observed repository bookmark-state mutation is a write, even without relying on a working-copy update. This boundary includes repository state beyond ref-only effects; no additional object/index/config/workspace effect is claimed for this particular case.

Verification: source-based oracle reasoning only. I did not execute the VCS command, fixture/transcript code, classifier, gate, build, tests, or installers. Tool installations: none.
