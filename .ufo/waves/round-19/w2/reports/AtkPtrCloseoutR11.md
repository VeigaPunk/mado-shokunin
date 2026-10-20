# MadoR19.AtkPtrCloseoutR11 — partial

Target: the round-19 appended block, `corpus/knowledge/closeout-r11.md:296-304` (heading
`:297`) at tip `01b80946d92b26370d3012a7da655d00dd135154`, baseline
`9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`. Worktree bytes equal the tip blob
(sha256 `dab87af80f32055b97ef3674d770cc5489bdf0b89da1e76bdd7b78554ed917ba`;
`git status --porcelain` empty for the path). Host reads are file bytes / `stat`
only: no gate, no package query, no process probe, no socket connect.

Verdict by sub-question: **(a) holds**; **(b) holds on the 2.17.2 runtime question but
carries one false provenance negative (`:301`)**; **(c) holds, one plural/count
wording defect**; **(d) S090 supports the sentence it carries, but the citation is
unjoined in `S090.used-by` and is a round-18 row, not the round-19 host-bytes row**.

---

## (a) Pre-existing bytes beyond the documented head `source:` swap — HOLD

`closeout-r11.md` has no in-place head edit at all (its `source:` line, `:3`, carries
no `S###` token), so the walker-route-r18/theme-route-r18 swap cannot apply to it.
The baseline blob is a byte-exact prefix of the tip; the only delta is the append.

```text
$ git diff --numstat 9c54c56 01b8094 -- corpus/knowledge/closeout-r11.md
10	1	corpus/knowledge/closeout-r11.md
$ git diff … | grep -c '^@@'          -> 1
$ git show 9c54c56:… | wc -l -c       -> 294 19250     (last byte '.', no LF)
$ git show 01b8094:… | wc -l -c       -> 303 20516
$ sha256sum base tip
670b5a396ecb8789430709a8e490c93a5672399401e6a8209f26e93645d818a1  base
dab87af80f32055b97ef3674d770cc5489bdf0b89da1e76bdd7b78554ed917ba  tip
$ head -c 19250 tip | sha256sum
670b5a396ecb8789430709a8e490c93a5672399401e6a8209f26e93645d818a1  -
$ cmp -n 19250 base tip && echo PREFIX_IDENTICAL   -> PREFIX_IDENTICAL
```

The appended 1,266 B begin `\n\n## Freshness pointer (round 19, 2026-10-20)\n\n` and
end without a trailing LF. The `-1/+1` in the git diff is only the pre-existing last
line gaining its terminator as the first appended byte; no pre-existing byte value
changed (first divergence offset = 19,250 = end of base, `cmp` reports EOF on base).

Cross-check over every changed `corpus/knowledge/*.md` (same prefix test):

```text
APPEND  closeout-r11.md             base=19250 tip=20516 prefix=True
APPEND  arc-synthesis.md            base=30796 tip=32331 prefix=True
APPEND  config-health-report-r3.md  base=62249 tip=63705 prefix=True
APPEND  remaining-planes-census.md  base=20512 tip=22211 prefix=True
APPEND  walker-deep-r9.md           base=24391 tip=25976 prefix=True
APPEND  walker-deep.md              base=38403 tip=40352 prefix=True
APPEND  walker-live-surface.md      base=19203 tip=20413 prefix=True
APPEND  waybar-walker-plane.md      base=28392 tip=29796 prefix=True
APPEND  waybar-walker-semantics.md  base=38083 tip=39539 prefix=True
PREFIX  walker-route-r18.md         base=24830 tip=25722 firstdiff=1391  (head line 1)
PREFIX  theme-route-r18.md          base=19121 tip=19867 firstdiff=412   (head line 1)
```

Only the two documented route heads rewrite pre-existing bytes. `closeout-r11.md` is
a pure append. (PROVINCE.md/SKILL.md/tools/mado-verify.sh have their own documented
non-pointer edits and are outside this note.)

## (b) Live/runtime facts about 2.17.2, or un-rehashed re-verification — ONE FALSE NEGATIVE

No sentence claims a live/runtime fact about 2.17.2; the block explicitly bounds both
runtime sentences:

- `closeout-r11.md:302` — "the 2.17.2 binary's live reload behaviour is [UNK]".
- `closeout-r11.md:304` — "behaviour of the 2.17.2 binary stays [UNK]".
- `:299` "the host package moved to 2.17.2" is a package-manager fact, not runtime.

But `:301` says the socket observation is "**not re-measured this round**". That is
false: the round's own wave-1 delta seat re-statted exactly these sockets, and the
stat reproduces now (file bytes/stat only):

```text
$ sed -n '136,139p' .ufo/waves/round-19/w1/reports/DeltaWalkerCli.md   # committed at tip
Live socket state today (stat only): both sockets `755 0`, mtime
`2026-10-20 09:57:13.737056297 -0300` (walker) / `.715056299` (elephant) — later
than both post-upgrade restart-hook lines (`pacman.log:3062` 09:18:25, `:3123`
09:31:04); the cause of the 09:57 bind is `[UNK]`.

$ stat -c '%a %s %y %n' /run/user/1000/walker/walker.sock /run/user/1000/elephant/elephant.sock
755 0 2026-10-20 09:57:13.737056297 -0300 /run/user/1000/walker/walker.sock
755 0 2026-10-20 09:57:13.715056299 -0300 /run/user/1000/elephant/elephant.sock
```

