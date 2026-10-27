# ExecFetchR50 — C1 rows: re-fetch of every round-49 pin and byte stability (round 50, w1)

Seat: `ExecFetchR50`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `8ae47b957034ae21012bbf09173cca2c48be345e`.
Read first: `.ufo/waves/round-50/claims.md`, `.ufo/waves/round-49/candidate/rows.md` (S352–S363), `corpus/lessons/round-49-verifier-spotcheck.md` §6.
Access date for every source below: **2026-10-27** (fetches between 05:56:22Z and 05:57:xxZ).

## Verdict

**14/14 fetched pins are byte-identical to their round-49 pin; 0 differing; 1 own-work pin re-measured identical.
No finding.** The C1 pin set the round-50 port will cite is byte-stable on this round's access date, at the same commits.

Axes (godspeed): the move is **freshness** (every held pin re-opened this round, all equal) with **calibration** support (the
check is a re-runnable script and a manifest with status/bytes/lines/sha256 on both sides). Coverage is unchanged — this seat adds
no row; operability is unchanged — no tool is built here. Nothing is harmed: no tracked file was edited, no host state written.

## Manifest summary (`fetch-manifest.tsv`, 14 rows, one per fetched pin)

| # | pin (basename, same as round-49) | row | http | bytes | lines | sha256 (this round = round-49) | equal |
|---|---|---|---|---|---|---|---|
| 1 | Hyprland-KeybindManager.cpp | S352 | 200 | 39334 | 975 | `8d8f35fc84c4…d9342d4e40` | yes |
| 2 | Hyprland-legacy-ConfigManager.cpp | S353 | 200 | 90963 | 2184 | `9db68cf44048…65f65be62b` | yes |
| 3 | Hyprland-InputManager.cpp | S354 | 200 | 98845 | 2315 | `feedf32e2e3d…e9ece4765` | yes |
| 4 | xkbcommon-keysym.c | S355 | 200 | 14948 | 450 | `123e3390d443…99c3369c5` | yes |
| 5 | xkbcommon-keysym.h | S355 | 200 | 4949 | 124 | `1398b750580f…78431949` | yes |
| 6 | xkbcommon-ks_tables.h | S356 | 200 | 324906 | 8314 | `6960e7e4aa49…ff8246781` | yes |
| 7 | xkbcommon-tools-how-to-type.c | S357 | 200 | 30238 | 836 | `f774882e88f0…41c8515bc` | yes |
| 8 | xkbcommon-xkbcommon-keysyms.h | S358 | 200 | 264502 | 3545 | `13023369f65a…490a463f3` | yes |
| 9 | wiki-Binds.md | S359 | 200 | 19526 | 600 | `3d8a2a6832da…4b17d628` | yes |
| 10 | wiki-Variables.md | S360 | 200 | 51064 | 684 | `3b3bb219f57d…dfcbf5905` | yes |
| 11 | xkbcommon-state.c | S362 | 200 | 67069 | 1955 | `8cc57f53d41b…bc6955262` | yes |
| 12 | Hyprland-IKeyboard.hpp | S363 | 200 | 4816 | 137 | `82e0bc9e1f31…f0f716f05` | yes |
| 13 | Hyprland-IKeyboard.cpp | S318 (held, `corpus/SOURCES.md:267`) | 200 | 15941 | 460 | `8a800efe9baa…a1102a1aa3d` | yes |
| 14 | Hyprland-ConfigValues.cpp | S319 (held, `corpus/SOURCES.md:268`) | 200 | 59222 | 734 | `a76f05079454…4ad97754` | yes |
| — | binds-live-r49.txt | S361 | own-work | 1302 | 16 | `290f6e49c119…af0e72eeb` | own-work, re-measured |

Full 64-hex digests, URLs, HTTP status and ISO access times: `ExecFetchR50/fetch-manifest.tsv`.
Rows 13 and 14 are in `.ufo/waves/round-49/fetch/` but are not rows of `candidate/rows.md`: they are the held rows S318/S319, which
the round-49 entry cites without re-registering; they were in the assigned pin set, so they were re-fetched too.

