# ReopenUnshare — partly falsified: S109/S112 bytes, quotes, tag pins and the default-path capability claim verify; falsified are (a) the S112 Gate admission under the Gate preamble's "version equals the host's installed tool" rule (pin man-pages 6.16; host has 6.19-1, installed 15 h before the gate fetch) and (b) the unqualified "`--map-current-user` gives no CAP_SYS_ADMIN" — `--keep-caps` (`unshare.1.adoc:97-98`) retains CAP_SYS_ADMIN in the exec'd payload and the same tmpfs mount succeeds.

Scope: SOURCES rows S109 (`corpus/SOURCES.md:121`) and S112 (`:124`), their Gate lines
(`corpus/lessons/round-20.md:46`, `:49`) under the gate preamble at `:24-32`, and the
consumer texts that cite them (`corpus/knowledge/tripwire-precision-r20.md:68`,
`corpus/QUALITY.md:244`). Refetch receipts: `.ufo/waves/round-20/w2/ReopenUnshare/fetch/receipts.jsonl`
(10 `mado-fetch-receipt-v1` lines, curl 8.23.0: S109's five row files, S112's two, both
S112 files at the peeled commit, and `sys-utils/unshare.c` for F5). Repro:
`w2/ReopenUnshare/repro.sh`.

## F1 — S109 (util-linux v2.42.4): holds

All five pinned files were refetched at the commit the row names and hash-match both the
row and the w1 receipt; the w1 stored bodies also re-hash to their receipts.

| file (at `d76cbf8f…`) | bytes | sha256 | row `…` prefix | receipt |
|---|---|---|---|---|
| sys-utils/unshare.1.adoc | 21,149 | `023e15ba559af1e3ea1e2eb7efdd0903dadc49af58cb433eef7411db937ba4ae` | `023e15ba…` ✓ | == |
| sys-utils/mount.8.adoc | 107,386 | `9df748670dde8f98af91c0ca023a364699e4aea16dd1c5b3398f0b4882629e6d` | `9df74867…` ✓ | == |
| libmount/src/context.c | 93,933 | `e8a67883eb37f459f255047ca325ffffc12427708487d3baab9d33ec9cb298e8` | `e8a67883…` ✓ | == |
| libmount/src/context_mount.c | 53,656 | `e486b4095f9d88bde837fcd1dad564549496bf1f6ad371f05d911f5ac6fc6363` | `e486b409…` ✓ | == |
| sys-utils/mount.c | 32,599 | `0fead9beac92b208c9e144aaa0aac5e47ce657adff271ddf78838aca1d47afa2` | `0fead9be…` ✓ | == |

Tag→commit pin (`git ls-remote https://github.com/util-linux/util-linux 'refs/tags/v2.42.4*'`):

```
a1d2b6980b84f38b389a6d6dda4a9623f47d13be	refs/tags/v2.42.4
d76cbf8f13e65ff657344f7f6a90042cf755ba59	refs/tags/v2.42.4^{}
```

Matches the row's "tag v2.42.4 (`a1d2b698…`) → commit `d76cbf8f…`". Host version equals
the pin: `unshare from util-linux 2.42.4`; `mount from util-linux 2.42.4 (libmount 2.42.4…)`.

Gate quote (`round-20.md:46`): `:132` — both fragments are verbatim on that one line, 13
words (≤ 25). Source line 132 contains, among the `--map-root-user` entry:

> "…have been mapped to the superuser UID and GID in the newly created user namespace.
> This makes it possible to conveniently gain capabilities needed to manage various
> aspects of the newly created namespaces (such as configuring interfaces in the network
> namespace or mounting filesystems in the mount namespace) even when run unprivileged."

Machine check printed `[True, True]`, `words: 13`. The row's further claims check out in
the same bytes:

- `context.c:80` — `cxt->restricted = (uid_t) 0 == ruid && !is_privileged_execution() ? 0 : 1;`
  (restricted is keyed on the real uid; a setuid/privileged exec also matters).
- `mount.c:46-58` `suid_drop()` calls `mnt_context_force_unrestricted(cxt)`; the
  two-positional branch `mount.c:1105-1114` (`argc == 2`, comment `D) mount <source> <target>`)
  calls `suid_drop()` when the context is restricted. `mount --bind a b` reaches this
  branch after option parsing (getopt removes `--bind`, leaving two argv entries).
