# AttackP6Listeners — P6 `Listeners` + `hyprlock` bullets vs fetched bytes

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60`
Target: `corpus/knowledge/idle-lock-route-r17.md` — `### Listeners (hypridle)`, `### hyprlock (documentary, from wiki and README)`, and the `### hyprlock.conf` host bullets that follow.
Mode: read-only, hermetic. No package/compositor/systemd/PAM execution, no live probes, no installs (`installs: none`).

## Axes

1. **Quote fidelity** — is every quoted string present at the pinned bytes?
2. **Host leakage** — does any bullet assert behaviour of *this* host, contrary to the note's contract?
3. **Host testability** — can a host claim be checked from the note's own declared evidence set?
4. **Anchor reproducibility** — do `[HW]/[LW]/[HC]/[HH]/[HM]/[HR]/[LR]` numbers land where the note says?

## Result in one line

No fabricated quote was found. The `Listeners` section makes **no** host-behaviour claim. The `hyprlock` section contains **exactly one** bullet that states behaviour on this host — the Arch/`pam_faillock` bullet — and the host's PAM bytes contradict **both** of its numbers (10 failures / 120 s, not 3 / 600 s). One medium defect: `grace` is not a `hyprlock.conf` key at v0.9.6 and cannot be "not set: defaults apply".

---

## Findings

### P6-L1 — HIGH — the Arch/faillock bullet states host behaviour, and the host refutes both numbers

Note text (unchanged):

> - Arch: "On Arch Linux, by default, hyprlock integrates with pambase through pam_faillock.so, which forces a 10 minute timeout after 3 failed unlocks." [LW:84]. Remedy per [LW:85] (documentary).

The wiki sentence is quoted verbatim (`lock-wiki.html`, sha256 `f69cff6…`, block line 73/74). But the bullet is the one in-scope place that makes a claim about the machine the note describes, and the host's PAM stack does not have those values. Host chain read as bytes (`cat -n`/`grep`, no `pam_*` executed):

| file:line | content |
|---|---|
| `/etc/pam.d/hyprlock:3` | `auth        include     login` |
| `/etc/pam.d/login:4` | `auth       include      system-local-login` |
| `/etc/pam.d/system-local-login:3` | `auth      include   system-login` |
| `/etc/pam.d/system-login:5` | `auth       include    system-auth` |
| `/etc/pam.d/system-auth:3` | `auth required pam_faillock.so preauth silent deny=10 unlock_time=120` |
| `/etc/pam.d/system-auth:8` | `auth [default=die] pam_faillock.so authfail deny=10 unlock_time=120` |
| `/etc/pam.d/system-auth:11` | `auth required pam_faillock.so authsucc` |
| `/etc/security/faillock.conf:32` | `deny = 10` |
| `/etc/security/faillock.conf:45` | `# unlock_time = 600` |

This is the stack hyprlock actually uses: v0.9.6 `src/auth/Pam.cpp:67-72` selects `auth:pam:module` (default `hyprlock`), falls back to `su` only when `/etc/pam.d/<module>` is absent — it is present here — and `Pam.cpp:118` calls `pam_start(m_sPamModule…)`.

Effective on this host: **deny = 10 consecutive failures, unlock_time = 120 s (2 min)**. The bullet says **3 failures, 600 s (10 min)**. Both numbers are wrong for this host. The note's global contract ("no behaviour on the running host is claimed") and the single hedge in `§ Unexercised` ("the PAM faillock lockout in [LW:84] is documentary") do not reach the bullet text: the bullet carries no per-claim doc marker, its subject is the exact distro the note's host runs, and the host declaration table contains no PAM file — so nothing in the note itself can adjudicate the claim.

Second-order: the [LW:85] remedy ("update `/etc/security/faillock.conf`") cannot change these values here. `system-auth:3,8` pass `deny`/`unlock_time` on the module command line, and `pam_faillock(8)` states: *"The options specified on the module command line override the values from the configuration file."* (`man7.org`, sha256 `61ed38a5…`). So the anchored remedy is inapplicable to the host's numbers, not merely documentary.

**Fix**: mark the bullet `[DOC-ONLY; host PAM unread]` (or quote without the assertive "forces"), or replace it with the host values and add `/etc/pam.d/{hyprlock,login,system-local-login,system-login,system-auth}` + `/etc/security/faillock.conf` to the host declaration table with sha256.

### P6-L2 — MEDIUM — `grace` is a CLI flag, not an unset config key

Note text:

> - `hide_cursor`, `fail_timeout`, `pam:module`, `grace` not set: defaults apply [LW:37, 49, 54].

