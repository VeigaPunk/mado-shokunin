# JjRemote oracle

The oracle expects a `write` finding for `jj --ignore-working-copy git remote add origin local.git`. The committed round-20 `ReviewVcsV3` report records a successful `jj git remote add origin ...` under `--ignore-working-copy` and an observed change to the repository Git remote configuration (lines 14–20, 52). That configuration mutation is a repository write; suppressing working-copy snapshotting does not make the operation clean. This matches the registered boundary, which counts repository configuration writes.

The measured round-20 command used an explicit repository selector and a different local remote path; this oracle uses the supplied command shape. No VCS command, fixture/transcript, classifier, or measurement tool was executed/accessed. No tool was installed.

Report: .ufo/waves/round-21/w1/reports/OracleJjRemote.md