- `context_mount.c:1755` takes `syserr = mnt_context_get_syscall_errno(cxt)`; `:1778-1790`
  maps an EPERM to `"permission denied"`/`"mount point is not a directory"` when
  `geteuid() == 0`, else to `"must be superuser to use mount"` — exactly the row's
  "only when `geteuid() != 0`". `mount.8.adoc:185` documents the since-2.35 behaviour of
  dropping suid instead of exiting.
- Observed (fresh private namespace, `/tmp` target): `unshare --map-current-user --mount`
  then `mount -t tmpfs tmpfs …` and `mount --bind …` both print
  `mount: /tmp/mado-r20w2-ReopenUnshare/t: must be superuser to use mount.` with rc=32.
  A failed mount(2), not an fstab policy miss — as the row says.

## F2 — S112 (man-pages 6.16): holds

| file (`?h=man-pages-6.16`) | bytes | sha256 | row `…` prefix | receipt |
|---|---|---|---|---|
| man/man7/user_namespaces.7 | 45,324 | `155d07c0186d2e9d52b253795b564f3041d3cd8ccd1474f3e3895896ffc5729a` | `155d07c0…` ✓ | == |
| man/man7/capabilities.7 | 53,128 | `40a71b475511625a03336562df0c5e7eded84a878200d2262e0d67a98b1baab5` | `40a71b47…` ✓ | == |

Tag→commit pin (`git ls-remote https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git 'refs/tags/man-pages-6.16*'`):

```
5d300a0fcb7df33de34f4e81d1c2d27ef94a850b	refs/tags/man-pages-6.16
29e0874dde8dd3e1ba555ca377b32ff18274a8e2	refs/tags/man-pages-6.16^{}
```

Matches the row. Refetching both files at the peeled commit
(`?h=29e0874d…`) returns the same sha256 as `?h=man-pages-6.16` — the tag and its commit
are byte-identical for these files.

Gate quote (`round-20.md:49`): `:277-280` renders exactly

```
277: Holding
278: .B CAP_SYS_ADMIN
279: within the user namespace that owns a process's mount namespace
280: allows that process to create bind mounts
```

which is the Gate string verbatim (19 words ≤ 25); the sentence continues on `:281`
("and mount the following types of filesystems:"), so the quote is an honest prefix.
Machine check printed `exact: True words: 19`.

Row claims verified in the same bytes: `:130-137` unshare(2)/setns(2) gain "a full set of
capabilities in that namespace"; `capabilities.7:1233-1238` a nonzero uid exec clears
permitted and effective; `capabilities.7:1296-1299` uid 0 makes the file inheritable and
permitted sets "notionally … all ones"; `user_namespaces.7:277-281` CAP_SYS_ADMIN in the
owning user namespace permits bind mounts and tmpfs (`:296`); `:350-352` a nonuser
namespace is owned by the user namespace the creator was in. For the default path the
row's conclusion — "the uid mapping, not the namespace itself, decides whether an exec'd
payload can mount" — is supported by the cited bytes and was reproduced (below); F5
shows the ambient-capability qualifier the row omits.

Capability controls (host kernel 7.2.11-arch1-1, private user+mount namespaces, /tmp
targets only):

- `--map-current-user`: `uid=1000`, `/proc/self/uid_map` = `1000 1000 1`,
  `capsh --print` → `Current: =` (no permitted/effective capabilities); tmpfs and bind
  mounts fail `must be superuser to use mount`, rc=32.
- `--map-root-user`: `uid=0`, uid_map = `0 1000 1`, `Current: =ep`, `TMPFS_OK`,
  `DIRBIND_OK`.

That is exactly the knowledge note's mechanism for the default invocation: the creating
process gets a full set in the new namespace, the exec'd program with a nonzero namespace
uid has it cleared, and the uid mapping decides the outcome. The scope is the default
only: `--keep-caps` changes it (F5).

## F3 — consumer support

