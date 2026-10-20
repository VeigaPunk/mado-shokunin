# SkillErratumAttack — partial

Attack seat: AtkSkillErratum. Target: the round-19 SKILL.md erratum at the tip
`01b80946d92b26370d3012a7da655d00dd135154` (heading `## Errata (round 19, append-only — walker 2.17.2 pins; S090/S091/S096)`, tip `SKILL.md:1853-1865`), and the baseline lines it cites from
`9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.

Bottom line: **every host-file value the erratum asserts reproduces exactly** (binary bytes/hash,
BuildID, `.comment`, rodata offset, embedded config, both config files, package identity, and the
2026-10-14 values it transcribes). Two **intra-file locators** and one **completeness sentence** do
not survive byte checks against the committed tip. There is no evidence of an executed `--version`
or `pacman -Qkk` being smuggled in as observation — both are explicitly disclaimed.

## Attack 1 — host values (all reproduced, independently re-run)

Commands (read-only file bytes; no walker, pacman, hyprctl, or process probe):

```
sha256sum /usr/bin/walker ; stat -c '%s' /usr/bin/walker
readelf -n /usr/bin/walker | grep -i 'build id'
readelf -p .comment /usr/bin/walker
python3 -c "d=open('/usr/bin/walker','rb').read(); ..."   # literal scan + embedded-config slice
wc -l /etc/xdg/walker/config.toml ; wc -c ... ; sha256sum ...
wc -l ~/.config/walker/config.toml ; wc -c ... ; sha256sum ...
```

Observed:

| erratum assertion (tip line) | observed |
|---|---|
| `/usr/bin/walker` 7,039,912 B, sha256 `25240650…` (`:1860`, `:1861`) | `7039912`; `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` |
| BuildID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` (`:1861`) | identical (`readelf -n`) |
| `.comment` rustc 1.99.0 (b940084d7 2026-09-28), LLD 23.1.1, GCC 16.2.1 20260810 (`:1862`) | identical three lines (`readelf -p .comment`: `rustc version 1.99.0 (b940084d7 2026-09-28) (Arch Linux rust 1:1.99.0-1)`, `Linker: LLD 23.1.1`, `GCC: (GNU) 16.2.1 20260810`) |
| sole version literal `2.17.2` at file offset 856,302, run `version2.17.2\n`, in `.rodata` (`:1860`, `:1864`) | all `2.17` hits in the 7 MB binary are exactly two: offset 23,204 `GLIBC_2.17` (dynstr) and 856,302 `version2.17.2\ntoggle exact search…`; `.rodata` = file off `0x0b6900`, size `0x074654` → 747,776–1,224,531, contains 856,302 |
| embedded default at 806,960 = 13,743 B / `3c5c6867…`, byte-equal to `/etc/xdg` (`:1864`) | `d[806960:806960+13743]` sha256 `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`, `slice == /etc/xdg file` True, 305 newlines, exactly one copy in the binary |
| `/etc/xdg/walker/config.toml` 305 L / 13,743 B / `3c5c6867…` (`:1855`, `:1857`) | 305 / 13,743 / `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b` |
| `~/.config/walker/config.toml` 49 L / 1,336 B / `fecf71fa…` (`:1859`) | 49 / 1,336 / `fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787` |
| installed package 2.17.2-1; log line 2929 (`:1855`) | `/var/lib/pacman/local/walker-2.17.2-1/desc` `%VERSION%` → `2.17.2-1`; `/var/log/pacman.log:2929` = `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)` |

Fetch receipt (for the erratum's "byte-equal to the upstream v2.17.2 `resources/config.toml`":

```
url=https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/resources/config.toml
http=200 bytes=13743
sha256=3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b
fetched_at=2026-10-20T18:06:57Z  (saved /tmp/walker-upstream-config.toml)
```

Baseline values the erratum transcribes (`:1860`-`:1864`) were checked against the still-cached
`/var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst` extracted to `/tmp/w2170`:

- sha256 `64826a8531eac525adfa3eff65548e93a6f7714feb1d3e13b4fa35bbcc3cfda0` (erratum prefix `64826a85…` OK), size 6,661,264;
- BuildID `a22452d1e4243bad1bf9fd487aa569f673ad9c5a` (`a22452d1…` OK);
- `.comment` `rustc version 1.97.1 (8bab26f4f 2026-07-14) (Arch Linux rust 1:1.97.1-1)` and `Linker: LLD 22.1.8` (OK);
- `version2.17.0\n` at offset **847,791**, zero other `2.17.0` occurrences (OK).

So the old-line quotations are faithful, not invented. The erratum's two self-restraints are also
accurate: it says the printed `--version` line is **inferred** from the literal, not observed
(`:1860`), and it leaves `pacman -Qkk` as `[UNK]` rather than asserting the round-9 count (`:1863`).
The host-pause framing is consistent with the ban in force; no execution happened here either.

## Attack 2 — intra-file locators (break at the committed tip)

The tip is not a pure tail append: the same commit adds 6 lines to the instrument table at
`SKILL.md:572-577` (`git diff 9c54c56 01b8094 -- SKILL.md` hunk `@@ -571,0 +572,6 @@`), shifting
every line after 571 by +6. The erratum's bare cross-references were not re-numbered:

- `SKILL.md:1855` — "the round-18 erratum at `:1820-1828` already dates `:23` and `:114`".
  At the tip, 1820–1828 is the round-12 tail plus blanks plus the round-18 heading (1826) and one
  line of the round-18 blockquote (1828); the dating sentence is at **1830**, outside the cited
  range. The range is correct only in baseline numbering (baseline 1820 = heading, 1824 = dating
  line). The round-18 erratum at the tip is `1826-1836`.
- `SKILL.md:1857` — "dated 2026-10-14 (round-18 erratum `:1824`)". At the tip, line 1824 is an
  **empty line** (1823 is the round-12 "Append-only disposition" paragraph; 1824 and 1825 are
  blank). The cite resolves only against baseline `9c54c56:SKILL.md:1824`, which does carry the
  dating sentence.
- The erratum's own former-line refs `:23`/`:114` still resolve at the tip (both precede the
  insertion), and `:1075`/`:1473-1476` are labelled "Former" — they are baseline refs, and
  `walker --version` now sits at tip `:1081`. So the substantive pointer set is recoverable by a
  reader, but the two bare `:18xx` locators are not.