Equal/differ count: **equal 14, differ 0** (`cmp_equal=14 differ=0 ownwork=1`, `ExecFetchR50/cmp-verify.txt`; every `cmp_rc=0`).
A differing pin would have been a finding with a diff stat; there is none.

## Commands and receipts

| evidence file | what it is |
|---|---|
| `ExecFetchR50/fetch-all.sh` | the re-fetch driver: 14 URLs (commit/tag URLs only, `raw.githubusercontent.com`), one `curl -sS --max-time 180 -o … -w '%{http_code}'` per pin, refuses a work dir under `/tmp`, `/var/tmp`, `/dev/shm`, `ulimit -f 65536`, writes the manifest. Run as `WORKDIR=<scratch> LANE=<lane> ./fetch-all.sh`; final line `manifest_rows=14 failures=0`, exit 0. |
| `ExecFetchR50/fetch-manifest.tsv` | basename, url, http_status, bytes, lines, sha256, round-49 pin sha256, equal, accessed_utc — 14 rows, `equal` column all `yes`. |
| `ExecFetchR50/cmp-verify.txt` | `cmp -s` of each round-49 pin against this round's copy (rc + 16-hex prefix of both sides); `cmp_rc=0` for all 14. |
| `ExecFetchR50/commit-identity.txt` | tag→commit resolution, wiki tag count, GitHub API commit identity for all three commits. |
| `ExecFetchR50/commit-crosscheck.tsv` + `ExecFetchR50/crosscheck-commit/` | the 6 libxkbcommon files re-fetched at the **commit** URL `d1442aaa…` (not the tag), compared to the round-49 pins: 200, equal yes, all 6. |
| `ExecFetchR50/rows-digest-binding.txt` | machine check: the 13 distinct `sha256:` tokens in `candidate/rows.md` all equal a round-49 pin, none unmatched; every pin is covered by the manifest; the 12 size/line claims the rows make agree with the pinned bytes (`mismatches: []`). |
| `ExecFetchR50/live-ownwork-r50.txt` | the S361 own-work re-measure (shape only, no raw JSON). |

## Commit and tag identity

```
$ git ls-remote https://github.com/xkbcommon/libxkbcommon refs/tags/xkbcommon-1.13.2 'refs/tags/xkbcommon-1.13.2^{}'
322bf223710e9d3a646dd345896eb4e7a83f8c41	refs/tags/xkbcommon-1.13.2
d1442aaa6b635551182e83c3b55037f4c118c962	refs/tags/xkbcommon-1.13.2^{}
$ git ls-remote https://github.com/hyprwm/hyprland-wiki 'refs/tags/*' | wc -l
0
$ curl -sS https://api.github.com/repos/<repo>/commits/<sha>   # sha + committer date
xkbcommon/libxkbcommon d1442aaa6b635551182e83c3b55037f4c118c962 2026-05-30T08:34:04Z | Bump version to 1.13.2
hyprwm/Hyprland       efb50993780079460b0cbed1363e2166a2de1d9f 2026-08-05T14:13:21Z | [gha] Nix: update inputs
hyprwm/hyprland-wiki  d5f07c60e16fe03744aabb76e492117b7f7c4679 2026-08-05T13:16:48Z | Documentation for system bell Lua event and sound customization variab…
```

The three commits the rows name exist and are the commit the URLs address. The libxkbcommon tag `xkbcommon-1.13.2` resolves to
`d1442aaa…` — exactly the commit rows S355–S358 and S362 declare — and the six files fetched at that commit URL are byte-identical to
the tag fetch **and** to the round-49 pins (`commit-crosscheck.tsv`, all `equal yes`). The wiki has no tags, which is why rows S359/S360
correctly pin a commit.

## Row↔pin digest binding (relevant to the round-49 C2 counter clauses b/c/d/e/j)

Every one of the 14 pins has a digest recorded in a row, and that digest equals the pin bytes:

- 12 pins are bound by `candidate/rows.md` S352–S363 (13 distinct `sha256:` tokens: S355 binds both keysym files).
- 2 pins are bound by the held rows `corpus/SOURCES.md:267` (S318, `sha256:a76f0507…`) and `:268` (S319, `sha256:8a800efe…`).

