# RevRowsUnchanged — report, mado round-36 wave 1

Seat: `L1Mado36.RevRowsUnchanged` (reviewer)
Scope: verify that no `corpus/SOURCES.md` row has been edited in place since the round-35 tip
(`7a068cb`) through `master`.
Verdict: **PASS** — no change; file is byte-identical across the range.

## Revisions resolved

```
7a068cbee3b0983230b8fb8467c02e12772832dd   (round-35 tip)
dbf8b579aeac0f023aaf595770f1cb0049e4baa2   (master)
```

`git log -1 --format='%h %s %ci'`:

- `7a068cb round-35: close 2026-10-25 03:53:37 -0300`
- `dbf8b57 round-36: freeze both predicates, the control manifest, the cribs and the before receipts 2026-10-25 04:24:12 -0300`

## Commands and output

### 1. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --numstat 7a068cb master -- corpus/SOURCES.md`

Output: **(empty)** — exit 0, zero lines. Expected-empty check holds: no additions/deletions
recorded against the path.

### 2. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --oneline 7a068cb..master -- corpus/SOURCES.md`

Output: **(empty)** — exit 0, zero commits. No commit in the range touched
`corpus/SOURCES.md`, so no row could have been edited, added, or removed in place.

### 3. Row counts at both revisions

`git show <rev>:corpus/SOURCES.md | wc -l` and `grep -c '^|'`:

| revision | total lines | table rows (`^|`) |
|---|---|---|
| `7a068cb` | 450 | 202 |
| `master`  | 450 | 202 |

Row shape: header line 11 (`| id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by |`), separator line 12, so **200 source data rows** at both
revisions (`grep -c '^| *S[0-9]'` = 200).

### 4. Content hash

`git show <rev>:corpus/SOURCES.md | sha256sum`:

```
7a068cb:  0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51
master:   0bf117e2f472ec4f80adec17d58fe50b4fbd4fa9568ffa8523a4bfc272950d51
```

Byte-identical — stronger than row-level equality; not even whitespace changed.

## Finding detail

- Rows changed in place: **none** (no commits touch the path; numstat empty; sha256 equal).
- If a row had changed, none exists to name.

## Residual risk / gaps

- Check covers committed history only (`7a068cb..master`). Any uncommitted working-tree
  edit is outside this gate's range; not observed and not part of the assignment.
- "Row" interpreted both as table rows and whole-file content; both unchanged, so the
  verdict is robust to either reading.

## Tool installs

None. `git`, `wc`, `grep`, `sha256sum` already present; no pacman transaction run
(host-wide pause honored).