Evidence bytes:
`git show 01b8094:SKILL.md | sed -n '1820,1832p'` → 1820 round-12 bullet, 1823 disposition, 1824 blank,
1826 heading, 1830 `("walker 2.17.0"; packaged table "298 L") are dated 2026-10-14…`.
`git show 9c54c56:SKILL.md | grep -n '^## Errata (round 18'` → 1820; `walker --version` at 1075.

## Attack 3 — "the only moved value on that row"

`SKILL.md:1859`: "the only moved value on that row is the walker version, now 2.17.2 (S090)."
Line 114 is the launcher row; it contains, in this order, `49 L` (unchanged), packaged table
`298 L` (**moved**, and the immediately preceding bullet `:1857` itself re-states it as `305 L`),
and `walker 2.17.0` (**moved**). Two values on the row require supersession, so "the only moved
value" is contradicted both by host bytes and by the erratum's own previous bullet. The charitable
reading ("only moved value in this cell") fails too: `298 L` is inside the same markdown cell as
`49 L`. Correct form would have been "the `49 L` value is unchanged; the row's moved values are the
packaged length (305 L) and the walker version (2.17.2)".

## Attack 4 — quoted-line precision (minor)

- `:1861` heads "Former `SKILL.md:1473` — 'binary sha256 `64826a85…`, BuildID `a22452d1…`'".
  Baseline 1473 ends at `binary sha256 64826a85…,`; `BuildID a22452d1…` begins baseline 1474.
- `:1864` heads "Former `SKILL.md:1476` — 'printed `2.17.0\n` … rodata literal (offset 847,791)'".
  The word "printed" is on baseline 1475; 1476 starts at `` `2.17.0\n` ``.
Both quotes merge wrapped lines under one line number. The values are right; only the per-line
attribution is overprecise.

## Attack 5 — the `[UNK]` is a gap, not an impossibility (not a break)

`SKILL.md:1863` says the `-Qkk` count stays `[UNK]`. That is honest about what was run, but the
answer is recoverable read-only: `/var/lib/pacman/local/walker-2.17.2-1/mtree` binds
`./usr/bin/walker` to `sha256digest=25240650…96` (equal to the installed bytes, so the installed
binary is the package's file, not a rebuilt one), and hashing the 19 regular-file entries gives
0 altered, with all 10 directories present. The two `.BUILDINFO`/`.PKGINFO` entries are not
installed at `/` (they live in the local db). [INFERENCE] A `pacman -Qkk`-equivalent read is
therefore available without pacman; the erratum does not claim otherwise, so this is a limits note,
not a false assertion.

## Limits

- No walker/elephant execution, no `--version`, no pacman (including `-Q`), no systemctl/hyprctl,
  no process probe, no gate run. Running state remains `[UNK]`, matching the erratum.
- The old 2.17.0 identity was verified from the cached package bytes, not from a live install;
  if the cache entry were a rebuild of the same NEVRA the digests could differ, but here the
  extracted sha matches the erratum's prefix and the round-9 note's values.
- `.comment`/BuildID claims were checked with `readelf` on the exact installed file; no
  independent upstream-build reproduction was attempted.
- Citation findings are against committed tip `01b8094` only; they are caused by the 6-line
  table insertion at `:572-577` landing after the erratum text was numbered, not by a host change.
- `walker-route-r18.md` exists and is v2.17.2-oriented with SOURCES rows S073/S090/S091/S096
  routing to it; its internal prose was not re-audited in full.

## Verdict

**partial** — the measured host state holds on every axis (binary, toolchain, offsets, both config
files, package/version binding, and the transcribed old values); the erratum overclaims nothing
about execution. It does carry two stale intra-file locators that resolve to the wrong bytes at the
tip (`:1820-1828`, `:1824`), one false completeness sentence about the launcher row's moved values,
and two line-attribution merges. None of these change a host fact; all are fixable by re-numbering
the two `:18xx` cites to `1826-1836`/`1830` and dropping "only" from `:1859`.

## Installs

None.
