Round 47 (2026-10-26), w1 source-log note for the integrator (draft; L1 owns the merge into `corpus/SOURCES.md` § search log).

Question: what does the xdg-terminal-exec 0.14.3 selection chain read, in what order, and with what
rejections, so a host observation can say which terminal SUPER+RETURN launches and why?
Searched in chain order: the pinned host script and its tag siblings (script, README, man page,
upstream test suite, Makefile, tag `xdg-terminals.list`), then the spec texts it claims to
implement (proposal MR 3 raw file at its head SHA, Desktop Entry Specification, Base Directory
Specification), then the omarchy v3.8.3 sources that produce the two host inputs (Alacritty entry,
list file, list writer, cwd helper), then the host bytes (both Alacritty entries, the installed
omarchy tree and its version file).
Opened 21 locations; included 13 new rows S326-S338. Held back 3 rather than rowed: the tag
`xdg-terminals.list` (sha256 a2b5bf69…, the digest S060 already carries, so no new evidence), the
`Makefile` (build only, names no selection rule) and the repo/API tree listings plus MR metadata
(used as anchors, not as text). Excluded 2: `mime-apps-spec` (named only as the model the config
spec copies) and the `test/config/*` fixture lists (their expectations are already carried by the
test-suite row S329). S326 and S327 reopen the S057 and S056 URLs under distinct scopes: census
reports W04 for both, warning only, no E04. Stop: every layer of the chain (resolver code, shipped
docs, normative spec, deployment source, host bytes) has one primary source; the runtime print-mode
observation belongs to the C2 entry's receipt, not to a row.
