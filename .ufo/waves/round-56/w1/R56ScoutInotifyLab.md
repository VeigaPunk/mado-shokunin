# R56ScoutInotifyLab — inotify lab for the C1 entry's Limits section (wave w1)

Seat: read-only/lab research. No lane file edited, no git/jj mutation, no host write, no
compositor/service touched, no hold-out fixture sought or seen. No tool installed (inotifywait
absent on host; used python3 ctypes over glibc `inotify_init1`/`inotify_add_watch` — nothing to
record under RULES.md, no pacman, no uv/npx channel used).

## What was reproduced

`fetch/Hyprland-ConfigWatcher.cpp:52-72` (pin, Hyprland v0.56.2): for each path,
`inotify_add_watch(path, isDirectory ? directoryMask : fileMask)` with
`fileMask = IN_CLOSE_WRITE|IN_DONT_FOLLOW` (0x02000008) and
`directoryMask = fileMask|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM` (0x020003c8); when the
path is a symlink, a second watch on `canonical(path)` with bare `IN_CLOSE_WRITE` (0x8) — no
`IN_DONT_FOLLOW` on the canonical watch. These exact masks were placed with ctypes on scratch
files/dirs under `--work` only; the tool honours `--work`, never `/tmp`.

## Method and exact commands

```
command -v inotifywait            # empty → not installed
uname -r                          # 7.2.11-arch1-1
python3 -I /fast/scratch/hyaku/mado-r56/R56ScoutInotifyLab/inotify_lab.py \
  --work /fast/scratch/hyaku/mado-r56/R56ScoutInotifyLab/work     # pass 1: Hyprland-exact masks
python3 -I /fast/scratch/hyaku/mado-r56/R56ScoutInotifyLab/inotify_lab2.py \
  /fast/scratch/hyaku/mado-r56/R56ScoutInotifyLab/work2           # pass 2: self-event disambiguation
```
Host: python 3.14.8, kernel `7.2.11-arch1-1`, x86_64, glibc inotify_* via ctypes, non-blocking fd,
drained by select (0.5 s first, 0.15 s quiet tail). Every scenario got a fresh tree; files were
created before the watch was added and a pre-action drain confirmed silence.

## Pass 1 — observed events per scenario (Hyprland-exact masks)

File watch `IN_CLOSE_WRITE|IN_DONT_FOLLOW` on a regular file:

| scenario | events on the file watch |
|---|---|
| a1 in-place write (open/append/close) | `IN_CLOSE_WRITE` |
| a2 truncate-write (`open 'wb'`, O_TRUNC) | `IN_CLOSE_WRITE` |
| a3 `echo > file` | `IN_CLOSE_WRITE` |
| a4 editor atomic save (temp in same dir, rename over target) | `IN_IGNORED` only; follow-up write: NONE |
| a5 `touch` (utimensat) | NONE |
| a6 `mv` of the file away (rename in same dir) | NONE; recreated file at old path then written: NONE (old watch never sees the new inode) |
| (c1) `echo > existing file in dir` — dir watch | `IN_CLOSE_WRITE name='hyprland.conf'` (no `IN_CREATE`: O_TRUNC creates nothing) |
| (c6) `touch` — dir watch | NONE |

Symlink setup (watch 1 `IN_CLOSE_WRITE|IN_DONT_FOLLOW` on the link, watch 2 `IN_CLOSE_WRITE` on the
canonical target):

| scenario | events |
|---|---|
| b1 write through the symlink (open/append/close via link path) | `[symlink-watch]` NONE; `[canonical-watch] IN_CLOSE_WRITE` |
| b2 EXTRA: atomic save whose temp is renamed over the SYMLINK path | `[symlink-watch] IN_IGNORED` (symlink inode replaced by a regular file); `[canonical-watch]` NONE — canonical watch left on the old target |

Directory watch `IN_CLOSE_WRITE|IN_DONT_FOLLOW|IN_CREATE|IN_DELETE|IN_MOVED_TO|IN_MOVED_FROM`:

| scenario | events on the dir watch |
|---|---|
| c2 editor atomic save in the dir | `IN_CREATE name='.tmp-editor'`, `IN_CLOSE_WRITE name='.tmp-editor'`, `IN_MOVED_FROM name='.tmp-editor' cookie=0x1751e9f3`, `IN_MOVED_TO name='hyprland.conf' cookie=0x1751e9f3` (same cookie pairs the rename) |
| c3 `mv` file away (same dir) | `IN_MOVED_FROM name='hyprland.conf'` + `IN_MOVED_TO name='moved-away'`, same cookie |
| c4 `rm` file | `IN_DELETE name='hyprland.conf'` |
| c5 `mkdir subdir` | `IN_CREATE\|IN_ISDIR name='subdir'` |

