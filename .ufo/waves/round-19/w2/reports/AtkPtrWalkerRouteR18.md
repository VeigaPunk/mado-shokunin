# MadoR19.AtkPtrWalkerRouteR18 — breaks

Item: attack the round-19 appended block in `corpus/knowledge/walker-route-r18.md`
(`git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d 01b80946d92b26370d3012a7da655d00dd135154 -- corpus/knowledge/walker-route-r18.md`),
questions (a) undocumented byte change, (b) live/runtime or un-rehashed re-verification
claim, (c) cited line numbers, (d) S### rows supporting their sentences.

Bottom line: **the block's own assertions verify** — only the S084 token changed, no live
fact is claimed, all three cited line ranges are exact in the xdg 3.0.0 crate, and
S084/S098/S096 all exist with supporting content. It **breaks in integration**: the
replacement token carries the superseded id `S084` *inside* the machine-read `source:`
line, so the note still credits a rejected registry row, and the lane's own committed
round-18 join checker goes **PASS (baseline) → FAIL, exit 1** at `df84807` and at the tip.
Two lesser defects: the unchanged head `verified-at` receipt sentence is false for S098,
and the appended S096 citation is unjoined (row `used-by` omits this note; row absent
from the head inventory).

## (a) Byte audit — holds

Diff is two hunks and nothing else:

```text
@@ -1,4 +1,4 @@
-source: S072 … S084 https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html (find_config_file, find_config_files, XDG defaults) …
+source: S072 … S098 https://static.crates.io/crates/xdg/xdg-3.0.0.crate (src/base_directories.rs:446-457 find_config_file, :308-310/:321-323 XDG defaults; supersedes S084, round 19) …
@@ -321,3 +321,8 @@
+## Round-19 corrections (append-only, 2026-10-20)
+(2 bullets, lines 325-328)
```

Byte-exact test outside the token (`python3`, raw bytes of head line 1):

```text
OLD TOK: b'S084 https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html (find_config_file, find_config_files, XDG defaults)'
NEW TOK: b'S098 https://static.crates.io/crates/xdg/xdg-3.0.0.crate (src/base_directories.rs:446-457 find_config_file, :308-310/:321-323 XDG defaults; supersedes S084, round 19)'
prefix equal: True   (1389 B both sides)
suffix equal: True   (781 B both sides)
newlines in line 1: 1 / 1 ; semicolons: 21 -> 22
```

Sweep of every changed `corpus/knowledge/*.md` head line between the same two commits
(`git diff --name-only … -- corpus/knowledge/`, compare first `source:` line old vs new):
only `corpus/knowledge/walker-route-r18.md` and `corpus/knowledge/theme-route-r18.md`
changed, matching the documented scope. The theme sibling is the same shape (S094 →
S097 token; prefix/suffix equal, no other byte moved). No pre-existing body byte changed.
**Answer (a): no undocumented change.**

## (b) Live/runtime or un-rehashed claim — no live claim; one stale provenance sentence

The appended block claims no live fact, and says so:

- `corpus/knowledge/walker-route-r18.md:328`: "2.17.2 literal at offset 856,302;
  `--version` output and runtime behaviour of 2.17.2 are not observed (host pause) and
  stay [UNK]." File bytes only — correct posture.

Independently re-read as file bytes (allowed under the pause; python `open`, `sha256sum`,
`stat`; nothing executed):

```text
size 7039912 sha256 25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
2.17.2 count 1 first 856302 ; bytes[856302:856309] = b'2.17.2\n' ; 2.17.0 count 0
$ stat -c '%s %y' /usr/bin/walker -> 7039912 2026-10-08 11:14:32.000000000 -0300
```

That is exactly what `S096` (`corpus/SOURCES.md:108`) and the bullet claim.

