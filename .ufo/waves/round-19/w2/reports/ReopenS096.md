# ReopenS096 — holds

Seat ReopenS096 (round-19 w2, FALSIFY). Item: re-open S096 (`corpus/SOURCES.md:108`) independently — do its anchors reproduce, is the lesson § Gate quote located and true, does the row claim anything beyond file bytes.

Verdict: **holds** on all three questions. Every anchor value reproduces from host file bytes; the Gate quote is true, 1 word, and locatable; the row explicitly disclaims running-process and `--version` facts and I found no S096-derived runtime claim. Two adjacent defects are recorded below — one in the row's `used-by` cell, one in two notes' prose *about* S096 — neither touches the row's evidence.

Attack surface tried: tampering after install (checked against the pacman cache package), a second or ambiguous version literal, a mislabeled offset, digest/date drift, and any claim wider than file bytes.

## 1. Anchors re-derived from host bytes (OBS)

```
$ sha256sum /usr/bin/walker
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
$ stat -c '%s %y' /usr/bin/walker
7039912 2026-10-08 11:14:32.000000000 -0300
$ file /usr/bin/walker
ELF 64-bit LSB pie executable, x86-64 … BuildID[sha1]=19200fe47eb6c90fc4956f0d52d0c7c84bb89e99, stripped
$ readlink -f /usr/bin/walker
/usr/bin/walker
```

Literal scan (`open('/usr/bin/walker','rb').read()`):

```
data.find(b'2.17.2') -> 856302 ; data.count(b'2.17.2') -> 1
data.find(b'2.17.0') -> -1      ; data.find(b'2.17.1') -> -1
data[856302:856309] = b'2.17.2\n'
data.find(b'loadstruct Action with 6 elementsversion2.17.2\ntoggle exact search') -> 856262 (66 B)
```

Section bounds — `readelf -SW /usr/bin/walker`: `[12] .rodata PROGBITS 00000000000b6900 0b6900 074654` → file bytes 747,776–1,224,532; 856,302 lies inside. Broader `2.17` scan: 2 hits — `GLIBC_2.17` at 23,204 and the version literal at 856,302; no UTF-16 form.

```
$ sha256sum /var/lib/pacman/local/walker-2.17.2-1/desc
5c0d9d89d3e8d6c433b89ebaf2bb8f11056e15cfaed69a430333e0b8d50b0928
desc: %VERSION% 2.17.2-1 ; %BUILDDATE% 1791468872 ; %INSTALLDATE% 1792498606
$ date -u -d @1791468872 +%FT%TZ ; date -u -d @1792498606 +%FT%TZ
2026-10-08T14:14:32Z
2026-10-20T12:16:46Z
$ sha256sum /var/log/pacman.log ; stat -c %s /var/log/pacman.log
27bbd0b558cfbc6ee27f5644863d6a62e1b468d462f4ea0de577ced86b256ffc  244858
$ sed -n '2929p' /var/log/pacman.log
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
$ sha256sum /var/lib/pacman/local/walker-2.17.2-1/mtree      # gzip file as bytes
d5dfb3f1f4d964aed2ab984c256df29109c8f67c42277b4e4168e279f1519aa4
$ zcat …/mtree | sed -n '30p'
./usr/bin/walker time=1791468872.0 size=7039912 sha256digest=25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096
```