- `corpus/knowledge/tripwire-precision-r20.md:68` — "`--map-current-user` gives no
  CAP_SYS_ADMIN in the mount namespace's owner; S109, S112". Supported by F1+F2 for the
  default invocation the round-19 harness used (no `--keep-caps`) and reproduced; false
  as an unqualified rule once `--keep-caps` is passed (F5).
- `corpus/QUALITY.md:244` (criterion 29) — "util-linux unshare/mount and the namespace
  capability rules (S109, S112)". Supported: the code paths and the namespace rules are
  the ones actually exercised by a stubbed-mount harness.
- `SKILL.md` does **not** cite S109/S112 anywhere: `grep -n "S109\|S112" SKILL.md` exits 1.
  The round-20 section at `SKILL.md:542` cites S110 for the `set -e` exception and uses
  QUALITY 29 for fail-closed harnesses but does not repeat or attribute the namespace
  claim. [INFERENCE] The assignment's "what … SKILL say[s]" half is vacuous for these two
  rows; the live consumers are the knowledge note and QUALITY 29.

## F4 — falsified part: S112 Gate admission vs the Gate preamble's version rule

`corpus/lessons/round-20.md:30` states the admission rule: "Admit tag- or commit-pinned
raw files whose version equals the host's installed tool". `:26-32` lists "man-pages
6.16" among the candidates and `:49` admits S112.

The host has **man-pages 6.19**, not 6.16:

- `/var/lib/pacman/local/man-pages-6.19-1/desc` → `%VERSION% 6.19-1`,
  `%INSTALLDATE% 1792469232` = `2026-10-20T04:07:12Z` — i.e. installed ~15 h before the
  w1 gate fetch at `2026-10-20T19:48:35Z`. (Read as a file, no pacman command run: the
  host pause forbids even `-Q`.)
- `/usr/share/man/man7/user_namespaces.7.gz` decompresses to 45,453 B,
  sha256 `c2b87e7d06469b4990248778985b0073009d3560ef238599cedfd8c10712de62`;
  `.TH user_namespaces 7 2026-02-08 "Linux man-pages 6.19"`.
  `/usr/share/man/man7/capabilities.7.gz` → 53,189 B,
  sha256 `8ac227c750e4dabfcf74d04b54c1489562485dfb37eafb134b1aa887bde53492`;
  `.TH Capabilities 7 2026-02-08 "Linux man-pages 6.19"`.

So the literal rule fails for S112 (pin 6.16 ≠ installed 6.19); it holds for S109
(pinned v2.42.4 = installed 2.42.4). The row itself never claims host equality, and the
claim is unaffected substantively: the full 6.16↔6.19 diff is header/copyright/URL-escape
only — `user_namespaces.7` has four changed lines, all in the header (two copyright
lines removed, `.TH` replaced), and `capabilities.7` changes the copyright line, `.TH`,
and two `\:` URL escapes. The quoted
sentence is byte-identical in 6.19 at `:279-282`, and the rules the note relies on are
unchanged. Options for L1: re-pin S112 to `man-pages-6.19` (digests above) or amend the
Gate wording to carve out docs-of-kernel rows; as written the admission record overstates
the rule for S112. [INFERENCE] fixed by either action, not by editing the row's claim.

## F5 — falsified part: the unqualified "no CAP_SYS_ADMIN" / "uid mapping … decides" wording

`unshare.1.adoc:97-98` documents `--keep-caps` ("When the *--user* option is given,
ensure that capabilities granted in the user namespace are preserved in the child
process"), and the pinned `sys-utils/unshare.c` (same commit, 38,989 B, sha256
`881e7a8048f448af078c3cf60c1521b63de466953b7a774eda70c769197efa8e`) implements it at
`:1320-1321`: `if (keepcaps && (unshare_flags & CLONE_NEWUSER)) cap_permitted_to_ambient();`
before `execvp`. Measured, not inferred:

```
$ unshare --map-current-user --keep-caps --mount --propagation unchanged sh -c \
    'capsh --print | sed -n "1,3p"; capsh --has-p=cap_sys_admin && echo HAS_CAP_SYS_ADMIN_P; \
     mount -t tmpfs tmpfs /tmp/mado-r20w2-ReopenUnshare/t && echo TMPFS_OK'
uid=1000(vgpnk) …
Current: =eip
Ambient set =cap_chown,cap_dac_override,…,cap_sys_admin,…      (the full bounding list)
HAS_CAP_SYS_ADMIN_P
TMPFS_OK
$ unshare --map-current-user --keep-caps --mount … python3   # non-setuid payload, mount(2) via ctypes
py_mount_rc 0 errno 0
CapPrm: 000001ffffffffff
CapEff: 000001ffffffffff
CapAmb: 000001ffffffffff
$ # same invocation without --keep-caps
cap[cap_sys_admin] not permitted
mount: /tmp/…: must be superuser to use mount.        (exit 32)
```

`capabilities.7:1179-1184` is the ambient-preservation rule (`P'(ambient) = (file is
privileged) ? 0 : P(ambient)`, and `P'(permitted)`/`P'(effective)` include it); the row
cites the section heading `:1171-1173` and the `:1234-1238` nonzero-uid clear sentence,
but not `:1179-1184`, so its summary omits the term that makes `--keep-caps` work.
`/usr/bin/mount` is setuid root on this host (`-rwsr-xr-x root:root`); the non-setuid
python ctypes payload mounts anyway, so the result is the ambient-capability effect, not
the setuid bit. The knowledge note's parenthetical and S112's closing clause "the uid
mapping, not the namespace itself, decides whether an exec'd payload can mount" are true
only of the default (no `--keep-caps`) invocation that round 19 used —
`SentinelGatePath.md` records "used `unshare --user --map-current-user --mount`" — so
they need that qualifier to stand as rules rather than as descriptions of one run. The
round-19 incident explanation itself stands. [INFERENCE] A one-clause fix ("without
`--keep-caps`") closes this; no row re-pin is needed for it.

## F6 — nits, non-blocking

- `corpus/knowledge/tripwire-precision-r20.md:67-68` shorthand: the process that calls
  unshare(CLONE_NEWUSER) does hold a full capability set in the new namespace
  (`user_namespaces.7:130-137`); what has no CAP_SYS_ADMIN by default is the program it
  execs with a nonzero namespace uid (`capabilities.7:1234-1238`). F5 is the sharper
  version of this concern.
- `corpus/SOURCES.md:121`: "unrestriced" typo (should be "unrestricted"); cosmetic.
- `corpus/SOURCES.md:124`: the ownership sentence cited as `:351-353` opens at `:350`
  ("When a nonuser namespace is created,"); content present, one-line offset.

## Limits

- Reproduction ran on kernel 7.2.11-arch1-1 where unprivileged user namespaces are
  allowed; a host with userns disabled would fail differently (ENOSPC/EINVAL at
  unshare), so the probe is host-scoped.
- All mount attempts were inside private user+mount namespaces with `/tmp` targets; no
  host-visible mount was created and no mount/namespace state was changed. File bind
  sources were `/etc/hostname` (read) and `/tmp`; the `--map-root-user` tmpfs and dir
  bind lived only in the ephemeral namespace. The `--keep-caps` arm retains
  CAP_SYS_ADMIN only in its ephemeral user namespace; [INFERENCE] it grants nothing over
  init-user-namespace resources and the mount it made died with its namespace.
- Host-pause compliance: no pacman/yay/paru/makepkg/expac/pactree/checkupdates, sudo,
  systemctl/journalctl/loginctl, hyprctl, libinput, wayland-info, walker, elephant,
  swaybg, waybar, alacritty, hypridle, hyprlock, omarchy-*, notify-send, screenshot,
  input/device probe, service/compositor operation, or live gate was run. The installed
  man-pages version came from reading `/var/lib/pacman/local/.../desc` and the installed
  `.gz` man files as bytes.
- Did not run the tripwire precision/recall/isolation suites: not part of this item.
- `w1` receipt bodies under `.ufo/waves/round-20/fetch/SrcUnshare/` were re-hashed
  (7/7 match their `receipts.jsonl`); this closes the "receipt says one digest, stored
  body says another" failure mode for these rows.
- [UNK] Not tested: behavior on a host where `user.max_user_namespaces=0` or an LSM
  blocks userns creation; the sources' claims are conditional on namespace creation.

## Installs

none.
