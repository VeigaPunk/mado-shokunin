# Round-49 w1 — correction lines for N1, N2, N3, N5

seat: `ScrCorrections` · lane `mado-shokunin` · written 2026-10-27
base `03e4ae76aff7a4be59cb69970dd553baa319695a` (2026-10-27 01:21:55 -0300) · lane HEAD during these reads
`5f37c1b87b3ce5e438d19284e32b2e46fd548a92` (the round-49 dispatch commit)
source of the four items: `corpus/lessons/round-48-verifier-spotcheck.md` §6 items 1-5

Method. Every count below comes from a command run in this seat on 2026-10-27 and pasted with its output; locators are
computed (`grep -n`) and not typed. Nothing in the lane was edited: this file is a set of **append-only correction
lines plus their evidence**, for the L1 to paste. No custody, no `git`/`jj` mutation, no operator home write, no compositor
call. Receipts sit beside this file: `n1-untracked-count.txt`, `n2-cache-digest.txt`, `n3-gate-counts.txt`,
`n5-gitlab-files-api.txt`, plus the two fetched pins `api-rules.in`, `api-symbols-br`.

---

## N1 — the untracked `*.synthetic` surplus is 47, not 52

**Target.** `.ufo/reports/round-48/mado.md:37` (fleet repo, read-only for this seat) — "the 52 untracked `*.synthetic`
files under `.ufo/waves/round-45/` and `round-46/`".

**Correction line (append candidate).**
> N1 correction (2026-10-27, round 49): the inherited untracked `*.synthetic` surplus is **47**, not 52 — 45 under
> `.ufo/waves/round-45/w1/RevengerOmarchy/` and 2 under `.ufo/waves/round-46/w1/` (`.ufo/waves/round-46/w1/CritW2Gate.md.synthetic`,
> `.ufo/waves/round-46/w1/CritW2Gate/report.md.synthetic`). Counted with `git status --porcelain -uall | grep -c '\.synthetic$'`. The
> "nothing else untracked" half of the sentence holds for the round-48 tip; inside round 49 the *unscoped* total is
> not stable, because wave-w1 seats are writing their own files while the round runs.

**Counted (stable, scoped).**
```
$ git -C mado-shokunin status --porcelain -uall | grep -c '\.synthetic$'
47
$ ... | awk '{print $2}' | grep -c '^\.ufo/waves/round-45/w1/'
45
$ ... | awk '{print $2}' | grep -c '^\.ufo/waves/round-46/w1/'
2
$ ... | awk '{print $2}' | grep '^\.ufo/waves/round-46/'
.ufo/waves/round-46/w1/CritW2Gate.md.synthetic
.ufo/waves/round-46/w1/CritW2Gate/report.md.synthetic
$ ... | awk '{print $2}' | grep -vE '^\.ufo/waves/round-4[56]/w1/' | wc -l
0
```
`45 + 2 = 47`, and no sidecar path falls outside those two waves. The 47 are untracked surplus, not uncommitted copies
of tracked files: `git ls-files -- '*.synthetic' | wc -l` → `100` (earlier rounds did commit some `.synthetic` paths),
so the two sets are disjoint by path.

**Why the number moves.** At the moment of this read the *unscoped* count was `70`, not 47:
```
$ git status --porcelain -uall | wc -l
70
$ ... | grep -v '\.synthetic$' | awk '{print $2}' | grep -vc '^\.ufo/waves/round-49/w1'
0
```
i.e. all 23 non-synthetic untracked paths are round-49 w1 seat writes created after base `03e4ae76` (01:21:55 -0300);
the count was 59 two minutes earlier and will keep moving until w1 lands. A future report that cites a bare
`wc -l` must date its read and name the wave in flight; the durable number is the scoped 47.

**Attacks/supports.** Attacks `N1` (report count does not reproduce). Supports the spot-check's own §1 row
(`untracked=47`) and the round-49 claims' phrasing "the 47 untracked `*.synthetic` sidecars".

---

## N2 — `host_cache_untouched_sha256` is the w2 mutant's bytes, not an untouched cache

**Target.** `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4`, field
`host_cache_untouched_sha256=c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144`. Lesson line to append
under `corpus/lessons/round-48.md` `## Mistakes`, next to M48-10 (`:263`).

**Correction line (append candidate).**
> N2 correction (2026-10-27, round 49): `host_cache_untouched_sha256` in
> `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4` is `c8b104e6…40144`, which **is**
> `printf 'r48-w2\n' | sha256sum` — the 7 bytes M48-10's unsandboxed M-WRITE mutant left in the operator's resolver
> cache. The field therefore records a *mutated* cache at the 23:20:44 -03 capture, and its name reads as the
> opposite. It is a witness to M48-10, not a clean-state control. Any future receipt of operator-owned state must label
> the pair as operator-owned and state which of before/after is expected clean.