| row cell (`SOURCES.md:108`) | re-derived | match |
|---|---|---|
| 7,039,912 B | `stat` 7039912 | yes |
| sha256 `25240650…93096` | `sha256sum` same | yes |
| mtime `2026-10-08T11:14:32-0300` | `stat` `-0300` | yes |
| BuildID `19200fe4…89e99` | `readelf -n`, `file` | yes |
| literal `2.17.2\n` @ **856,302** | `find` 856302, bytes `2.17.2\n` | yes |
| `.rodata` off `0x0b6900`, size `0x074654` | `readelf -SW` | yes |
| context `…loadstruct…toggle exact search…` | contiguous at 856262 (66 B) | yes |
| `desc` sha256 `5c0d9d89…b0928` | `sha256sum` same | yes |
| `%VERSION%` `2.17.2-1` | `desc` body | yes |
| `%BUILDDATE%` `1791468872` = `2026-10-08T14:14:32Z` | `date -u` | yes; equals mtime to the second |
| `%INSTALLDATE%` `1792498606` = `2026-10-20T12:16:46Z` | `date -u` | yes; equals log:2929 `09:16:46-0300` |
| log 244,858 B sha256 `27bbd0b5…56ffc`, line 2929 | `sha256sum`, `sed` | yes |
| `mtree` gzip sha256 `d5dfb3f1…19aa4`, line 30 digest = binary digest | `sha256sum`, `zcat` | yes |
| "no `2.17.0` literal survives (0 hits)" | `find b'2.17.0'` → -1 | yes, of the binary (see F3) |

Independent strengthening: the installed binary is byte-identical to the packaged one, checked against the cache archive itself, not only the local `mtree`:

```
$ bsdtar -xf /var/cache/pacman/pkg/walker-2.17.2-1-x86_64.pkg.tar.zst -C /tmp/s096y usr/bin/walker
$ sha256sum /tmp/s096y/usr/bin/walker /usr/bin/walker
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /tmp/s096y/usr/bin/walker
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
$ cmp /tmp/s096y/usr/bin/walker /usr/bin/walker && echo CMP_IDENTICAL
CMP_IDENTICAL
```

The cached 2.17.0 package also settles the offset convention on the prior build (without network or pacman): its binary is sha `64826a8531eac525…`, and `2.17.0` starts at 847,791 while the 13-byte run `version2.17.0` starts at 847,784 — the same 7-byte relationship as the new build. `[INF]` the rodata literal is walker's version: adjacent `version` token in both builds, package `desc` and transaction log independently say 2.17.2/2.17.2-1, and round 9 observed the 2.17.0 print equal to that literal (`walker-deep-r9.md:107-116`).

## 2. The lesson § Gate quote (`corpus/lessons/round-19.md:41`)

Cell 5 is `` `/usr/bin/walker` byte 856,302: "version2.17.2" (1 word) ``.

- Word count: 1 → ≤25 satisfied.
- Text: `version2.17.2` is contiguous in the binary at 856,295–856,307, followed by the LF at 856,308. The quote is true and searchable.
- Alignment: the cited byte 856,302 is the first byte of `2.17.2\n`; the quoted run's first byte is 856,295 (7 earlier). This is the lane's established convention, not a new error: `walker-deep-r9.md:109-116` quotes `…version` + `2.17.0` + LF and gives 847,791, which in the cached 2.17.0 binary is the `2` of `2.17.0` (the `version` run begins at 847,784). The w1 draft that authored the row kept the qualifier — `.ufo/waves/round-19/drafts/HostWalkerBytes-row.md:16-17`: "`/usr/bin/walker` @ byte 856,302: `version2.17.2` — the literal is the 7 bytes `2.17.2\n` (digits at 856,302, LF at 856,308)". The lesson § Gate cell compresses that line and drops the "(digits at 856,302, LF at 856,308)" qualifier, so as landed it reads as if the quoted run starts at 856,302. `[INF]` if the Gate standard demands quote-start == cited byte, this cell needs offset 856,295 or the quote `2.17.2`; as written it still locates the version token, and the row's own `2.17.2\n` @ 856,302 is exact. (Independent wave-2 seat AtkLessonGate reports the same 856,295 start; my check above is byte-derived, not taken from that report.)

## 3. Claims beyond file bytes?

- Row scope cell: "read as file bytes only (no walker or pacman execution)". Row teaches cell: "**no running-process fact is claimed** — `walker --version` was not executed (host pause)". Both true of what I ran: walker and pacman were never invoked.
- Uses agree: `SKILL.md:1864` calls the printed line inferred from the literal, "not observed"; `corpus/knowledge/walker-route-r18.md:328` keeps `--version` and runtime `[UNK]`.
- The gate's live arm (`tools/mado-verify.sh:3294-3296`) does execute `walker --version` and compares to `WALKER_VERSION_PIN="2.17.2"` (`:105`); that is the gate's own runtime measurement, not an S096 claim. No file in the lane states a *running* walker version on S096's authority.

