# Gate lines — rows S326..S338 (round 47 w1, C2 seat ScrRows)

One line per row: id, URL fetched today (2026-10-26), the receipt locator, and one quote
taken at that locator. Every quote is <= 25 words and is checked by `verify-quotes.sh`,
which greps the receipt file and requires a hit on the stated line.

Fields are tab-separated inside the block below (`id`, `url`, `accessed`, `receipt:line`, `quote`).

```
S326	https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec	2026-10-26	fetch/xdg-terminal-exec:1057	# for explicitly listed entries do not apply DE *ShowIn limits
S327	https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md	2026-10-26	fetch/README.md:320	### Exec command parsing, escape sequences.
S328	https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec.1.scd	2026-10-26	fetch/xdg-terminal-exec.1.scd:90	The first listed, found, and valid Desktop Entry is used.
S329	https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/test/tests.bats	2026-10-26	fetch/tests.bats:127	@test "ignores hidden entry" {
S330	https://gitlab.freedesktop.org/terminal-wg/specifications/-/merge_requests/3	2026-10-26	fetch/spec-xte-proposal.md:163	- the first applicable entry is used
S331	https://gitlab.freedesktop.org/xdg/xdg-specs/-/blob/a0eaad5cc900684519030ceb568f7053dc315fe6/desktop-entry/desktop-entry-spec.xml	2026-10-26	fetch/desktop-entry-spec.xml:570	<varname>Hidden</varname> should have been called <varname>Deleted</varname>.
S332	https://gitlab.freedesktop.org/xdg/xdg-specs/-/blob/a0eaad5cc900684519030ceb568f7053dc315fe6/basedir/basedir-spec.xml	2026-10-26	fetch/basedir-spec.xml:191	<literal>$XDG_CONFIG_DIRS</literal> defines the preference-ordered set of
S333	https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/applications/Alacritty.desktop	2026-10-26	fetch/om/applications_Alacritty.desktop:14	X-TerminalArgExec=-e
S334	https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/config/xdg-terminals.list	2026-10-26	fetch/om/config_xdg-terminals.list:2	The first found and valid terminal will be used
S335	https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/bin/omarchy-default-terminal	2026-10-26	fetch/om/bin_omarchy-default-terminal:30	cat >~/.config/xdg-terminals.list <<EOF
S336	https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/bin/omarchy-cmd-terminal-cwd	2026-10-26	fetch/om/bin_omarchy-cmd-terminal-cwd:6	terminal_pid=$(hyprctl activewindow | awk '/pid:/ {print $2}')
S337	host bytes ~/.local/share/applications/Alacritty.desktop	2026-10-26	fetch/host/Alacritty.desktop.user:17	X-TerminalArgDir=--working-directory=
S338	host bytes ~/.local/share/omarchy/version	2026-10-26	fetch/host/omarchy-version:1	3.8.3
```

## Fetched pins (sha256 of the bytes held in `fetch/`)

| receipt | bytes | sha256 | provenance URL |
|---|---|---|---|
| fetch/xdg-terminal-exec | 44020 | 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac | raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec |
| fetch/README.md | 14762 | c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40 | raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md |
| fetch/xdg-terminal-exec.1.scd | 6071 | 3dba162f5502a3553bad9b2398ace10f7bc2456900c7c9ff62a436935876ec59 | raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec.1.scd |
| fetch/tests.bats | 8181 | ce4b634257dd6c1ebddd96d88f00f1b324f054209be6c80737224b69e986b311 | raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/test/tests.bats |
| fetch/spec-xte-proposal.md | 10498 | c16a717a0232d08402d53d8847c25c3de6ddf443760ec1ecdf6a3ee76ca8375a | gitlab.freedesktop.org/api/v4/projects/terminal-wg%2Fspecifications/repository/files/proposals%2Fxdg-terminal-exec.md/raw?ref=64c429dfaf442d4a7ca9a656baf91a1b2d9c1a4d |
| fetch/desktop-entry-spec.xml | 71116 | a1baadee9676a2e333377907b3eb7fb06df91976db9a013d29d338fa429f8f81 | gitlab.freedesktop.org/api/v4/projects/xdg%2Fxdg-specs/repository/files/desktop-entry%2Fdesktop-entry-spec.xml/raw?ref=a0eaad5cc900684519030ceb568f7053dc315fe6 |
| fetch/basedir-spec.xml | 15498 | c44dba06041dcfa53c676071615c73b7407242841feadc2affd777b76c8029ae | gitlab.freedesktop.org/api/v4/projects/xdg%2Fxdg-specs/repository/files/basedir%2Fbasedir-spec.xml/raw?ref=a0eaad5cc900684519030ceb568f7053dc315fe6 |
| fetch/om/applications_Alacritty.desktop | 452 | 713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683 | raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/applications/Alacritty.desktop |
| fetch/om/config_xdg-terminals.list | 127 | d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b | raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/config/xdg-terminals.list |
| fetch/om/bin_omarchy-default-terminal | 1173 | 42e422255521b970c16c42545e167ca6e094d8030fe6478531b16784d26ead91 | raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/bin/omarchy-default-terminal |
| fetch/om/bin_omarchy-cmd-terminal-cwd | 565 | 1c262a806b8fb8ececcec1f3db31f1b2bb43ab8bcabdbdca43bafd3e5dae7f3c | raw.githubusercontent.com/omacom/omarchy/6aa2aec1c035/bin/omarchy-cmd-terminal-cwd |
| fetch/host/Alacritty.desktop.user | 452 | 713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683 | host file ~/.local/share/applications/Alacritty.desktop |
| fetch/host/Alacritty.desktop.system | 374 | d420b0f418d9039f324bdb423181f874dee36c47ce2ab643435a4c04aac243d8 | host file /usr/share/applications/Alacritty.desktop |
| fetch/host/omarchy-installed-Alacritty.desktop | 452 | 713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683 | host file ~/.local/share/omarchy/applications/Alacritty.desktop |
| fetch/host/omarchy-installed-xdg-terminals.list | 127 | d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b | host file ~/.local/share/omarchy/config/xdg-terminals.list |
| fetch/host/omarchy-version | 6 | 0a5c29521592a324aa0381ac743c15dc552747cd89c5f5c9715e547df40258c6 | host file ~/.local/share/omarchy/version |
