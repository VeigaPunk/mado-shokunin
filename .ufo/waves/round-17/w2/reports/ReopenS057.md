# Reopen S057 — xdg-terminal-exec v0.14.3 reference script

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`; lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
Row: `corpus/SOURCES.md:69`. Gate line: `corpus/lessons/round-17.md:44` (§ Gate, new-rows table).
Citing note (used-by): `corpus/knowledge/terminal-route-r17.md`.
Installs: **none** (HOST PAUSE honored: no pacman/sudo/systemctl/hyprctl/libinput/evtest/alacritty/xdg-terminal-exec; bytes, curl and read-only git only).

## Verdict

**The attack failed.** URL, raw digest, byte count, every cited anchor, the ≤25-word gate quote, tier/kind/status, and every S057-attributed claim in the citing note verify against freshly fetched bytes. No counterexample to any truth claim. Three precision findings (two locator boundaries, one anchor-attribution imprecision) are recorded below; none changes a claim or the P4 capability.

## Fetch evidence (tag-pinned raw bytes)

| Item | Value |
|---|---|
| URL fetched | `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec` |
| SHA-256 | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` — **identical** to row and gate |
| Bytes / lines | `44020` / `1499` — bytes **identical** to row |
| Tag binding | `git ls-remote … refs/tags/v0.14.3` → `065925df9f419008159258ae169018bfd23df71b`, single line, no `^{}` line ⇒ lightweight tag, matching the note's ref-object claim |
| Cross-check | `README.md` v0.14.3 → `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40`, `14762` bytes — matches the note's comparison table (S056 digest) |
| Census | `scripts/sources-census.sh validate --root … mado` → `mado ok`; its only W04 warnings are S030/S042/S045, unrelated to S057 |

## Row cells (`corpus/SOURCES.md:69`, byte-identical at HEAD and worktree)

| Cell | Row value | Observed at anchor | Holds |
|---|---|---|---|
| source | v0.14.3 reference script, tag-pinned raw URL | raw bytes at that exact URL, digest match | yes |
| kind / tier | `code` / `A` | upstream source code at tag; CORPUS.md:93–97 defines A as "primary or authoritative for that scope … source code" | yes |
| scope | "option and lookup code at tag v0.14.3" | option help 101–110, config lookup 143–163, option parse 1252–1259 | yes |
| anchor 106 (--dir) | `--dir=workdir` documentation | line 106 = `			--dir=workdir      set workdir of terminal.` | yes |
| anchor 148-162 (config sequence) | config file precedence | 148–154: `XDG_CONFIG_HOME`/`XDG_CONFIG_DIRS`, per-desktop-prefixed then plain; 156–163: `XDG_DATA_DIRS` + `xdg-terminal-exec/`, same order | yes (see N1) |
| anchor 402-413 (execarg defaults) | `/execarg_default` handling | 402 `/execarg_default:*:*`; 407–409 split; 413 append to `XTE__EXECARG_DEFAULTS`; consumed by `get_default_execarg` 1113–1130 | yes (see N1) |
| anchor 919 (TerminalArgDir) | entry key read | 919 `'X-TerminalArgDir'*=* \| 'TerminalArgDir'*=*)` → `XTE__DIRARG`, inside `check_entry_key()` (802) | yes |
| anchor 1252 (--dir= parse) | option branch | 1252 `--dir=*)` → `XTE__DIRVAL` | yes |
| digest + size | `89f2…ac`, 44020 bytes | fetched bytes hash and size match exactly | yes |
| teaches | "script agrees with README on lookup order and `--dir` meaning; execution not performed" | README.md:113–123 order == script 148–163 order; README.md:202–208 `--dir` → `X-TerminalArgDir`, else "change dir before executing" == script 1400–1411 (`set -- "${XTE__DIRARG}${XTE__DIRVAL}"`) + 1494–1496 (`cd "$XTE__DIRVAL"`) | yes |
| status / opened / recheck | `mined` / `2026-10-20` / `on-release` | used-by cites S057; opened matches gate's "all opened 2026-10-20"; `on-release` is an allowed cadence (CORPUS.md:102–103) | yes |
| used-by | `corpus/knowledge/terminal-route-r17.md` | file exists and cites S057 at lines 1, 30, 39–41, 46–47 | yes |

Caveat not a defect: `XTE__EXECARG_DEFAULTS` is only a *custom* default; the ultimate fallback is hardcoded `-e` at line 1128. The row/note say "defaults come from `/execarg_default:` directives", which is true for the custom case and does not misstate the host entry (it declares `X-TerminalArgExec=-e` explicitly).

## Gate line (`corpus/lessons/round-17.md:44`)

`| S057 | <same URL> | xdg-terminal-exec:106 "set workdir of terminal." (4 words) | \`89f2…ac\` |`

