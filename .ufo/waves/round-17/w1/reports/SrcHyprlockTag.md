# SrcHyprlockTag — hyprlock latest tag, README, example config, PAM config

Seat: `MadoR17.SrcHyprlockTag` (leaf scout). Round 17 / hyaku phase 2.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `27cd06f`,
pre-registration `0175f13`. Access date for every network read: **2026-10-20**.
Question answered: P6 (screen/idle) documentary route material for hyprlock —
tag identity, the three requested files, and the auth/grace/ext-session-lock
facts they actually support.

## 1. Tag resolution — observed

| Fact | Value | Evidence |
|---|---|---|
| Latest release tag | `v0.9.6` | releases atom (below) |
| Release URL | `https://github.com/hyprwm/hyprlock/releases/tag/v0.9.6` | atom `<id>` = `tag:github.com,2008:Repository/759446562/v0.9.6` |
| Tag object | lightweight; `refs/tags/v0.9.6` = `b222d9b1f87e980cac379371df57913a53b99d7f` with no `^{}` peel line | `git ls-remote https://github.com/hyprwm/hyprlock.git 'refs/tags/v0.9.6*'` |
| Release timestamp | `2026-07-18T15:55:27Z` feed, entry `<updated>` 2026-07-18T15:55:50Z | atom |