**Verified.**
```
$ grep -n 'host_cache_untouched' .../live-terminal-cache-r48.txt
4:host_cache_untouched_sha256=c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144
$ sed -n 4p .../live-terminal-cache-r48.txt | cut -d= -f2
c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144
$ printf 'r48-w2\n' | sha256sum
c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144  -
$ printf 'r48-w2\n' | wc -c
7
EQUAL: receipt field == printf 'r48-w2\n' digest
```
The two digests are byte-identical, and the mutant payload is 7 bytes — the same 7 bytes M48-10 records
(`corpus/lessons/round-48.md:263`: "overwritten at 22:26:35 -03 with the 7 bytes `r48-w2\n`").

**Limits of this evidence.** This is a digest identity between two byte strings, not a fresh observation of
`~/.cache/xdg-terminal-exec`: this seat neither read nor wrote the operator cache (host guard). The claim "the cache was
still the mutant's bytes at 23:20:44" is the digest showing it; the claim "the cache is clean today" is **not** made
here.

**Attacks/supports.** Attacks `N2` / strengthens `M48-10`. Note the spot-check's own §1 C1 row read this receipt's
field as a live control ("the operator cache mtime `1793069967` did not move during the re-check") — that mtime
observation is separate and unaffected; only the field *name* is at fault.

---

## N3 — the Gate holds 12 admits and 3 rejects, not "five gate decisions (three admits, two rejects)"

**Target.** `corpus/lessons/round-48.md:425` (inside `## Spot-check (pending non-author)`, item 4; the section runs
`:411-431`).

**Correction line (append candidate).**
> N3 correction (2026-10-27, round 49): `corpus/lessons/round-48.md:425` asks for a spot-check of "the five gate decisions
> above (three admits, two rejects)". The `## Gate` section of the same file holds **12 admit blocks**
> (`:55`-`:66`, rows S340-S351) and **3 reject blocks** (`:71`-`:73`). The "five / three / two" wording is a stale
> pre-gate template; the non-author closure in fact sampled 6 of the 15 (S340, S347, S349 admits plus all 3 rejects). The
> line's instruction is unchanged in force — sample the Gate's decisions on outside re-reading — only its counts were
> wrong.

**Counted.**
```
$ grep -cE '^- \*\*S3[0-9]{2} admit\*\*' corpus/lessons/round-48.md
12
$ grep -nE '^- \*\*S3[0-9]{2} admit\*\*' corpus/lessons/round-48.md | cut -d: -f1
55 56 57 58 59 60 61 62 63 64 65 66
$ grep -oE '^- \*\*S3[0-9]{2} admit\*\*' ... | grep -oE 'S3[0-9]{2}' | sort
S340 S341 S342 S343 S344 S345 S346 S347 S348 S349 S350 S351
$ grep -cE '^- \*\*REJECT\*\*' corpus/lessons/round-48.md
3
$ grep -nE '^- \*\*REJECT\*\*' corpus/lessons/round-48.md | cut -c1-120
71:- **REJECT** `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/devices/…
72:- **REJECT** `https://wiki.archlinux.org/title/Xorg/Keyboard_configuration`, opened 2026-10-26.…
73:- **REJECT** `https://xkbcommon.org/doc/current/index.html`, opened 2026-10-26. The current docume…
```
Cross-check, independent of the block regex: the Gate's own prose at `:49` reads `Admitted: rows \`S340\`-\`S351\`` —
12 consecutive ids — and matches the 12 blocks. Sample actually taken by the closure:
```
$ grep -cE '^\| .S3[0-9]{2} admit.' corpus/lessons/round-48-verifier-spotcheck.md
3
$ grep -cE '^\| REJECT ' corpus/lessons/round-48-verifier-spotcheck.md
3
```
15 gate decisions total, 6 sampled.

**Attacks/supports.** Attacks `N3` (stale "five gate decisions"). Supports the spot-check's §4 table (6 rows) and its
§2 C2 row ("rows `S340`-`S351`").

---

## N5 — GitLab files-API fallback for S346/S347: URL form verified; the `-/raw/` premise does **not** reproduce

**Target.** `corpus/SOURCES.md` rows `S346` (`:295`, `xkeyboard-config-2.48/rules/rules.in`) and `S347` (`:296`,
`xkeyboard-config-2.48/symbols/br`), both pinned at commit `cf8d1151bb4c9ef5b895828d0e6dd7860c0833e0`.

**Correction line (append candidate).**
> N5 correction (2026-10-27, round 49): the GitLab files-API form is a verified equivalent fetch route for S346/S347 —
> `https://gitlab.freedesktop.org/api/v4/projects/xkeyboard-config%2Fxkeyboard-config/repository/files/<url-encoded-path>/raw?ref=<tag>`
> with `<path>` = `rules%2Frules.in` / `symbols%2Fbr` and `ref=xkeyboard-config-2.48` returned HTTP 200, `text/plain`, and
> bytes byte-equal to the round-48 pins (`rules.in` 15768 B sha256 `16389776…ffa3`; `symbols/br` 19592 B sha256
> `8cf65550…f35e`), `cmp`-equal to `.ufo/waves/round-48/fetch/`. Carry it as a **fallback when `-/raw/` serves HTML**,
> not as the only working route: on 2026-10-27 the `-/raw/` URLs returned the same pinned bytes on 4 consecutive
> requests, with a normal, a `Python-urllib/3.13` and an empty `User-Agent`. The round-48 closure's "now returns an
> anti-bot page" was not reproducible today, so the transient condition is uncharacterised — record the API form as
> an equivalent alternative and re-test `-/raw/` before declaring it broken.

