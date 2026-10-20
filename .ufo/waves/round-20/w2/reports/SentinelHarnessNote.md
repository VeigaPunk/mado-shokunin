# SentinelHarnessNote — partly falsified: the prose warnings hold, but `isolate.sh` itself is a live-session pass-through whose "passes the check" transcript can be read as containment, and a PATH-resolved `cmp` fails it open

Attacked: whether a future seat could read `isolation-check.sh` passing `isolate.sh` as "safe to run hyprctl inside", plus the cheap guards the item names. Empirically, a payload under `isolate.sh` (a4046a8, sha256 `332b3fed6ad680f0bd2eec35ff686b768e2619a828925f13d429807a817fcccc`) inherits the live session, writes the host filesystem, and — under a stubbed `cmp` — runs with a completely unbound target.

## Finding 1 — "not a sandbox" is documented in prose but absent from the artifact and its check transcript; a seat reading the transcript alone can misread the pass

- `SKILL.md:569-571` does warn: `isolate.sh` "is not a sandbox (the environment and the compositor/session sockets stay reachable) and gives no licence to run a host probe while the host pause binds." `QUALITY.md:246-248` and `corpus/knowledge/tripwire-precision-r20.md:78-80` repeat it. On the documented-artifact axis, the claim survives.
- But the two artifacts a seat actually runs carry no hint:
  - `isolate.sh` itself: 76 lines, one comment (`:37-38`, about the ready marker), usage line (`:5`) says only `--stub/--target/-- CMD`. Nothing names the env/socket pass-through.
  - `isolation-check.sh` output ends `FAIL_CLOSED isolate.sh mode=…` ×6 + `POSITIVE_CONTROL_OK isolate.sh`, `exit=0` (`evidence/crit29-isolate.txt`). No trailing caveat; the word "sandbox"/"environment"/"socket" never appears in the transcript.
  - `isolate.sh` is not in the SKILL gate-registry table (`SKILL.md:580-616` — only `isolation-check.sh` is, SCORECARD.md:1343 as "harness fail-closed check"), so the registry's per-tool write-scope column never fires for it.
- Counterexample confirmed, not hypothetical — the payload below ran under the harness in /tmp and observed:

```
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792501032_1839528943
WAYLAND_DISPLAY=wayland-1
DBUS_SESSION_BUS_ADDRESS=set
XDG_RUNTIME_DIR=/run/user/1000
hyprctl resolves to: /usr/bin/hyprctl
LIVE hyprctl socket REACHABLE: /run/user/1000/hypr/…/.socket.sock
```

  Command: `/tmp/mado-r20w2-SentinelHarnessNote/.ufo/waves/round-20/isolate.sh --stub /tmp/shn-demo/stub --target /tmp/shn-demo/target -- /tmp/shn-demo/probe.sh`, exit 0. This reproduces w1 SentinelPause20 H3 (`w1/reports/SentinelPause20.md:64-75`) and adds that `command -v hyprctl` resolves — `hyprctl` with `HYPRLAND_INSTANCE_SIGNATURE` set needs nothing else to drive the live compositor. So a seat that ran `isolation-check.sh isolate.sh`, saw 7 green lines, and exec'd `hyprctl` as CMD would be issuing live IPC. The doc warnings are the only barrier, and they sit three files away from the green output.

- Second demonstration — the "containment" boundary does not exist for the filesystem either: payload `echo … > /tmp/shn-demo/host-write-proof.txt` succeeded and `cat` confirmed `written-by-isolate-payload` on the host; only the stubbed target showed stub bytes. `unshare --user --map-root-user` does not confine writes outside the stubbed paths.

## Finding 2 — real fail-open: `cmp` is PATH-resolved, so a successful no-op mount passes verification

`isolate.sh:58,61`: `command mount --bind …` then `cmp -s -- "$target" "$stub"`. `command` bypasses shell *functions* only; both binaries still resolve through the caller's PATH. Demonstrated:

```
PATH=/tmp/shn-demo/fakebin:$PATH ./.ufo/waves/round-20/isolate.sh --stub stub --target target2 -- canary.sh
harness-exit=0
PAYLOAD RAN — target bytes: orig-real-bytes
```

with `fakebin/mount` = `exit 0` (no bind) and `fakebin/cmp` = `exit 0`. The payload ran with the real target exposed — exactly the mount-noop mode the checker is meant to catch, defeated by a tool the checker never stubs (`isolation-check.sh` stubs only `mount` and `unshare`, lines 65-107; it even `unset -f`s functions at :18 but leaves `cmp` PATH-resolved). Same exposure applies to `mktemp`, `rm`, `bash` in the ready-marker path. Severity: medium — requires a hostile/mistaken PATH, but that is precisely the class of error the harness exists to survive, and the checker's own injection mechanism proves PATH is attacker/caller-controlled.

Smallest safe correction (kernel-side, no new PATH dependency): replace the `cmp` loop with a `/proc/self/mountinfo` membership check, which the kernel cannot fake via PATH:

```bash
for target in "${targets[@]}"; do
    command mount --bind "$stub" "$target" || exit 125
done
for target in "${targets[@]}"; do
    # field 5 is the mount point; a no-op or shadowed mount leaves no row
    while read -r _ _ _ _ mp _; do [[ $mp == "$target" ]] && continue 2; done < /proc/self/mountinfo
    exit 125
done
```