- URL: byte-identical to the row's source cell. ✓
- Quote: `set workdir of terminal.` is a verbatim substring of line 106 (the help-heredoc description for `--dir=workdir`); 4 words, within the ≤25-word rule. ✓
- Digest: exact. ✓
- Access date: gate section head states "all opened 2026-10-20"; row `opened` is `2026-10-20`. ✓
- Tier/status/verdict: the gate table has only `id | URL / path | located quote | sha256` (header, lesson line 41); kind/tier/status (`code`/`A`/`mined`) live on the SOURCES row and all check clean. The row's `teaches` verdict is verified above.

## Citing-note claims from S057 at the given anchors

1. `terminal-route-r17.md:30` — "script builds the same sequence from `XDG_CONFIG_HOME`/`XDG_CONFIG_DIRS` and then the data-dir `xdg-terminal-exec/` copies (xdg-terminal-exec:148-162)." **Verified**: 148–163 matches README.md:113–123 item-for-item, including `/etc/xdg` after `~/.config` and `/usr/share` last.
2. `:39-41` — "xdg-terminal-exec:106 documents `--dir=workdir`: 'set workdir of terminal.'"; "option parser is at …1252"; "A desktop entry may carry `TerminalArgDir` (…919)". **Verified** exactly.
3. `:46-47` — "`TerminalArgExec` defaults come from `/execarg_default:` directives (…402-413)." **Verified**; consumer at 1114–1126 and usage at 1092–1101.
4. `:119-123` — "the keys the applicability check and `--dir=` mapping read (xdg-terminal-exec:919, 402-413)". **Anchor-attribution imprecision (N3)**, substance survives (below).

## Precision findings (no falsification)

- **N1 — locator boundaries.** `148-162` omits the closing `done` at 163; `402-413` omits `fi` (414) and `;;` (415). Every substantive line of both constructs is inside the cited ranges, so the labels are accurate; exact-construct ranges would be `148-163` and `402-415`.
- **N2 — gate quote vs compound teaches.** The gate quote grounds the `--dir` half of `teaches`; the lookup-order half is grounded by anchor 148-162 plus README:115-118 (S056), both authenticated by the same file digest. CORPUS.md rule 1 ("a ≤25-word quote with its location grounding `teaches`") reads as satisfied by the digest+anchor pair; noted only as a strictness interpretation.
- **N3 — note's final anchor pair.** At 919 the key read is `X-TerminalArgDir` (correct for the `--dir=` mapping). At 402-413 the script parses a *list-file directive* and stores a default; it does **not** read the desktop-entry key `X-TerminalArgExec` (that read is at **885**, setting `XTE__EXECARG_DEFINED`) and it is not the applicability check (Categories/`TerminalEmulator` read at **816-821**, enforced at 1088-1090). So the sentence's appositive, read literally, attributes to `(919, 402-413)` two reads that happen at 885 and 816-821. The claim's substance — the host entry's keys are ones this script consumes — is true at 885/919; only the anchor pair is loose. Suggested correction if an erratum is ever written: "…the keys the entry-key parser and `--dir=` mapping read (885, 919), with `TerminalArgExec` defaults from `/execarg_default:` directives (402-413)".

## Attack log (what was tried, and why it failed)

- Digest/byte drift: none; fetched raw bytes hash and size match to the byte.
- Wrong tag/file: raw URL pins `v0.14.3`; `ls-remote` returns the note's lightweight tag object; README digest matches its separate row.
- Quote absent/misplaced at 106: present verbatim; word count correct.
- Anchor content absent: every line range contains the construct it is labeled with (106 help, 148–163 lookup, 402–415 directive, 919 key read, 1252 parse).
- "Script agrees with README" overstated: the order is item-for-item identical, and the README's non-key `--dir` fallback ("change dir before executing terminal") is implemented at 1494–1496; `--dir=` is also translated through `X-TerminalArgDir` at 1400–1411.
- Note's S057 claims attributed at wrong anchors: only N3, and it is a pairing imprecision, not a false source statement.
- Status/tier inflation: `mined` + used-by citation resolve; `code`/`A` match CORPUS.md tier rules; census clean for S057.

## Concurrency note (not a finding about S057)

The worktree has in-flight peer edits beyond HEAD: `SOURCES.md` now carries S071 (absent at HEAD) and `terminal-route-r17.md` has wave-2 corrections to the S059 host table and compliance bullet. The S057 row is byte-identical at HEAD and worktree (`sha256` of line 69 equal), and none of the S057-bearing note lines (1, 30, 39–41, 46–47, 119–123) appear in that diff.

## Residual unknowns

- "execution not performed" is an author absence claim; bytes cannot prove a negative. Nothing in the note's S057-derived statements requires execution, and no contradicting evidence exists in the lane.
- Whether installed `xdg-terminal-exec 0.14.3-2` bytes equal the tag is **not claimed** by the row or note (`[UNK] the running binary`); I did not test it either.
- Host-side rows S059/S060/S071 (bindings.conf, lists, Alacritty.desktop) were not re-read here; out of this item's scope.

Confidence: high on row/gate (byte-level match), high on the note's S057 claims; N3 is a wording/anchor nit whose severity depends on how literally the appositive is read.
