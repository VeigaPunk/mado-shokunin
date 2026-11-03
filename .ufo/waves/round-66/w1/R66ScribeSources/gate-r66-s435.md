## Gate draft — S435 (round 66 lesson `## Gate` section)

S435 — GNU Bash 5.3 release manual §3.7.5 Exit Status (opened 2026-11-03, this round)
- URL: https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz (HTML rendering of the same section:
  https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html)
- Access date: 2026-11-03
- Located quote (15 words): "So while an exit status of zero indicates success, a non-zero
  exit status indicates failure." — `doc/bashref.texi:3905-3906` (§3.7.5), and the same text
  at `Exit-Status.html:68-69`.
- Supporting located quote (19 words): "If a command is not found, the child process created
  to execute it returns a status of 127." — `doc/bashref.texi:3914-3915`, `Exit-Status.html:77-78`.
- Version/section anchor: §3.7.5 (`@node Exit Status`, texi:3890) of the **Bash 5.3 release**.
  Digests: tarball 11,355,854 B sha256
  `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`; `doc/bashref.texi`
  415,804 B sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`; HTML node
  5,187 B sha256 `b5489d3d21e32da01de356e7a63093ec276a60a020d616a05fffcc9b7b19d983`; single-page
  manual 1,040,954 B sha256 `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`
  carries "version 5.3, 18 May 2025".
- Cross-check: both digests equal the values S110 already records for its own tag-anchored
  read, so the release bytes are independently reproduced; S110's scope (`set -e` exception
  set) is untouched.
- Host binding: `bash --version` → `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)`.
- Upstream state: immutable release artifact; the HTML node is live and digest-pinned only.
- Teaches (scoped): rc is the value the child returns through `waitpid`; zero is a *shell
  convention* for success and non-zero the failure signal; 126 = found-not-executable,
  127 = not found, 128+N = fatal signal, builtin misuse = 2. A forced rc=0 therefore cannot
  be told apart from genuine success by its status, and no status shows what work ran.
- Limits stated with the row: this source proves neither the register's row truth (C1) nor
  that any child was invoked or that any marker was emitted (C2). It fixes vocabulary only.
- Registry effect: one new tier-A row, `status: mined`, `opened: 2026-11-03`,
  `recheck: on-release`, `used-by: corpus/lessons/round-66.md`. No existing row edited.