**Verified (API route).**
```
$ grep -E '^\| S34[67] ' corpus/SOURCES.md | grep -oE 'sha256:[0-9a-f]{64}'
… sha256:163897760093007e1f97808e9319ef2f30bed224c7ea19f0645cca5358b4ffa3   (rules.in, S346)
… sha256:8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e   (symbols/br, S347)
$ curl -sS -L -o api-rules.in '…/files/rules%2Frules.in/raw?ref=xkeyboard-config-2.48' -w 'http=%{http_code} bytes=%{size_download} ctype=%{content_type}\n'
http=200 bytes=15768 ctype=text/plain; charset=utf-8
$ curl -sS -L -o api-symbols-br '…/files/symbols%2Fbr/raw?ref=xkeyboard-config-2.48' -w '…'
http=200 bytes=19592 ctype=text/plain; charset=utf-8
$ sha256sum api-rules.in api-symbols-br
163897760093007e1f97808e9319ef2f30bed224c7ea19f0645cca5358b4ffa3  api-rules.in
8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e  api-symbols-br
$ cmp api-rules.in .ufo/waves/round-48/fetch/xkeyboard-config-rules-rules.in && echo equal
rules.in API == pin
$ cmp api-symbols-br .ufo/waves/round-48/fetch/xkeyboard-config-symbols-br && echo equal
symbols/br API == pin
```
Both API digests equal the digest in their row **and** the committed round-48 pin.

**Counter-evidence (the reason the append line is worded as a fallback).**
```
$ curl -sS -L 'https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/xkeyboard-config-2.48/rules/rules.in' -w '…\n'
raw rules/rules.in run1 http=200 bytes=15768 ctype=text/plain; charset=utf-8 16389776…ffa3
raw rules/rules.in run2 http=200 bytes=15768 ctype=text/plain; charset=utf-8 16389776…ffa3
raw symbols/br  run1 http=200 bytes=19592 ctype=text/plain; charset=utf-8 8cf65550…f35e
raw symbols/br  run2 http=200 bytes=19592 ctype=text/plain; charset=utf-8 8cf65550…f35e
$ curl -A '' …/-/raw/…/symbols/br -w '…'
empty-ua http=200 bytes=19592 ctype=text/plain; charset=utf-8
```
Five `-/raw/` requests, five pinned-byte bodies, no HTML. So the spot-check's parenthetical ("the `-/raw/` URL now
returns an anti-bot HTML page") is **not reproducible from this host on 2026-10-27**; the anti-bot page it saw is either
transient, rate/route-dependent, or was seen from a different egress. Recording the API form as the sole route would
freeze an unverified premise into the registry note.

**Attacks/supports.** Supports `N5`'s *remedy* (an equivalent fetch URL form exists and reproduces the pins) and attacks
its *premise* (that `-/raw/` is broken). Also supports the freshness re-fetch path for any xkeyboard-config row.

---

## Findings summary

| id | target file:line | correction | evidence | verdict |
|---|---|---|---|---|
| N1 | `.ufo/reports/round-48/mado.md:37` | 52 → **47** (45 r45 + 2 r46) | `git status --porcelain -uall` scoped count | reproduces |
| N2 | `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4` + `corpus/lessons/round-48.md:263` | field is the mutant's 7 bytes, not a clean control | digest equality with `printf 'r48-w2\n'` | reproduces |
| N3 | `corpus/lessons/round-48.md:425` | "five (3 admit, 2 reject)" → **15 (12 admit, 3 reject)**, 6 sampled | `grep -cE` block counts + `:49` prose cross-check | reproduces |
| N5 | `corpus/SOURCES.md:295`, `:296` | API fallback URL form works and pins reproduce; `-/raw/` was **not** broken today | 2 API fetches `cmp`-equal + 5 `-/raw/` fetches byte-equal | remedy verified, premise contradicted |

Open, not corrected by this seat (named, not upgraded):
- **N5's anti-bot page** — uncharacterised. Whoever re-tests it should record egress, UA and HTTP status, because the
  round-48 observation does not reproduce from this host. Depth of investigation stopped at "does it happen here now":
  five requests over ~5 minutes is not a rate-limit study.
- **N1's unscoped total** — inherently unstable during a live wave; only the scoped 47 is citable.
- **N2 today's cache state** — deliberately not observed (host guard). The spot-check's 190 B / `ddd94f6b…` /
  mtime `1793069967` reading is the only recent observation and this seat did not re-measure it.
- The 47 sidecars' **disposition** (commit vs remove) is the L1's call and is not decided here.

Out of scope by assignment: N4 (round-48 v2 matrix text rows), M48-8, M48-10's own fix, M48-13, `w2/SentScratch`, the
`registration-v2.md` residuals, and every C1/C2 claim.