Evidence at hyprlock v0.9.6:

- `src/config/ConfigManager.cpp` (sha256 `ca0f581f…`): `grep -n grace` → **0 hits**. The registered defaults are `:244 general:hide_cursor=0`, `:245 general:ignore_empty_input=0`, `:249 general:fail_timeout=2000`, `:251 auth:pam:enabled=1`, `:252 auth:pam:module=hyprlock`, `:253 auth:fingerprint:enabled=0`.
- `src/main.cpp:29` registers the CLI int option `grace`/`-g`; `:59` `int graceSeconds = argParser.getInt("grace").value_or(0);`; the only consumer is `src/core/hyprlock.cpp:67-68` (`if (graceSeconds > 0) m_tGraceEnds = …`).
- The note's own sentence lists **four** keys but cites **three** anchors; the wiki's grace row is [LW:16] under *Command-line Arguments*, not [LW:37/49/54].

Host effect: `~/.config/hypr/hyprlock.conf` (sha256 `b8d173…`) has no grace line and, at v0.9.6, cannot have one; `omarchy-system-lock:8-13` invokes `hyprlock` bare, so the effective grace is the CLI default **0**. The bullet's "defaults apply" is true only by CLI-default coincidence and misstates where the knob lives.

**Fix**: split the bullet — three conf keys with [LW:37/49/54]; separately "`grace` is CLI-only (`-g/--grace`), default 0 (`main.cpp:59`); the host invocation passes none".

### P6-L3 — LOW — `on-timeout` "otherwise" omits two upstream gates and their effect on `on-resume`

Note text:

> - **timeout / on-timeout** — `onIdled` returns without firing while any inhibit is held … Otherwise the command runs via `spawn(pListener->onTimeout);` [HC:327].

Source order (v0.1.8, sha256 `2dd4d73d…`):

- `HC:306-309` — empty `onTimeout` → log "Ignoring, onTimeout is empty." → return.
- `HC:312-323` — non-empty `conditionCmd` → `runConditionCmd`; non-zero → optionally schedule retry → return.
- `HC:326` — `pListener->onTimeoutFired = true;`
- `HC:327` — `spawn(pListener->onTimeout);`
- `HC:347-349` — `if (!pListener->onTimeoutFired)` → "Skipping onResumed…" → return.

So "otherwise" is false for (a) an empty `on-timeout` and (b) a `condition_cmd` that exits non-zero. A deferred condition also keeps `onTimeoutFired == false`, so **`on-resume` is suppressed too** — a coupling the note's condition bullet cites the wiki for but never states. Host impact is nil: `hypridle.conf:9-12` and `:15-19` both set non-empty `on-timeout` and no `condition_cmd`. The upstream contract sentence is still overbroad.

**Fix**: "Otherwise — and only if `on-timeout` is non-empty and, when set, `condition_cmd` exits 0 — `spawn(pListener->onTimeout)` runs [HC:326-327]".

### P6-L4 — LOW (provenance/recheck) — the stated anchor form does not mechanically reproduce the cited numbers

Both fetched pages match their SOURCES sha256 (`b45c03dc…` idle, `f69cff6b…` lock), and **every quoted string I checked is verbatim**. The defect is the extraction contract, not the quotes:

| reading | idle lines | lock lines |
|---|---|---|
| one line per block element, whitespace collapsed ("table cells run together") | 64 | 273 |
| block boundaries + preserved source newlines | 118 | 329 |
| cited range in S063/S064 | "6-120" | "6-85" |

Concrete misses under the literal block reading: warning at 6 (cited [LW:7]); `--grace` at 15 (cited 16); `hide_cursor` at 36 (37); `fail_timeout` at 48 (49); `pam:enabled` at 52 (53); faillock sentence at 73 (cited 84). The cited numbers are consistent with a parse that prepends one line and preserves intra-block newlines inside the code and animation-tree blocks (+11 before the System Configuration section) — a clause the anchor-form sentence does not state; I did not reconstruct the exact extractor end-to-end.

**Fix**: name the extractor (or ship the derived text files with their own sha256) so the note's recheck instruction ("re-anchor the cited lines") is executable by a third party.

---

## Attacks that failed (no finding)