The round-11 observation quoted in the block is the walker-row "sockets `stat`'d 0 B,
never connected" (`closeout-r11.md:43`). Its stat half was re-measured this round
(stat only; mode/size unchanged, mtime moved); the connect half was not repeated.
The pointer's correct wording is "re-statted this round (stat only; shape unchanged,
mtime moved); connect not repeated", not "not re-measured this round". This is the
same class of defect the sibling attack on `arc-synthesis.md` scored as a break
(`.ufo/waves/round-19/w2/reports/AtkPtrArcSynthesis.md`, (b): the listed sockets were
re-measured by `DeltaWalkerCli.md:136`).

No sentence calls anything "re-verified" without a hash; the route-grep sentence
(`:302`) describes the round-18 note's source reading (`walker-route-r18.md:96`), not
a round-19 re-run, and the v2.17.2 tag is immutable.

Delta check used for the version-binding: `DeltaWalkerConfig.md:160-164` re-ran the
reload token census on both released binaries (`inotify` 0/0, `(?i)watch` 0/0,
`restart` 0/0, `load_config`/`reload_config`/`set_config`/`file_watch` 0/0) and says
"No hot-reload, restart is the apply path" is not disturbed by the delta;
`DeltaWalkerCli.md:115-116` finds no `--config` and no reload verb. The block's
decision to bind the old "no reload path" reading to 2.17.0 and leave 2.17.2 live
behaviour `[UNK]` is therefore conservative, not an overclaim.

## (c) Cited line numbers — HOLD (one wording defect)

Every number is correct on the tip bytes and is before the append, so none shifted:

| cited | tip line content |
|---|---|
| `line 12` | `verified-at: 2026-10-14 21:23–21:35Z …` |
| `line 43` | `| walker | 2.17.0; sockets …; no reload path … | consumer-side probe |` |
| `line 174` | `walker ×3 — a seam decision …` |
| `lines 152, 154, 187, 201` | all four contain `walker-deep` (errata rows; F3 `walker-deep-r9.md:296`) |
| `line 264` | `… walker 1203471, elephant 1203474, swaybg 1203358 alive` |

Wording defect: `:299` says "The walker version **pins** … (**lines 43**)" although
the note has exactly one `2.17.0` line and one pin:
`grep -c '2\.17\.0'` on the baseline = 1 (only line 43). No wrong number, but "line
43" / one pin is the accurate form.

## (d) S### support — HOLD for content; join gap

Only `S090` is cited (`:299`). `corpus/SOURCES.md:102` is the row: status `mined`,
anchor "lines 1943 …, 2929 (walker 2.17.0-1 -> 2.17.2-1, 2026-10-20T09:16:46-0300),
3062 and 3123 (walker-restart.hook) …", teaches "host package versions match tags
v2.17.2 and v2.22.1", and adds "a log line is not a running-binary fact". The block
mirrors that scope: it says the package moved, not that the binary runs.

Independent check of the cited line and the package state (file bytes):

```text
$ sed -n '2929p;3062p;3123p' /var/log/pacman.log
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
[2026-10-20T09:18:25-0300] [ALPM] running 'walker-restart.hook'...
[2026-10-20T09:31:04-0300] [ALPM] running 'walker-restart.hook'...
$ awk 'NR>2929 && /walker/' /var/log/pacman.log   # only the two hook lines; no later transaction
$ sed -n '1,6p' /var/lib/pacman/local/walker-2.17.2-1/desc
%NAME%
walker
%VERSION%
2.17.2-1
```

Two registry caveats, neither making the sentence false:

1. **Unjoined `used-by`.** `CORPUS.md:107` defines `used-by` as "repo-relative paths
   of the knowledge entries or lessons citing the row". `SOURCES.md:102` still lists
   only `corpus/knowledge/walker-route-r18.md`; `closeout-r11.md:299` is now a citing
   entry and is absent. Same class as the five S090-only pointers in
   `CriticC2W2.md:72` / `CriticAdmission.md` Finding 2; `SOURCES.md` is L1-owned, so
   this is an integration follow-up, not a lane write owed by the pointer seat.
2. **Round-18 row, not the C2 host-bytes row.** `S090` is already present at
   `9c54c56:102`; `S096` (host walker bytes, `/usr/bin/walker` literal at 856,302)
   is absent at baseline (`grep -c '^| S096 '` = 0) and present at tip
   (`SOURCES.md:108`). The block cites only `S090`, so it does not meet the C2
   pre-registration's per-file "SOURCES row opened this round for the host walker
   bytes (+ upstream release)" wording. It is truthful as written (it makes no
   binary-read claim), so this is a C2-claim scope shortfall already carried by
   CriticC2W2 F2, not a false statement in this block.

Secondary nit: `:303` says the other mentions are "none … affected by the host move".
Line 264's PID sample is a live, session-dependent value in the same class as the
socket sample that `:301` marks session-dependent; the 09:57 socket rebind and the
two restart hooks make those PIDs stale as live values. The block labels it "the
2026-10-14 PID sample", so it remains a dated record — no false assertion, but the
asymmetry with `:301` should be stated. [INFERENCE]

## Limits

- Did not re-fetch the walker tag or crate, did not run the gate or any suite, did not
  probe processes, did not connect the sockets. The `DeltaWalkerCli` socket stat is
  corroborated by my own `stat` of both sockets, not accepted on report evidence.
- Did not verify `S096`'s binary literal (out of scope); it is cited only as the
  registry row that exists at tip and is not used by this block.
- Chronology: the w1 pointer and delta seats ran in parallel; the false negative may
  have been true for the pointer lane's own read set, but it is false at the
  integrated tip, which is what the item asks about.
- `git` reads only; no lane writes except this report.

## Installs

none