## Adjacent findings (true at tip 01b8094; not counters to the row's evidence)

**F1 — two committed notes deny S096 exists (real; being repaired in w2).** At the tip under attack:

- `corpus/knowledge/walker-live-surface.md:305` — "…the host binary bytes are reserved as S096 (row pending, not re-read this round)."
- `corpus/knowledge/remaining-planes-census.md:338` — "…the binary-bytes row S096 is reserved and not yet recorded."

`SOURCES.md:108` is a `mined` row opened 2026-10-20 and `lessons/round-19.md:41` opened it, so both sentences are false at tip. Both files nonetheless count as *current* in the C2 counter — `python3 -I .ufo/waves/round-19/fresh-pins.py 01b8094…` → `denominator 13 current 13 score 10.0`, with `remaining-planes-census` `pointer_lines [338, 340]` and `walker-live-surface` `[305]` — i.e. 13/13 includes two pointer lines whose prose denies the source row exists. Both lines also carry `S090`, so the counter's `S###` arm would pass on them even if S096 did not exist (the pointer proves a row token is present, not which row the pointer is about). `[INF]` this is exactly the QUALITY 28 review limit ("a reviewer reads each pointer"), not a counter defect. The worktree already carries append-only w2 corrections to both files from peers; the finding is stated against committed tip bytes (`git show 01b8094…:<path>`), which is what I attacked.

**F2 — row `used-by` cell is incomplete (row metadata, observed).** The cell lists `walker-deep.md, walker-deep-r9.md, walker-live-surface.md, remaining-planes-census.md, tools/mado-verify.sh, SKILL.md`, but at tip S096 also carries present-tense use in `corpus/knowledge/walker-route-r18.md:328` and `corpus/README.md:137`; the lesson's status/recheck/used-by change block logs only S084/S094, so this is unlogged. `[UNK]` whether `corpus/QUALITY.md:186` (criterion-28 runnable-check prose naming rows S090/S096) counts as `used-by` by the registry's convention.

**F3 — "no `2.17.0` literal survives (0 hits)" is binary-scoped.** True of `/usr/bin/walker` (0 hits), but `/var/log/pacman.log` retains three `2.17.0` strings: byte 47,100 (`libvpl 2.17.0-1`), 144,158 (walker `2.16.2-1 -> 2.17.0-1`) and 222,448 (walker `2.17.0-1 -> 2.17.2-1`). The sentence's subject and the lesson's `find` phrasing scope it to the binary; a host-wide reading would be false. `[INF]` wording risk only.

**F4 — "three independent file-byte facts" is a characterization.** The rodata literal is independent of pacman; `desc` and the log line are two pacman-authored records of one transaction. Values all hold; "independent" is loose `[INF]`.

**Wave-1 limit corrected.** `.ufo/waves/round-19/w1/reports/HostWalkerBytes.md:127` says the old 2.17.0 binary was "not present on disk". `/var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst` (2,460,483 B) contains it; extraction gives sha `64826a85…` matching the round-9 pin, with no network and no pacman. This strengthens, not weakens, the row.

## Limits

- Host pause respected: no walker, pacman, yay, paru, systemctl, journalctl, `/proc`, compositor, input or screenshot operation; no gate run; no network.
- `walker --version` was **not** executed, so the printed line stays `[UNK]`; the row does not claim it.
- Lane bytes read at the committed tip via `git show 01b8094…` for the files I cite; host files read as bytes; two cached package members extracted to `/tmp` only. No lane edits (this report only).
- Remaining unknowns: `[UNK]` which binary the running walker process executes; `[UNK]` whether this binary is a faithful build of the upstream v2.17.2 tag beyond its packaged digest; `[UNK]` the `used-by` convention for QUALITY prose (F2).

## Installs

none.
