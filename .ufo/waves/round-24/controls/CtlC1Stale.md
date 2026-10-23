# CtlC1Stale — stale-source control

Control: added an eight-claim note using only existing SOURCES rows S016–S020, with each quote checked against its source bytes; added only the note path to those five `used-by` cells and indexed the note in README. The variant additionally rewrites those rows' `opened` cells from 2026-10-19 to 2026-10-23 (append-only violation). Neither control changes the claims, quotes, source URLs, or hashes.

## Source-byte provenance

Fetched before building the note:
- S016 `https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/` — sha256 `24c3987dd95986ef306edf14804c4a959c5846d4a105d70bb1d58f6b78c6b468`; quote `getprop`.
- S017 `https://wiki.hypr.land/Configuring/Basics/Window-Rules/` — sha256 `15ab38f26e31dcf1f0523e0735190112a2f4430260d5916b92cb14b8ac6118a2`; quotes `match`, `props`.
- S018 `https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/debug/HyprCtl.cpp` — sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`; quotes `PROP`, `getprop`.
- S019 quotes the exact captured line in `.ufo/evidence/round-12/getprop-help.txt`: `usage: hyprctl [flags] getprop <regex> <property>`.
- S020 quotes exact lines read from `/home/vgpnk/.local/share/omarchy/default/hypr/windows.conf` and `.../apps/terminals.conf` (the two `windowrule = opacity ... match:tag ...` lines).

## Exact setup and commit commands

`timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale`
`timeout 60 git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale checkout -q 4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`
Base commit command: `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale add corpus/SOURCES.md corpus/README.md corpus/knowledge/rule-attribution-r24.md && timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale -c user.name=ctl -c user.email=ctl@local commit -m 'control: cite stale sources for C1'`

Base control commit: `f5fddaeb83ca809ca8c18ce49af26acdb0309ba5`.
`git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale show --stat f5fddaeb83ca809ca8c18ce49af26acdb0309ba5`:
```
commit f5fddaeb83ca809ca8c18ce49af26acdb0309ba5
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:38:14 2026 -0300

    control: cite stale sources for C1

 corpus/README.md                         |  1 +
 corpus/SOURCES.md                        | 10 +++++-----
 corpus/knowledge/rule-attribution-r24.md | 14 ++++++++++++++
 3 files changed, 20 insertions(+), 5 deletions(-)
```

Variant commit command: `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale add corpus/SOURCES.md && timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale -c user.name=ctl -c user.email=ctl@local commit -m 'control variant: rewrite source opened dates'`

Variant commit: `a62dd4837b8e2e3e50d04f512700c6a6d340e729`.
`git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale show --stat a62dd4837b8e2e3e50d04f512700c6a6d340e729`:
```
commit a62dd4837b8e2e3e50d04f512700c6a6d340e729
Author: ctl <ctl@local>
Date:   Fri Oct 23 00:38:49 2026 -0300

    control variant: rewrite source opened dates

 corpus/SOURCES.md | 10 +++++-----
 1 file changed, 5 insertions(+), 5 deletions(-)
```

## Frozen counter hashes

`timeout 30 sha256sum /fast/scratch/hyaku/mado-r24/ctl/c1-v1.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py`
```
2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291  /fast/scratch/hyaku/mado-r24/ctl/c1-v1.py
b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py
```

## Base control scores

v1 command: `timeout 900 env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale python3 -I /fast/scratch/hyaku/mado-r24/ctl/c1-v1.py f5fddaeb83ca809ca8c18ce49af26acdb0309ba5; rc=$?; printf 'EXIT=%s\n' "$rc"`
```
A1\tS016\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A2\tS017\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A3\tS017\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A4\tS018\tFAIL_ROW\topened!=2026-10-23,no-sha256
A5\tS018\tFAIL_ROW\topened!=2026-10-23,no-sha256
A6\tS019\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A7\tS020\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A8\tS020\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
revision=f5fddaeb83ca809ca8c18ce49af26acdb0309ba5 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
EXIT=1
```

v2 command: `timeout 900 env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py f5fddaeb83ca809ca8c18ce49af26acdb0309ba5; rc=$?; printf 'EXIT=%s\n' "$rc"`
```
A1\tS016\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A2\tS017\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A3\tS017\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A4\tS018\tFAIL_ROW\topened!=2026-10-23,no-sha256
A5\tS018\tFAIL_ROW\topened!=2026-10-23,no-sha256
A6\tS019\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A7\tS020\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
A8\tS020\tFAIL_ROW\topened!=2026-10-23,no-hyprwm-url,no-sha256
counter_version=v2 revision=f5fddaeb83ca809ca8c18ce49af26acdb0309ba5 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
EXIT=1
```

## Opened-date variant scores

v1 command: `timeout 900 env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale python3 -I /fast/scratch/hyaku/mado-r24/ctl/c1-v1.py a62dd4837b8e2e3e50d04f512700c6a6d340e729; rc=$?; printf 'EXIT=%s\n' "$rc"`
```
A1\tS016\tFAIL_ROW\tno-hyprwm-url,no-sha256
A2\tS017\tFAIL_ROW\tno-hyprwm-url,no-sha256
A3\tS017\tFAIL_ROW\tno-hyprwm-url,no-sha256
A4\tS018\tFAIL_ROW\tno-sha256
A5\tS018\tFAIL_ROW\tno-sha256
A6\tS019\tFAIL_ROW\tno-hyprwm-url,no-sha256
A7\tS020\tFAIL_ROW\tno-hyprwm-url,no-sha256
A8\tS020\tFAIL_ROW\tno-hyprwm-url,no-sha256
revision=a62dd4837b8e2e3e50d04f512700c6a6d340e729 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=2fc366ab073db7e45dd6534f98409628a4571f3c3e863a51b1f3f35343fa2291
EXIT=1
```

v2 command: `timeout 900 env MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py a62dd4837b8e2e3e50d04f512700c6a6d340e729; rc=$?; printf 'EXIT=%s\n' "$rc"`
```
A1\tS016\tFAIL_ROW\tno-hyprwm-url,no-sha256
A2\tS017\tFAIL_ROW\tno-hyprwm-url,no-sha256
A3\tS017\tFAIL_ROW\tno-hyprwm-url,no-sha256
A4\tS018\tFAIL_ROW\tno-sha256
A5\tS018\tFAIL_ROW\tno-sha256
A6\tS019\tFAIL_ROW\tno-hyprwm-url,no-sha256
A7\tS020\tFAIL_ROW\tno-hyprwm-url,no-sha256
A8\tS020\tFAIL_ROW\tno-hyprwm-url,no-sha256
counter_version=v2 revision=a62dd4837b8e2e3e50d04f512700c6a6d340e729 mode=refetch note_present=True rows=8 PASS_ROW=0 distinct_sources=0 readme_indexed=True verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
EXIT=1
```

Patch command: `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mado-r24/ctl/CtlC1Stale format-patch -1 --stdout f5fddaeb83ca809ca8c18ce49af26acdb0309ba5 > /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/controls/CtlC1Stale.patch`.

`CONTROL_MEETS_TARGET: no`

The opened-date mutation also fails: the eligible-looking S018 rows have no recorded SHA-256, while S016/S017/S019/S020 lack the counter's required Hyprwm URL and recorded SHA-256. The counter reports zero passing rows for both commits, under both counter versions.