The rows' own metadata also agrees with the pinned bytes for every file they size-name: 12 files, 12 byte-count claims, 0 mismatches,
and the line counts in the rows (975, 2184, 2315, 450, 8314, 836, 3545, 600, 684, 1955, 137) equal `wc -l` of both this round's copy and
the round-49 pin. Because the bytes are identical, every row locator (`File.cpp:LINE`) resolves to the same text this round as last round.

## Own-work pin S361 (`binds-live-r49.txt`) — not fetched, re-measured

The round-49 pin is the seat's own capture; it is not a URL. Copy and provenance still agree: `.ufo/waves/round-49/fetch/binds-live-r49.txt`
and `.ufo/waves/round-49/receipts/binds-live-r49.txt` are `cmp`-identical, both `290f6e49c119a680c3e87f92eeb667cf6f6dd86c24f46b4f8064089af0e72eeb`.
Re-measured this round with the allowed read-only reads (shape only; no raw JSON stored, no device name, title, dispatcher arg or home path):

```
hyprctl version -> Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean
hyprctl binds -j | sha256 of raw bytes -> 9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779  (90401 bytes)
   (the digest the round-49 receipt records; byte-identical capture, not merely equal counts)
   binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0
hyprctl getoption input:resolve_binds_by_sym -j -> int=0 set=false
```

So the own-work row's facts (192 binds, the 142/42/6/2/0 split, `resolve_binds_by_sym` false) still hold at this round's access date,
and the raw bind surface is byte-identical to the round-49 capture.

## Findings and observations

- **Finding: none.** No pin differs; there is no diff stat to report. Nothing upstream moved between round 49 and round 50 at these commits.
- **Observation O1 (pin form, not a defect).** 6 of the 14 pins are **tag** URLs (`xkbcommon-1.13.2`): a git tag can be moved, so the URL
  alone is not immutable. Immutability is proven here two ways — the tag resolves to `d1442aaa…`, the commit the rows already name, and
  fetching the same 6 files at that commit URL gives byte-identical files. If the L1 wants PRED-C1-r50 to accept only commit URLs, the row
  swap is mechanical (same bytes, same digests); no byte in the round-49 pin set changes either way.
- **Observation O2 (for the round-50 C1 port's pin clause).** The pin set is exactly the 15 files in `.ufo/waves/round-49/fetch/`, and the
  round-49 candidate `rows.md` cites only files inside it (12 receipt basenames named in the rows, 0 missing). Any file the port needs beyond
  these has no round-49 pin and is therefore not covered by this seat's evidence.
- **Note on siblings:** `git status --porcelain` in the lane shows in-flight modifications under `.ufo/waves/round-49/w1/ExecControlsC1*`;
  they are another seat's work at the same time, not this seat's. This seat wrote only `.ufo/waves/round-50/w1/ExecFetchR50/**` and this report.

## Reproducibility, safety, cleanup

- Second run of `fetch-all.sh` (independent `curl` calls) reproduced `equal=yes` for all 14; the manifest was rewritten with the new access
  times and the copies stayed byte-identical. Both runs returned HTTP 200 for every URL.
- Scratch `/fast/scratch/hyaku/mado-r50/ExecFetchR50/` used as `WORKDIR` (never an inherited `TMPDIR`; `ulimit -f 65536`); removed at the end.
  No file was written under `/tmp`, no `~/.cache`, `~/.config`, `~/.local` or other home state was touched; no pacman, no compositor
  mutation, no `hyprctl dispatch/keyword/reload` — only `version`, `binds -j`, `getoption … -j`.
- No tool installed or upgraded this seat (`curl`, `git`, `python3` already present).
- Deliverables verified with `test -f` before this report was finalized: `fetch-manifest.tsv`, `commit-crosscheck.tsv`, `cmp-verify.txt`,
  `commit-identity.txt`, `rows-digest-binding.txt`, `live-ownwork-r50.txt`, `fetch-all.sh`, all 14 `fetch/<basename>`, this report.

## Risks / blockers

None. This seat builds no counter and scores no round-50 predicate; it hands the L1 a byte-stable pin set plus the digest-binding facts
above for the PRED-C1-r50 freeze.
