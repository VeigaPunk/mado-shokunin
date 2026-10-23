# Attack — S149 span (routed r23 defect 5)

Scope: re-open the foot wiki blob at the pinned commit and decide the line span of the quote. No product
file edited; the only lane write is this report.

## Commands run

1. `mkdir -p /fast/scratch/hyaku/mado-r24/w2 && git clone https://codeberg.org/dnkl/foot.wiki.git footwiki`
   (GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE unset; `timeout 300`) → exit 0.
2. `git -C footwiki cat-file -t 2475351ace3c8a618a3f2b8a7a486e987d125e07` → `commit`.
3. `git -C footwiki show 2475351ace3c8a618a3f2b8a7a486e987d125e07:Home.md | sha256sum` →
   `78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7`, `wc -c` → `32739`.
4. Identity cross-checks: clone `git rev-parse HEAD` → `2475351ace3c8a618a3f2b8a7a486e987d125e07`;
   `git hash-object Home.md` → `4b8fa7915082580393d00b37434d2f5aad8d5606` = `git rev-parse <commit>:Home.md`;
   `git status --porcelain` → empty; worktree `sha256sum Home.md` → `78bd64dc…` (same bytes as the blob read).
5. Numbered lines from the extracted blob (`git show … > /tmp/hyaku-foot-home-2475351.md`).

## Bytes

```
1011: ### How do I reload the configuration?
1012:
1013: Restart foot. If you are running foot in server mode, you **must**
1014: restart the server. There is no way to dynamically reload the
1015: configuration.
1016:
1017: For theme switching, there is builtin support (since 1.23.0) for
1018: switching between **two** themes (e.g. dark/light). See the `[colors]`
1019: and `[colors2]` sections in `foot.ini`, and the
1020: `color-theme-switch-{1,2}` and `color-theme-toggle` keybindings.
```

Sentence `There is no way to dynamically reload the configuration.`:
- raw (space-separated) substring: **absent** — the blob wraps it at `reload the` + newline + `configuration.`.
- whitespace-collapsed: **1 occurrence**, start **:1014 col 21** (after `restart the server. `),
  end **:1015 col 14**. 9 words.

## Verdict

`:1014-1015` is correct; `:1013-1014` is wrong.

VERDICT: holds (wave-1 scribe's `:1014-1015`); fails (closure's `:1013-1014`)

Blob identity holds exactly (`sha256:78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7`,
32,739 B, pinned blob object `4b8fa791…`), so the span is decided from the same bytes the row names.

## Secondary observations (not the assigned question)

1. Wave-1 scribe report transcription: `.ufo/waves/round-24/w1/reports/ScribeS149Anchor.md:9` quotes line 1013 as
   `Restart foot. If you are running in server mode, you **must**`; the blob reads `If you are running foot in
   server mode` (word `foot` omitted). Its span conclusion `:1014-1015` is still correct.
2. Correction not yet recorded: at HEAD `87429be`, `corpus/lessons/round-24.md:78` says
   `see ## Wave-2 dispositions`, but no `## Wave-2 dispositions` heading exists in that file (headings: `## Mistakes`,
   `## Gate`, `### New SOURCES rows`, `### Opened but not registered`, `## Routed defects … §7`). The defect-5
   correction text exists only in the wave-1 scribe report; the lesson pointer dangles at the current tip.
3. Anchor-to-interpretation gap in S149: the row's locator `Home.md:1011-1015` covers the reload answer but not
   `[colors]` / `[colors2]` at `:1018-1019`, although the row's own interpretation cell says the wiki names
   `[colors]`/`[colors2]`. The FAQ entry itself runs :1011-1020 (next heading :1022). The scribe's correction
   draft addresses only the quote span, so this gap would remain.
4. r23 spotcheck counts the quote as 10 words (`round-23-verifier-spotcheck.md:108`); it is 9. Immaterial to the
   ≤25-word rule.

## Limits

- Pinned raw wiki routes were not re-tried; the git blob from the pinned commit is the row's stated basis.
- No tool installed or updated; no package or service action; no host configuration touched.
- Scratch clone only: `/fast/scratch/hyaku/mado-r24/w2/footwiki`.
