# ScoutTransport — live re-derivation of S258 (request-socket transport modes)

Lane: mado-shokunin. Round 38, wave 1. Scope: `corpus/knowledge/request-socket-live-bound-r8.md`
§2 S258 OBS, re-derived live on this host, read-only. All work was read-only on the lane;
the only writes are this report and scratch under `/tmp/mado38-ScoutTransport/`.

**Verdict: the transport claim RE-DERIVES. Every mode field agrees with the frozen receipt,
byte-for-byte. One metadata defect was found in the S258 registry row (declared receipt size
1401 B vs actual 673 B — the sha256, which is what the counters bind, was correct); it was
independently corroborated by three sibling lanes and has since been fixed at lane HEAD
`ff81aaf` by commit `b8400aa`, so it is closed.**

---

## 0. Instance identification (does the host still have the receipt's instance?)

The receipt's instance dir is `efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678`.
The live host reports the same signature:

```
$ echo "$HYPRLAND_INSTANCE_SIGNATURE"
efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678
```

```
$ hyprctl instances
instance efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678:
	time: 1792804449
	pid: 1619
	wl socket: wayland-1
```

```
$ find /run/user/1000/hypr -maxdepth 2 -type d
/run/user/1000/hypr
/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678
```

`find /run /tmp -maxdepth 3 -name '.socket.sock'` returns nothing else; `ls -d /run/user/*/hypr`
returns only `/run/user/1000/hypr`. **No instance drift — the receipt's instance dir is still the
live one.** Compositor uptime: `ps -o pid,lstart,etime -p 1619` → `Fri Oct 23 22:14:09 2026`,
`1-13:02:41` elapsed, so the same compositor process that was measured at receipt time is
still running (i.e. the socket objects are the same live objects, not re-created files).

---

## 1. The primary re-derivation