Re-hash scope for the other source: the crate was re-fetched/re-hashed **this round** —
`.ufo/waves/round-19/fetch/{SrcS084,DeltaWalkerCli,FrontierRows,RevRubricVRisk}/xdg-3.0.0.crate`
all hash to `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`, and
`.ufo/waves/round-19/fetch/SrcS084/receipts.jsonl` records the crate at
`2026-10-20T17:06:24Z`, 15,821 B, and `walker-v2.17.2-Cargo.lock` at `17:06:13Z`; lock
line 2708 is `checksum = "2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5"`
(single `name = "xdg"` entry, version 3.0.0 at :2706). The "equals Cargo.lock:2708"
sentence is true.

**Stale sentence the swap falsifies** — head line 2, unchanged:

> `verified-at: 2026-10-20; … every raw body curl-fetched with a receipt in .ufo/waves/round-18/fetch/NoteWalker/receipts.jsonl; …`

`NoteWalker/receipts.jsonl` has 27 lines; its URLs are the walker/elephant raw bodies,
codeload, the two GitHub tree APIs and `docs.rs/xdg/latest/...`. There is **no
`static.crates.io` receipt**. The lane's own join checker prints the seats that hold an
S098 receipt: `JOIN S098 web receipts=2 … seats=MadoR18.RevengeTarballRepro,SrcWalkerConfigPaths`
— not NoteWalker. So a reader following the head's stated receipt trail cannot verify the
token the correction installed. [INFERENCE] severity: provenance/documentation, not a
false technical fact; the bytes are re-hashed elsewhere in the lane.

## (c) Cited line numbers — holds exactly

Extracted the committed crate (`tar xzf` into `/tmp`, sha verified above) and read
`xdg-3.0.0/src/base_directories.rs`:

```text
446 /// Given a relative path `path`, returns an absolute path to an existing
447 /// configuration file, or `None`. Searches `XDG_CONFIG_HOME` and then
448 /// `XDG_CONFIG_DIRS`.
308 let config_home = env_var("XDG_CONFIG_HOME")
309     .and_then(abspath)
310     .or_else(|| home.as_ref().map(|home| home.join(".config")));
321 let config_dirs = env_var("XDG_CONFIG_DIRS")
322     .and_then(abspaths)
323     .unwrap_or(vec![PathBuf::from("/etc/xdg")]);
```