- **All `Listeners` source anchors are exact**: `HC:301` (`m_iInhibitLocks > 0 && !pListener->ignoreInhibit`), `HC:326-327` (`onTimeoutFired = true; spawn(...)`), `HC:346-349` (guard + "Skipping onResumed: onTimeout was inhibited…"), `HC:352` (flag cleared), `HH:23` (`bool ignoreInhibit = false;`), `HH:26` (`conditionRetry`), `HC:68` (`onRestore = r.onResume`), `HC:70-72` (copy of `ignoreInhibit`/`conditionCmd`/`conditionRetry`), `HM:61` (`"ConfigManager: No hypridle.conf file found in:"`).
- **All quoted wiki/README strings are verbatim**: `[HR:5]`, `[HR:16]`, `[HR:20]`, `[HR:25]`, `[HR:28-29]`, `[HR:62]`, `[LR:5]`, `[LR:19]`; wiki config-required warning, listeners intro, on-resume sentence, `ignore_inhibit` row, condition rows, `--grace`, lock warning, faillock sentence.
- **The hyprlock wiki defaults match the tag source**: `hide_cursor=false`, `ignore_empty_input=false`, `fail_timeout=2000`, `pam:enabled=true`, `pam:module=hyprlock`, `fingerprint:enabled=false` ↔ `ConfigManager.cpp:244-253`.
- **The no-config warning matches source**: `resolveConfigPath` failure → `Log::CRIT " Config path error: …"` + `return 1` (`main.cpp:73-77`); config-init throw → `return 1` (`:80-86`).
- **`pam:module` fallback matches source**: `/etc/pam.d/<module>` missing → `su` (`Pam.cpp:70-72`). On this host `/etc/pam.d/hyprlock` exists, so the fallback is not taken — the note does not claim it is.
- **No `Listeners` bullet asserts host behaviour**; the injected-inhibit counter is fed by the ScreenSaver (dbus), systemd `BlockInhibited`, and name-owner-change paths (`Hypridle.cpp:516-595`), so "any inhibit" is outcome-accurate even though Wayland inhibitors act through the notification type rather than the counter.

## Residual risk / verification gaps

- All upstream checks are **tag-level** (hypridle `v0.1.8`, hyprlock `v0.9.6`). The note's version binding is a `pacman.log` line, not a running-binary fact; an Arch patch could differ. P6-L1 is version-independent: it is host PAM configuration, reached via the `hyprlock` service name.
- `pam_faillock` state is per-user and shared across services; `deny`/`unlock_time` are the stack's enforcement values, not an observed lockout. No failure was triggered.
- The [LW]/[HW] anchor numbers remain un-reproducible from the written convention (P6-L4); I did **not** find a wrong quote behind them.
- Nothing was executed from the lane; no `pacman`/`systemctl`/`hyprctl`/`loginctl`/`pidof`/binary version calls. Installs: **none**.

## Receipts

Fetched (curl, `--max-time`, raw bytes):

| file | sha256 |
|---|---|
| hypridle v0.1.8 `src/core/Hypridle.cpp` | `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` (matches S066) |
| hypridle v0.1.8 `src/core/Hypridle.hpp` | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` (S067) |
| hypridle v0.1.8 `src/main.cpp` | `379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38` (S068) |
| hypridle v0.1.8 `README.md` | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` (S065) |
| hyprlock v0.9.6 `README.md` | `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3` (S069) |
| hyprlock v0.9.6 `src/config/ConfigManager.cpp` | `ca0f581f933b08d0a2b10a0197432ac732233fa6d832120dbe989dd804bf97a0` |
| hyprlock v0.9.6 `src/main.cpp` | `606793cfcec83d7b9b5db03b92db728c6770cd782e75ff19f115949ac0176ae9` |
| hyprlock v0.9.6 `src/core/hyprlock.cpp` | `68b5491c4ea9105e51b31d1694c18c62efd4addaef24b261ff32556f56ce3663` |
| hyprlock v0.9.6 `src/auth/Pam.cpp` | `c74c78943c5bf9dc68f375060f6535cf8ca4bc1a2d0d31f78fe5541d89d02053` |
| wiki hypridle (HTML) | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` (S063) |
| wiki hyprlock (HTML) | `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5` (S064) |
| `pam_faillock(8)` (man7.org) | `61ed38a5feea94e89abb6c8e5e074218c1913495cc12e26926f2a54648b2dc44` |

Host files re-hashed and matching the note's table: `hypridle.conf` `e7d3b8dd…`, `hyprlock.conf` `b8d173dc…`, theme `3ef010e7…`, `omarchy-system-lock` `c1dd3881…`, `omarchy-system-wake` `09ad52b0…`, `omarchy-launch-screensaver` `ba783a3a…`, default autostart `acb6a668…`; ancillary `~/.config/hypr/autostart.conf` `5ace1701…`, `hyprland.conf` `ce7483f3…`. PAM bytes read: `/etc/pam.d/{hyprlock,login,system-local-login,system-login,system-auth}`, `/etc/security/faillock.conf`.