Command (the receipt's own command, run against the live instance):

```
$ D="$XDG_RUNTIME_DIR/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678"
$ stat -Lc '%a %F %n' "$D" "$D/.socket.sock" "$D/.socket2.sock"
700 directory /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678
755 socket /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket.sock
755 socket /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/.socket2.sock
```

Frozen receipt (`.ufo/waves/round-38/fetch/stat-sockets.txt`, last three lines) is
**byte-identical** to the live output:

```
$ diff -u <(tail -3 .ufo/waves/round-38/fetch/stat-sockets.txt) /tmp/mado38-ScoutTransport/live-stat.txt && echo IDENTICAL
IDENTICAL
```

| field | receipt says | live host | verdict |
|---|---|---|---|
| instance dir path | `efb50993…_1792804449_426444678` | same | **AGREE** (no move) |
| instance dir mode | `700` | `700` | **AGREE** |
| instance dir type | `directory` | `directory` | **AGREE** |
| `.socket.sock` mode | `755` | `755` | **AGREE** |
| `.socket.sock` type | `socket` | `socket` | **AGREE** |
| `.socket2.sock` mode | `755` | `755` | **AGREE** |
| `.socket2.sock` type | `socket` | `socket` | **AGREE** |

`stat -c` and `stat -Lc` agree (`diff` → `SAME`), so no symlink indirection is in play —
these are the real directory/socket objects.

---

## 2. Does an ACL or xattr change the story?

**No.** No extended ACL anywhere on the path, and no xattrs at all.

```
$ getfacl -p /run/user/1000/hypr
# file: /run/user/1000/hypr
# owner: vgpnk
# group: vgpnk
user::rwx
group::---
other::---

$ getfacl -p "$D"
# file: /run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678
# owner: vgpnk
# group: vgpnk
user::rwx
group::---
other::---

$ getfacl -c -E -p "$D"          # effective rights, no named entries
user::rwx
group::---
other::---
```

The sockets carry only the base triple (`other::r-x`), no named user/group entries:

```
$ getfacl -p "$D/.socket.sock" "$D/.socket2.sock"
# file: …/.socket.sock
# owner: vgpnk
# group: vgpnk
user::rwx
group::r-x
other::r-x
# file: …/.socket2.sock
… (identical)
```

xattrs — empty on the dir, both sockets, and the parent:

```
$ getfattr -m '.*' -d "$D" "$D/.socket.sock" "$D/.socket2.sock" "$XDG_RUNTIME_DIR/hypr"
$ echo $?
0        # rc=0 and no attribute lines printed ⇒ no extended attributes at all
```

`lsattr -d "$D"` prints only the header (no flags set). `lsattr` on the socket returns
`Operation not supported` — that is a tmpfs limitation on the socket inode, not a mode fact.

**Verdict: PASS.** The mode bits are the whole story. There is no POSIX ACL mask, no named
user/group grant, no `security.capability`/`security.selinux` xattr that would widen or narrow
access beyond what `stat` shows.

---

## 3. Can a non-owner stat inside? (the operational half of the claim)

`sudo` is present (`/usr/bin/sudo`, `sudo -n true` → OK), so the test ran as asked.

```
$ sudo -u nobody stat -Lc '%a %F %n' "$D"
stat: cannot statx '/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678': Permission denied

$ sudo -u nobody stat -Lc '%a %F %n' "$D/.socket.sock"
stat: cannot statx '…/.socket.sock': Permission denied

$ sudo -u nobody stat -Lc '%a %F %n' "$D/.socket2.sock"
stat: cannot statx '…/.socket2.sock': Permission denied

$ sudo -u nobody ls -la "$D"
ls: cannot access '…/efb50993…_426444678': Permission denied
```

The denial actually happens one level up — the whole runtime dir is closed:

```
$ sudo -u nobody stat -Lc '%a %F %n' /run/user/1000/hypr
stat: cannot statx '/run/user/1000/hypr': Permission denied
$ sudo -u nobody ls -la /run/user/1000
ls: cannot open directory '/run/user/1000': Permission denied
```

(`/run/user/1000` itself stats fine for `nobody` — 700 — because stat of the directory node
needs search on its *parent* `/run/user`, which is 0755; but traversal into it is refused.)

Alternate paths were probed too, in case a `/proc/<pid>/root` bypass existed:

```
$ sudo -u nobody stat -Lc '%a %F %n' /proc/1619/root/run/user/1000/hypr/efb50993…/.socket.sock
stat: cannot statx '…': Permission denied
$ sudo -u nobody ls -la /proc/1619/root/run/user/1000/hypr/efb50993…
ls: cannot access '…': Permission denied
$ sudo -u nobody ls -la /proc/1619/fd
ls: cannot open directory '/proc/1619/fd': Permission denied
```

Group exposure: `getent group 1000` → `vgpnk:x:1000:` — the socket's group is a
single-member group, so the `group::r-x` bits on the sockets grant nothing to anyone else.
Parent chain modes:

```
$ stat -Lc '%a %u %g %F %n' "$XDG_RUNTIME_DIR" "$XDG_RUNTIME_DIR/hypr" "$D" "$D/.socket.sock" "$D/.socket2.sock"
700 1000 1000 directory /run/user/1000
700 1000 1000 directory /run/user/1000/hypr
700 1000 1000 directory /run/user/1000/hypr/efb50993…_426444678
755 1000 1000 socket   /run/user/1000/hypr/efb50993…_426444678/.socket.sock
755 1000 1000 socket   /run/user/1000/hypr/efb50993…_426444678/.socket2.sock
```

`/run/user/1000` is a tmpfs mounted `mode=700,uid=1000,gid=1000` (`findmnt -no OPTIONS /run/user/1000`),
so the 0700 instance dir sits inside a 0700 mount owned by the same uid.

**Verdict: PASS.** The entry's operative sentence — "nothing outside the user's own UID
reaches the socket path" — holds under direct test as a non-owner.

---

## 4. Is the measured path the *live* request socket? (provenance of the object)

The stat was taken against socket objects the compositor actually holds and listens on, so
"live bound" is not a claim about a stale file:

```
$ grep -E "hypr/[^ ]*/\.socket2?\.sock$" /proc/1619/net/unix | awk '{print $5,$6,$7,$8}'
0001 01 37746   …/.socket.sock        # SOCK_STREAM, unconnected/listening
0001 01 38117   …/.socket2.sock      # SOCK_STREAM, unconnected/listening
0001 03 10029   …/.socket2.sock      # connected client
0001 03 181151236 …/.socket2.sock
0001 03 235508591 …/.socket.sock
```

Both paths appear in the compositor's own unix socket table with type `0001` (SOCK_STREAM).
`ls -l /proc/1619/fd | grep -c 'socket:\[37746\]'` → `2`: the compositor holds the
`.socket.sock` listener inode. `hyprland.lock` in the same dir contains `1619`/`wayland-1`,
matching the compositor pid.

Note: no socket was connected to and no request was sent — only `hyprctl instances`
(a read verb) was used, per the lane bounds.

---

## 5. Quote / digest fidelity of the S258 gate

```
$ sha256sum .ufo/waves/round-38/fetch/stat-sockets.txt
fcc608203f66879f469b61761619e555e04b67127f215d495bd35b9b27421928
```

Matches the frozen pin in `corpus/lessons/round-38.md:16` and in the counter's pin table
(`quality/counters/c2-r38-request-ground.py:72`) exactly, and matches the committed blob
(`git show HEAD:.ufo/waves/round-38/fetch/stat-sockets.txt | sha256sum` → same digest).

Quote check, byte-level:

```
$ python3 -c "…"
quote occurrences in receipt bytes: 1
quote in entry body: 1
```

The Gate quote `directory /run/user/1000/hypr/` occurs exactly once in the receipt bytes and
once in the entry body (`corpus/knowledge/request-socket-live-bound-r8.md:47`).

**PASS.**

---

## 6. FINDING — the S258 registry row declares a wrong receipt byte size

`corpus/SOURCES.md:222`, anchor cell:

```
…; receipt 1401 B sha256 `fcc608203f66879f469b61761619e555e04b67127f215d495bd35b9b27421928`
```

The committed receipt is **673 B**, not 1401 B:

```
$ wc -c .ufo/waves/round-38/fetch/stat-sockets.txt
673 .ufo/waves/round-38/fetch/stat-sockets.txt
$ git cat-file -s $(git rev-parse HEAD:.ufo/waves/round-38/fetch/stat-sockets.txt)
673
```

The declared size is wrong by 728 bytes. The **sha256 in the same cell is correct** and binds
to the 673 B file, so this does not break any digest binding — it is a metadata inaccuracy in
the row that carries the S258 claim.

Severity: **minor / cosmetic-but-false**. It is a factual statement about the artifact, and
it is the only field of the row that does not re-derive. Nothing currently catches it:
`grep -rn 1401 quality/ .ufo/waves/round-38/` finds it **only** in `corpus/SOURCES.md` —
the request-ground counter validates the row's cell *shape*, `status`, `used-by` and the
Gate-line digest, but never the declared byte size; the fleet census validator
(`scripts/sources-census.sh`) has no byte-size check either (`grep -n "byte\|wc -c\|stat -c %s"`
→ no match). So the counter's TARGET_MET at HEAD is unaffected by this — but the number is
wrong and should be 673 B.

Scope note: the row's declared size was introduced in `245065c` (2026-10-25 11:08) while the
receipt blob was added in `58e55ec` (2026-10-25 09:40) at 673 B and has never been a
different size in any commit reachable from any ref:

```
$ for c in 58e55ec 0bcd01d a3b2d8b ca7db0c; do echo -n "$c size="; git cat-file -s $(git rev-parse $c:.ufo/waves/round-38/fetch/stat-sockets.txt); done
58e55ec size=673
0bcd01d size=673
a3b2d8b size=673
ca7db0c size=673
```

So 1401 B does not correspond to any committed version of this receipt — it appears to be a
transcription of an earlier, larger scratch capture. **[INFERENCE]** as to origin.

### 6a. Origin hunt (closed, negative)

An exhaustive bounded search for the 1401-byte capture found nothing:

```
$ grep -rl "700 directory /run/user/1000/hypr" <fleet root> --include='*.txt' --include='*.md' …
mado-shokunin/.ufo/waves/round-38/fetch/stat-sockets.txt     # the 673 B committed receipt
mado-shokunin/.ufo/waves/round-38/w1-spec.json                # my own dispatch prompt
mado-shokunin/.ufo/waves/round-38/w1/reports/ScoutTransport.md
mado-shokunin/.ufo/waves/round-38/w1-dispatch.json
```

No other capture exists anywhere under the fleet root or in any sibling sandbox clone.
All eight sibling clones of the receipt (`/tmp/mado38-*/sb*/.ufo/waves/round-38/fetch/stat-sockets.txt`,
from LabratClockSkew, LabratProcProof, RevC2v3×3, RevDomCounter, RevM37Routing, SentSocketSafety)
are **673 B with digest `fcc608203f66879f…`** — identical to the lane's.

No file of exactly 1401 bytes exists under `/tmp/mado38-*` (maxdepth 6) or under the fleet
root's `.ufo` trees; the only 1401-byte files found in the fleet root are unrelated
git objects and fixture files in other lanes (`kaidoku-shokunin/.git/objects/…`,
`audio-shokunin/corpus/live/r94-scout/runs/analysis-remix.txt`, `lore-shokunin/corpus/fixtures/…`).

I also tried to reconstruct a plausible 1401 B capture from the command's own output
(`stat` over 4–5 paths, `ls -la`, `getfacl`, and combinations) — every candidate lands
between 443 B and 1250 B; none hits 1401. The number has **no reconstructable origin** from
this command's output. Combined with the size never appearing in any commit of the file,
the most economical explanation is a hand-entered number that was never checked against
the artifact. **[INFERENCE]**, stated at that confidence because the negative is now
exhaustively established.

### 6b. Independent corroboration

This finding is not unique to this lane's read. Three sibling reviewers in this same wave
independently reached it:

- `.ufo/waves/round-38/w1/reports/RevRegistry.md:87,90,108` — lists `S258 | receipt 1401 B`
  vs `stat-sockets.txt = 673 B`, and notes neither the request-ground counter nor
  `sources-census.sh` validates byte counts.
- `.ufo/waves/round-38/w1/reports/RevDomCounter.md:119` — "S258 `1401 B` vs 673 B".
- `.ufo/waves/round-38/w1/reports/ScoutS253.md:316,340` — same observation, same conclusion
  that neither counter checks byte counts.

Four independent lanes converging on the same unchecked false size cell is the strongest
available evidence that this is a real gap rather than an artifact of my own method.

### 6c. The finding is now FIXED at HEAD — verified

A sibling agent's seat-fix commit `b8400aa` ("registry row corrections (sizes/anchors/stamp/
S277 URL)") corrected the cell while this report was being written. At the current lane HEAD
(`ff81aaf`) the row reads:

```
$ git show HEAD:corpus/SOURCES.md | grep "^| S258 " | grep -o "receipt [0-9]* B sha256 \`[0-9a-f]\{16\}"
receipt 673 B sha256 `fcc608203f66879f
```

and the receipt at HEAD is still the same 673 B / `fcc60820…` artifact. The row now states the
artifact's true size; the digest was never wrong and is unchanged.

The same commit also added S258 to the entry's `source:` line, closing the adjacent observation
in §7.3 that I had flagged for the owning reviewers:

```
$ git show HEAD:corpus/knowledge/request-socket-live-bound-r8.md | grep -n "source:"
source: S158 — … ; S187 — …; S277 — …; S258 — host socket stat receipt
`.ufo/waves/round-38/fetch/stat-sockets.txt` (own-work)
```

So **item 10 is closed at HEAD**, and item 11's second half (the `source:`-line omission) is
closed as well. The remaining precision notes in §7.1 and §7.2 stand as written.

Adjacent context (not a defect in the claim): the same scan shows 7 other SOURCES.md rows whose
declared `N B` does not match their receipt file — S203, S206, S207, S208 (round 35) and S221,
S253, S277 (round 38). For S221/S253/S277 the declared number plausibly describes the
*upstream* document, while the sha256 describes the local receipt — two different objects in
one cell, which is itself a clarity problem. S258 has no such split: its cell says "receipt
1401 B sha256 …", both about the same file, and the size is simply wrong.

---

## 7. Precision notes on the entry's wording (no falsification)

1. `corpus/knowledge/request-socket-live-bound-r8.md:47` reads *"the instance directory
   `directory /run/user/1000/hypr/` carries mode 0700"*. The quoted fragment is a **prefix of
   the instance path**, not the parent path — the receipt's stat line is
   `700 directory /run/user/1000/hypr/efb50993…_426444678`. The trailing slash makes the
   fragment read like the parent directory `/run/user/1000/hypr/`. Substantively harmless:
   the parent is also 0700 (`stat` above), so the mode claim holds under either reading.
2. The row's `teaches` cell — "the directory mode is the effective access control" — is true
   but not the *whole* mechanism. Independently, Linux requires **write** permission on a
   pathname socket inode to connect (`man 2 connect`: "For UNIX domain sockets … Write
   permission is denied on the socket file"; `man 7 unix`: "connecting to a stream socket
   object requires write permission on that socket"). The sockets are 0755 — `other` has
   r-x and **no w** — so a non-owner could not connect even if the directory were traversable:

   ```
   owner w: True   group w: False   other w: False
   owner r: True   other r: True     other x: True
   ```

   The directory 0700 blocks traversal; the socket's own missing `w` for others blocks connect.
   Two independent barriers. The entry's claim is a correct lower bound, not a false statement.
3. Adjacent observation, flagged for the reviewers who own those clauses rather than asserted
   here: the entry's `source:` line listed `S158, S187, S277` — not S258 — even though the
   body carries an `**OBS** S258:` line and `SOURCES.md`'s S258 row names this entry in
   `used-by`. At the commit this report was first written (`3f14bd2`),
   `python3 quality/counters/c2-r38-request-ground.py --repo . --rev HEAD` reported
   `ids=S158,S187,S277` for this entry and still `verdict=TARGET_MET`, i.e. the S258 row was
   reached through the registry's used-by closure and the Gate block rather than through the
   entry's `source:` line. **Closed at HEAD `ff81aaf`**: `b8400aa` added S258 to the `source:`
   line (verified in §6c), so the row and the entry now name each other in both directions.

---

## 8. Commands run (complete list, all read-only)

```
echo "$HYPRLAND_INSTANCE_SIGNATURE"; hyprctl instances
find /run/user/1000/hypr -maxdepth 2 -type d
find /run /tmp -maxdepth 3 -name '.socket.sock'
ls -d /run/user/*/hypr
ps -o pid,lstart,etime,cmd -p 1619
stat -Lc '%a %F %n' <dir> <dir>/.socket.sock <dir>/.socket2.sock
stat -c  '%a %F %n' <same>            # -c vs -Lc: SAME
stat -Lc '%a %u %g %F %n' /run/user/1000 /run/user/1000/hypr <dir> <both sockets>
stat -Lc '%i %n' <both sockets>
getfacl -p /run/user/1000/hypr <dir> <both sockets>
getfacl -c -E -p <dir>
getfattr -m '.*' -d <dir> <both sockets> /run/user/1000/hypr
lsattr -d <dir> <both sockets>
sudo -u nobody stat -Lc '%a %F %n' <dir> <both sockets> /run/user/1000/hypr /run/user/1000
sudo -u nobody ls -la <dir> /run/user/1000
sudo -u nobody stat -Lc … /proc/1619/root<dir>/.socket.sock
sudo -u nobody ls -la /proc/1619/root<dir> /proc/1619/fd
getent group 1000; getent passwd | awk -F: '$4==1000 {print $1,$3}'
findmnt -no TARGET,SOURCE,FSTYPE,OPTIONS /run/user /run/user/1000
grep -E "hypr/[^ ]*/\.socket2?\.sock$" /proc/1619/net/unix
ls -l /proc/1619/fd | grep socket
cat <dir>/hyprland.lock
sha256sum .ufo/waves/round-38/fetch/stat-sockets.txt ; wc -c same
git show HEAD:.ufo/waves/round-38/fetch/stat-sockets.txt | sha256sum ; git cat-file -s …
git log --format='%h %s' -- .ufo/waves/round-38/fetch/stat-sockets.txt
git log --format='%h %ad %s' --date=iso -S"1401 B sha256" -- corpus/SOURCES.md
git status --porcelain ; git rev-parse HEAD
python3 quality/counters/c2-r38-request-ground.py --repo . --rev HEAD
```

**No socket was connected to. No request was sent. No hyprctl verb other than `instances`
(a read verb) was used. No compositor, config, service or package was touched. No lane
production file was edited; no git write was performed in the lane** (`git status --porcelain`
at the end shows only untracked wave-38 scratch/report paths created by this wave's agents,
including this report).

The lane HEAD advanced twice while this report was being written — `3f14bd2` → `b8400aa` →
`ff81aaf` — by sibling agents' seat-fix commits. **Neither advance is mine.** I re-verified
every field of my scope at the final HEAD `ff81aaf22125390a9df543156c149844248eaa6e`:

```
$ git rev-parse HEAD
ff81aaf22125390a9df543156c149844248eaa6e
$ git show HEAD:corpus/lessons/round-38.md | grep "GATE S258"
GATE S258 receipt=.ufo/waves/round-38/fetch/stat-sockets.txt sha256=fcc608203f66879f469b61761619e555e04b67127f215d495bd35b9b27421928 quote="directory /run/user/1000/hypr/"
$ diff <(git show HEAD:.ufo/waves/round-38/fetch/stat-sockets.txt | tail -3) <(stat -Lc '%a %F %n' "$D" "$D/.socket.sock" "$D/.socket2.sock") && echo IDENTICAL
IDENTICAL
$ sudo -u nobody stat -Lc '%a %F %n' "$D/.socket.sock"
stat: cannot statx '…/.socket.sock': Permission denied
```

The Gate pin, the receipt bytes, the live mode fields and the non-owner denial all still hold
at the final HEAD; the S258 registry row's size cell is now correct (§6c).

---

## 9. Summary table

| # | item | verdict |
|---|---|---|
| 1 | live instance dir == receipt's instance dir (no move) | **PASS** |
| 2 | instance dir mode 0700 | **PASS** (live `700`, identical bytes) |
| 3 | `.socket.sock` mode 0755 | **PASS** |
| 4 | `.socket2.sock` mode 0755 | **PASS** |
| 5 | no ACL changes the story (`getfacl -p`) | **PASS** |
| 6 | no xattrs change the story | **PASS** |
| 7 | non-owner cannot stat inside (`sudo -u nobody stat`) | **PASS** (EACCES at `/run/user/1000`) |
| 8 | gate quote verbatim in receipt bytes, digest matches pin | **PASS** |
| 9 | measured objects are the compositor's live sockets | **PASS** |
| 10 | SOURCES.md S258 row declares receipt as 1401 B; actual 673 B | **FINDING (minor) — FIXED at HEAD `ff81aaf` by `b8400aa`**; origin hunt negative; corroborated by RevRegistry / RevDomCounter / ScoutS253 |
| 11 | entry §2 wording: quoted path fragment reads like the parent dir; "directory mode is the effective access control" is a lower bound (socket 0755 also lacks `w` for others) | **NOTE (precision only)** |

Tooling: **no installs were needed** — `getfacl` (2.4.0), `getfattr` (2.6.0), `stat` (0.8.0),
`sudo`, `python3` and `hyprctl` were all already present on the host. No pacman/uv/npm
transaction was performed. Scratch written only to `/tmp/mado38-ScoutTransport/`
(`live-stat.txt`, `receipt-stat.txt`).