So `find_config_file` doc `:446-448`, defaults `:308-310` and `:321-323` are all exact,
and the head token's `:446-457` is the correct doc+signature+body span for
`find_config_file`. The body's `XD:n` anchor lines were checked against the committed
105,537 B saved HTML the note names (`NoteWalker/xdg-crate-basedirectories.html`, sha256
`0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d` = S084's anchor):
`:302` is `XDG_CONFIG_HOME … $HOME/.config`, `:306` is `XDG_CONFIG_DIRS … /etc/xdg`,
`:356-358` is the `find_config_file` section header plus "Searches `XDG_CONFIG_HOME` and
then `XDG_CONFIG_DIRS`". The remap is fact-correct.

Two precision nits, neither a false sentence:
- "read as the same **text**" is loose for the defaults: `XD:302/:306` are docs prose,
  `:308-310/:321-323` are the implementing code.
- The old token advertised `find_config_file, find_config_files`; the new one cites only
  `446-457`. `find_config_files`' doc is `:459-462`. No note claim relies on XD for it
  (`corpus/knowledge/walker-route-r18.md:119` cites `WT:56`), so coverage shrank silently
  but nothing became false.

## (d) S### rows — all three rows support, one join is one-sided

- `S084` (`corpus/SOURCES.md:96`): URL is the `docs.rs/xdg/latest/...` alias, status
  `rejected`, used-by `—`. Supports "an unpinned HTML page — R18-V4 … now rejected".
- `S098` (`corpus/SOURCES.md:110`): status `mined`, tier A, used-by
  `corpus/knowledge/walker-route-r18.md`, anchor carries the full crate sha and the lock
  checksum. Supports the head token and bullet 1.
- `S096` (`corpus/SOURCES.md:108`): status `mined`; content supports bullet 2 (literal
  `2.17.2\n` at 856,302). **But** its used-by cell is
  `corpus/knowledge/walker-deep.md, corpus/knowledge/walker-deep-r9.md,
  corpus/knowledge/walker-live-surface.md, corpus/knowledge/remaining-planes-census.md,
  tools/mado-verify.sh, SKILL.md` — this note is not listed, and S096 is absent from the
  head `source:` inventory (head tokens are S072-S083, S098, S085-S091). The citation at
  `walker-route-r18.md:328` is therefore unjoined in both directions.

## The break: the head line still credits the rejected row

The in-place token embeds `supersedes S084, round 19` **on the `source:` line**. The
committed round-18 falsifier parses every `S\d{3,}` on `source:` lines and requires
`status == 'mined'` plus a matching `used-by`
(`.ufo/waves/round-18/token-join-check.py:63` `SOURCE_TOKEN = re.compile(r'S\d{3,}')`,
`:270-276` the status gate). Re-run independently:

```text
$ python3 -I .ufo/waves/round-18/token-join-check.py 01b80946d92b26370d3012a7da655d00dd135154
NOTE corpus/knowledge/walker-route-r18.md source_lines=1 tokens=21 unique=21 web=18 host=2 gaps=1
NOTE corpus/knowledge/theme-route-r18.md source_lines=1 tokens=5 unique=5 web=3 host=1 gaps=1
GAP  corpus/knowledge/walker-route-r18.md:1 S084 not-mined detail=status='rejected'
GAP  corpus/knowledge/theme-route-r18.md:1 S094 not-mined detail=status='rejected'
SUMMARY rev=01b80946… notes=2 tokens=26 unique=26 web=21 host=3 gaps=2
RESULT FAIL          (exit 1; no stderr)

$ python3 -I .ufo/waves/round-18/token-join-check.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
NOTE corpus/knowledge/walker-route-r18.md … tokens=20 unique=20 … gaps=0
NOTE corpus/knowledge/theme-route-r18.md … tokens=4 unique=4 … gaps=0
SUMMARY rev=9c54c56a… notes=2 tokens=24 unique=24 web=21 host=3 gaps=0
RESULT PASS          (exit 0)
```

Same FAIL, exit 1, at the wave-1 integration commit `df84807d8fc49f5d8fb4ec3060859e5b1992084c`
— i.e. the regression landed with the supersession, not later. The token counts show the
mechanism: the source line gained one S-token (20 → 21; theme 4 → 5) and that token is the
rejected row. The appended sentence "was replaced in place by S098 … S084 is now
`rejected`" is therefore true of the bytes it names but not of the file as the lane reads
it: the note's credited-source line still names S084, while the registry now records
S084's used-by as `—` (`corpus/lessons/round-19.md`, M2 "used-by … → —").

Structural side effect of the same edit: the new parenthetical contains a `;`, so a naive
`; `-split of the head (the convention every other token follows) yields a URL-less
segment `supersedes S084, round 19)` in addition to the 21 S-ids.

Scope of impact: neither `tools/` nor `.ufo/waves/round-19/` references
`token-join-check` (grep), so the round-19 443-selftest and the gate do not see this; the
checker is nevertheless committed at the tip (`git cat-file -e 01b80946:.ufo/waves/round-18/token-join-check.py`
→ present) and its PASS was a published round-18 result. Minimal repair for the owner:
drop the id from the head parenthetical (e.g. "supersedes the docs.rs alias row, round 19")
and let line 327 carry the S084 explanation, or keep the id and accept the checker's FAIL.
An added `S096` used-by entry would close the second gap.

## Limits

- No network fetch was performed for this attack; every digest above is a re-hash of a
  committed/cached body plus its committed receipt. [UNK] whether `docs.rs/xdg/latest`
  now resolves to a release newer than 3.0.0 (irrelevant to (c): the mapping is anchored
  to the committed 105,537 B capture).
- `token-join-check.py` is a round-18 artifact; no lane document I found states whether
  round 19 retires it or intends it to stay green. The observed regression is real either
  way; its weight depends on that unwritten decision.
- I did not run the gate, open walker/elephant, or touch any service; host reads were
  `open()/stat/sha256sum` only.
- The `:270-276` and `:63` checker line numbers are the current committed copy; the
  behavior above is from execution, not from reading.

## Installs

none