Decisive lines (verbatim, pass 1):
```
# kernel: 7.2.11-arch1-1  arch: x86_64
    [file-watch] IN_CLOSE_WRITE                       (a1, a2, a3 — identical)
  after atomic save:
    [file-watch] IN_IGNORED                            (a4)
  after touch: NONE                                    (a5)
  after mv away: NONE                                  (a6)
    [canonical-watch] IN_CLOSE_WRITE                   (b1; symlink-watch silent)
    [dir-watch] IN_MOVED_FROM name='.tmp-editor' cookie=0x1751e9f3
    [dir-watch] IN_MOVED_TO name='hyprland.conf' cookie=0x1751e9f3   (c2)
```

## Pass 2 — why "nothing" is mask filtering, not absence of generation

Requested masks extended with `IN_MOVE_SELF|IN_DELETE_SELF|IN_ATTRIB` (everything else identical):

```
s1 mv-away (self mask requested): IN_MOVE_SELF
s2 rename-over (self mask requested): IN_ATTRIB
s2 rename-over (self mask requested): IN_DELETE_SELF
s2 rename-over (self mask requested): IN_IGNORED
s3 unlink (self mask requested): IN_ATTRIB / IN_DELETE_SELF / IN_IGNORED
s4a mv-away (Hyprland FILE_MASK): NONE
s4b write to MOVED path (old watch alive?): IN_CLOSE_WRITE   ← fired on the OLD wd (old inode)
s5 touch (IN_ATTRIB requested): IN_ATTRIB
```

Facts: the kernel does generate `IN_MOVE_SELF` on rename-away and `IN_ATTRIB`+`IN_DELETE_SELF`
(+`IN_IGNORED`) on replace-by-rename and on unlink — but inotify delivers an event only when its
bit is in the requested mask; `IN_IGNORED` is the one survivor under Hyprland's file mask. The
orphaned watch from a mv-away stays armed on the moved inode (s4b) and never sees a new file
created at the old path (a6 follow-up).

## Labeled inferences (event-plane only; beyond this is out of lab scope)

- INFERENCE: with this watch setup, in-place writes, truncate-writes, shell redirects and writes
  through a symlink are all visible as exactly one `IN_CLOSE_WRITE`; a mtime-only `touch` is
  invisible to both file and directory masks.
- INFERENCE: an editor-style atomic save (temp + rename over) is invisible to the `IN_CLOSE_WRITE`
  file watch (that watch dies with `IN_IGNORED`); the only mask-provided signal is the DIRECTORY
  watch's `IN_MOVED_TO` on the target name — so detection depends on the path list containing the
  file's parent directory. Whether Hyprland re-arms watches after `IN_IGNORED`/`IN_MOVED_TO` is
  Hyprland event-loop logic, not observable by this lab; unverified here.
- INFERENCE: the symlink canonical watch is what carries the reload-relevant event for writes
  through a symlink; the `IN_DONT_FOLLOW` link watch sees nothing (it watches the symlink inode).
- INFERENCE: replacing a symlink path by rename kills the link watch and strands the canonical
  watch on the old target (b2), and a watched file renamed away leaves a silent live watch on the
  moved inode (a6/s4) — under these masks both states are unsignalled.
- All of the above is kernel `7.2.11-arch1-1` behaviour; inotify(7)-era kernels may differ in the
  self-event filtering details. Host-vs-upstream-kernel equivalence is unverified.

## Input defects/ambiguities found by this seat

None. The fixture lines quoted by the seat spec (`fetch/Hyprland-ConfigWatcher.cpp:52-72`) match
registration §C2's mask model byte for byte, including the canonical watch being bare
`IN_CLOSE_WRITE`. The hold-out was never encountered.

## Not verified here

- Hyprland's own re-arm behaviour and which paths land in `m_configPaths` (other seats/pins cover
  that); this lab only establishes which events each mask produces.
- No hold-out fixture (H01-H08) was read or sought.

## Deliverables

- `.ufo/waves/round-56/w1/R56ScoutInotifyLab/inotify_lab.py` — pass-1 tool (honours `--work`)
- `.ufo/waves/round-56/w1/R56ScoutInotifyLab/inotify_lab2.py` — pass-2 self-event probe
- `.ufo/waves/round-56/w1/R56ScoutInotifyLab/raw-output.txt` — full pass-1 output (tee'd)

Scratch `/fast/scratch/hyaku/mado-r56/R56ScoutInotifyLab/` removed before yield.