Method note: `GET /repos/hyprwm/hyprlock/releases/latest` returned **HTTP 403**
`API rate limit exceeded` (unauthenticated), so the tag was resolved two
independent ways instead: the full tag namespace and the releases atom feed.
Both agree on `v0.9.6`. The full list (printed explicitly, because `git ls-remote`
sorts refnames lexicographically and a hypothetical `v0.10.x` would sort *before*
`v0.2.0*) contains 20 tags, `v0.1.0` … `v0.9.6`, and **no** `v0.10.x`:

```text
94ac7fe v0.1.0  0fe1028 v0.2.0  bc87adf v0.3.0  6e09211 v0.4.0
dba9d8b v0.4.1  a093a9e v0.5.0  381a284 v0.6.0  3d63d9b v0.6.1
9cb5cd9 v0.6.2  e588351 v0.7.0  8f73c39 v0.8.0  b3f1aa7 v0.8.1
6c64630 v0.8.2  31297a8 v0.9.0  bdf0ef8 v0.9.1  c48279d v0.9.2
d7079a1 v0.9.3  824c8b4 v0.9.4  d75e93f v0.9.5  b222d9b v0.9.6
```

Atom receipt: `https://github.com/hyprwm/hyprlock/releases.atom`,
sha256 `119b582ca3cc0e84924bc4c7921d9095680d38e1224288574f2bde1c7128608b`.

Tag tarball cross-check: `https://codeload.github.com/hyprwm/hyprlock/tar.gz/refs/tags/v0.9.6`
sha256 `7f653b87765bcfff7c1f8e04af326a7e73bbcacd1fb7d4436f6a16624a2247bb`,
contains `hyprlock-0.9.6/VERSION` = `0.9.6`.

## 2. File receipts

Every file was fetched twice: once from `raw.githubusercontent.com` at
`v0.9.6`, once from the tag tarball. Digests are identical across both sources
for all three requested files — the raw endpoint serves exactly the tag bytes.

| Path at `v0.9.6` | raw URL | sha256 | lines / bytes |
|---|---|---|---|
| `README.md` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md` | `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3` | 60 / 1458 |
| `assets/example.conf` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/assets/example.conf` | `22e74ea5e271fee900b8fd06b5900465adf779fc8ca50d70be14760622faa71e` | 109 / 2550 |
| `pam/hyprlock` | `https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/pam/hyprlock` | `f4f8c269ef8a2ad86d1ab42bb4ca7b719663e632b12ce21ac9aee19bf6e1272d` | 5 / 126 |

## 3. Quotes (verbatim, ≤25 words, line anchors in the fetched bytes)

`README.md`:
- l.2 — "Hyprland's simple, yet multi-threaded and GPU-accelerated screen locking utility." (9 words)
- l.5 — "Uses the ext-session-lock protocol" (5 words)
- l.39 — "pam" (dependency list entry)
- README l.21–26 documents a distro package channel and a source-build channel
  in prose; **nothing in that block was executed** (see §7) and it is not
  evidence of anything installed on this host.

`assets/example.conf`:
- l.1 — "# sample hyprlock.conf" (4 words)
- l.9 — "# you can get started by copying this config to ~/.config/hypr/hyprlock.conf" (13 words)
- l.19–21 — commented-out fingerprint block headers, "# auth {", "#     fingerprint {", "#         enabled = true"
- l.58 — "fail_text = $PAMFAIL$FPRINTFAIL"

`pam/hyprlock` (whole file is 4 content lines + trailing blank):
- l.1 — "# PAM configuration file for hyprlock" (6 words)
- l.2 — "# the 'login' configuration file (see /etc/pam.d/login)"
- l.4 — "auth        include     login"

## 4. Auth (PAM module name) — what the bytes actually say

Chain, all documentary, tag-pinned:

1. `pam/hyprlock:4` is `auth        include     login`. The **only** module
   token in the repo file is the *included service name* `login`; there is no
   `pam_unix.so` / `pam_faillock.so` / any `.so` literal in this file. So the
   repo's PAM policy is "delegate the auth stack to the distro `login`
   service", not "authenticate with module X directly".
2. `CMakeLists.txt:164–165` installs that file to
   `${CMAKE_INSTALL_FULL_SYSCONFDIR}/pam.d` — i.e. `/etc/pam.d/hyprlock`.
3. The **service name** the binary asks PAM for is a config string, not a
   compile-time constant: `src/config/ConfigManager.cpp:252`
   `m_config.addConfigValue("auth:pam:module", Hyprlang::STRING{"hyprlock"});`
   with `auth:pam:enabled` default `1` at l.251.
4. `src/auth/Pam.cpp:67–72`: reads `auth:pam:module`, then if
   `/etc/pam.d/<module>` is absent logs an error and **falls back to `su`**;
   l.118 `pam_start(m_sPamModule.c_str(), …)`.
5. `src/auth/Fingerprint.cpp` exists as an optional second auth path; the
   example config gates it behind a commented `auth { fingerprint { … } }`
   block (l.19–26).

Confidence: **high** that the PAM *service name* is `hyprlock` and that the
shipped stack is `auth include login`. Not claimed: which concrete PAM modules
the host's `/etc/pam.d/login` expands to, or whether `/etc/pam.d/hyprlock`
exists on this host — both are host state and were deliberately not read
(§7); host state is `[UNK]`.

`src/auth/Pam.cpp` sha256 `c74c78943c5bf9dc68f375060f6535cf8ca4bc1a2d0d31f78fe5541d89d02053`
(190 lines); `src/config/ConfigManager.cpp` sha256
`ca0f581f933b08d0a2b10a0197432ac732233fa6d832120dbe989dd804bf97a0` (678 lines);
`CMakeLists.txt` sha256 `96d8c54a4f1669cf1052f6d0dab8e6169762c2ad46a6d5b4c148bd5c65a0d54e` (170 lines).

## 5. Grace — what the bytes actually say

Grace is a **command-line** option, not a config key:

- `src/main.cpp:29` — `registerIntOption("grace", "g", "Seconds before authentication is required")`
  Quote: "Seconds before authentication is required" (6 words).
- `src/main.cpp:59` — `int graceSeconds = argParser.getInt("grace").value_or(0);`
  → default **0** when not passed.
- `src/main.cpp:61–62` — deprecated `--immediate` forces `graceSeconds = 0` and
  logs `"--immediate" is deprecated. Use the "--grace" option instead.`
  (14 words of the logged message).
- `src/core/hyprlock.cpp:67–68` — when `graceSeconds > 0`, sets
  `m_tGraceEnds = now + seconds(graceSeconds)`; `src/core/Seat.cpp:44` logs
  "In grace and cursor moved more than 5px, unlocking!".

Negative result worth recording: **`grace` appears 0 times** in
`assets/example.conf` (`grep -c grace` → `0`) and 0 times in `README.md`.
So an entry claiming grace is configured in `hyprlock.conf` would be wrong for
v0.9.6; the documented surface for it is the CLI/`--help`, and the deferred-lock
timer it arms.

`src/main.cpp` sha256 `606793cfcec83d7b9b5db03b92db728c6770cd782e75ff19f115949ac0176ae9` (99 lines);
`src/core/hyprlock.cpp` sha256 `68b5491c4ea9105e51b31d1694c18c62efd4addaef24b261ff32556f56ce3663` (939 lines).

## 6. Lock screen via ext-session-lock — corroborated three ways

- Claim (`README.md:5`): "Uses the ext-session-lock protocol".
- Build wiring: `CMakeLists.txt:154`
  `protocolnew("staging/ext-session-lock" "ext-session-lock-v1" false)`.
- Hard runtime requirement, not merely a capability: `src/core/hyprlock.cpp:347–350`
  binds `ext_session_lock_manager_v1`; if binding fails it logs
  "Couldn't bind to ext-session-lock-v1, does your compositor support it?" (10 words)
  and `exit(1)`. `src/core/LockSurface.cpp:51` asserts creation of
  `ext_session_lock_surface_v1`.

So "lock screen" here means a Wayland **session lock** (compositor must expose
`ext-session-lock-v1`), not an in-compositor overlay. A round-17 note may say
this; it may not say any host compositor actually supports or runs it.

## 7. Scope / hygiene receipt

- No `sudo`, `pacman`/`yay`/`paru` (not even `-Q`/`-Si`), `systemctl`,
  `hyprctl`, `waybar`, `walker`, `hypridle`, `hyprlock`, `alacritty`,
  `notify-send`, screenshots, `libinput`/`evtest`, or any live probe was run.
  The host pause was honoured in full; README's install prose was read as data
  only.
- No `~/.omp` transcript, `agent.db*`, credential/auth file, or host
  `~/.config`/omarchy tree was opened. Only network fetches into `/tmp/hl096`
  and this report were produced.
- No `jj` command of any kind; no git mutation; no commit; no fleet/sibling
  file touched. Nothing was installed or upgraded, so the tooling-directive
  record is empty.
- Host hyprlock version is **[UNK]**: deriving it would require a package
  query, which the pause forbids. A tag's source says nothing about the
  installed binary.

## 8. Remaining unknowns (explicit)

- `[UNK]` host hyprlock version, and whether hyprlock is installed at all.
- `[UNK]` `/etc/pam.d/hyprlock` presence and content on this host (not read).
- `[UNK]` what the `login` service expands to on this distro (pam modules).
- Not checked: hypridle-side idle→lock wiring (sibling seat `SrcHypridleSrc`),
  and hyprlock's `--grace` behaviour at runtime (never exercised).

## 9. Reproduction

```sh
git ls-remote https://github.com/hyprwm/hyprlock.git 'refs/tags/v0.9.6*'
curl -sS https://github.com/hyprwm/hyprlock/releases.atom -o releases.atom
sha256sum releases.atom
# expect 119b582c…7128608b; latest <title> v0.9.6
curl -sSL -o src.tar.gz https://codeload.github.com/hyprwm/hyprlock/tar.gz/refs/tags/v0.9.6
sha256sum src.tar.gz   # expect 7f653b87…4a2247bb
tar xzf src.tar.gz && cd hyprlock-0.9.6
sha256sum README.md assets/example.conf pam/hyprlock
# expect 83096def…38f50f3 / 22e74ea5…2faa71e / f4f8c269…6e1272d
sed -n '5p' README.md; sed -n '4p' pam/hyprlock; sed -n '29p' src/main.cpp
```