(verified: under the real harness, `/proc/self/mountinfo` inside the child lists `/tmp/shn-demo/target3` as a mount point). Note `mountinfo` field 5 is the target path with space-escapes — fine for `/tmp` harness paths; if retained alongside `cmp`, keep `cmp` too so the checker can still distinguish bound-with-wrong-bytes. Caveat: this makes the harness *more* fail-closed against the checker's PATH stubs, not less checkable — `mount-nonzero`, `unshare-refused`, `missing-*` still fail first.

## Finding 3 — the named cheap guards, evaluated

- **Refuse non-/tmp targets: reject.** The documented purpose is stubbing *host* binaries/config paths (round-19 lesson M2 was a real `/usr/bin/hyprctl` probe). `isolate.sh:12-35` accepts any path deliberately; the checker's own fixtures stay in /tmp only because the check runs benign payloads. A /tmp allowlist would remove the harness's reason to exist — the fix is honesty (warning), not a fake boundary. W1 SentinelPause20 H3 noted the same (`:67` "no /tmp allowlist" is descriptive, and the w1 item never proposed adding one [INFERENCE from gen_w1.py:92 spec]).
- **Scrub env: cheap, worth it, but hygiene not containment.** In the child before `exec`: `unset HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY DISPLAY DBUS_SESSION_BUS_ADDRESS SWAYSOCK I3SOCK XDG_CURRENT_DESKTOP` (keep `XDG_RUNTIME_DIR` — scrubbing it breaks legitimate needs while the dir stays reachable). With `HYPRLAND_INSTANCE_SIGNATURE` unset, `hyprctl` fails fast instead of reaching the socket — it closes the *accidental* foot-gun. It does not stop a deliberate payload (`ls $XDG_RUNTIME_DIR/hypr/` revealed the signature directory in the demonstration above), so it must not be documented as isolation.
- **Stronger-but-still-cheap options, ranked:** (a) `unshare --net` kills abstract-socket DBus but not filesystem sockets (hypr socket is `fs` — no help); (b) bind a stub dir over `$XDG_RUNTIME_DIR/hypr` as an extra mount — works, but needs a non-/tmp target, i.e. it conflicts with the rejected /tmp allowlist and adds a second attack surface; (c) the mountinfo guard above — recommended.

## Proposed warning text (exact)

1. Header comment in `isolate.sh`, after `set -u`:

```bash
# NOT A SANDBOX. This only bind-mounts STUB over each --target inside a private
# mount namespace. The payload inherits the full environment, the host filesystem
# (all unstubbed paths are read/write as the caller), and every session socket
# ($XDG_RUNTIME_DIR/hypr/*, wayland-*, D-Bus). A FAIL_CLOSED result from
# isolation-check.sh means "payload never ran after a setup failure" — it says
# nothing about containment. Do NOT run host probes (hyprctl, pacman, omarchy-*)
# as CMD; while the host pause binds they are forbidden inside or out.
```

2. Same caveat in `usage()` so it prints on every misuse:

```bash
printf '%s\n' 'NOTE: not a sandbox — env, host fs and session sockets pass through.' >&2
```

3. Trailing line in `isolation-check.sh` before `exit 0` (and symmetric text on `exit 1`), so the green transcript carries its own scope:

```bash
printf 'SCOPE %s: fail-closed setup only; not a sandbox — payload keeps env, host fs and session sockets.\n' "$harness_name"
```

4. Optional child-side scrub (Finding 3): `unset HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY DISPLAY DBUS_SESSION_BUS_ADDRESS SWAYSOCK I3SOCK` before `exec "$@"` — documented as hygiene only.

## Verdict on the attacked claim

- Holds: the three prose locations do say "not a sandbox / no licence to run a host probe"; a careful reader of SKILL.md/QUALITY/knowledge is warned.
- Falsified in part: "as documented" is thinner than the green-transcript reality — the harness, its usage, and the check output carry zero scope text, so a seat that meets the tool through `isolation-check.sh` output can plausibly read pass-as-safe; and the `cmp` PATH resolution is a concrete fail-open the current docs don't name (the QUALITY limit covers only *absolute-path* resolution bypassing the checker, `QUALITY.md:244-245` — the inverse case, PATH stubs *defeating* the harness's own verifier, is unlisted).
- Smallest safe correction: the three warning insertions + env scrub (one round of edits, no contract change); mountinfo verification as the follow-up hardening.

## Limits

- Did not run `hyprctl` or touch any live socket (host pause); reachability was shown by env inheritance, `command -v`, and `-S` stat only.
- The PATH-stub bypass requires caller-controlled PATH — realistic for ad-hoc harness reuse, not for a clean checkout run.
- `usage-exit` shown by my pipeline read 0 because `head` consumed the pipe; `isolate.sh` bare actually exits 125 per `:6` (the pipe masked it) — cosmetic, no impact.
- Did not test `--propagation private` interactions, directory-vs-file stub mismatches, or multi-target partial success; outside this item.
- mountinfo matching needs octal-escape handling if targets ever contain spaces; harness targets today are `/tmp/mado-*` paths.

## Installs

none.
