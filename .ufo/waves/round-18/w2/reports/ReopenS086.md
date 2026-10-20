# S086 — non-author re-open (round 18, wave 2 / FALSIFY)

Seat: MadoR18.ReopenS086. Read-only check of one newly credited SOURCES row
(R17-V3 receipt requirement). Baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`,
integration `4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. No lane write outside
`.ufo/waves/round-18/fetch/ReopenS086/` and this report; no tool installed or
upgraded; no package/service/compositor/process command.

## Row under test (bytes re-read at `4c103b55`)

`| S086 | omarchy bin/omarchy-launch-walker @ v3.8.4 —
https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-launch-walker
| code | A | launcher script that starts elephant and walker service, then execs
walker at tag v3.8.4 | file lines 5-14; sha256
fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8 (equal to host
copy) | the launcher, not walker, starts elephant when pgrep finds none; fixed
window size flags | mined | 2026-10-20 | on-change |
corpus/knowledge/walker-route-r18.md |`

The working-tree row equals the row at `4c103b55` (`git show 4c103b55:corpus/SOURCES.md`
returns the same single `^| S086 ` line). The citing note is unchanged from the
integration commit: `git diff --stat 4c103b55 -- corpus/knowledge/walker-route-r18.md`
is empty, and both working-tree and committed bytes sha256 to
`3ff430a4627d4204ff14c1e9e92eb726a38244ad8c27d8bda412243dfb8fbf20`.

## Independent fetch

Command (fetch rules): `curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}' URL`.

- Tag URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-launch-walker`
  → `200`, final URL identical, **412 bytes**,
  `fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8`,
  fetched `2026-10-20T16:00:54Z`.
  Body: `.ufo/waves/round-18/fetch/ReopenS086/omarchy-launch-walker-tag`
  (receipt line 1).
- Commit-pinned control `https://raw.githubusercontent.com/basecamp/omarchy/8fcc9d6048af4cb0e3af8512c78049857a3b53dd/bin/omarchy-launch-walker`
  → `200`, 412 bytes, same sha (receipt line 2).
- `github.com` blob path control `https://github.com/basecamp/omarchy/raw/v3.8.4/bin/omarchy-launch-walker`
  → `200`, redirects to `raw.githubusercontent.com/omacom/omarchy/v3.8.4/...`,
  412 bytes, same sha (receipt line 3). The `omacom` host in the third wave-1
  receipt is therefore a real redirect (org/repo rename), not a fabricated
  `final_url`; `git ls-remote https://github.com/omacom/omarchy refs/tags/v3.8.4`
  also returns `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`.

Receipts written to `.ufo/waves/round-18/fetch/ReopenS086/receipts.jsonl`,
schema `mado-fetch-receipt-v1`, one line per fetch.

Body read (attached, 14 lines; sha as above), lines 1-14:

```
 1  #!/bin/bash
 3  # omarchy:summary=Launch Walker and ensure its Elephant data provider is running
 5  if ! pgrep -x elephant > /dev/null; then
 6    setsid uwsm-app -- elephant &
 7  fi
 9  # Ensure walker service is running
10  if ! pgrep -f "walker --gapplication-service" > /dev/null; then
11    setsid uwsm-app -- env GSK_RENDERER=cairo walker --gapplication-service &
12  fi
14  exec walker --width 644 --maxheight 300 --minheight 300 "$@"
```

## Receipt cross-check (every wave-1 receipt for this URL)

`grep -rn "omarchy-launch-walker" .ufo/waves/round-18/fetch/*/receipts.jsonl`
returns exactly three wave-1 lines (other errors are `Reopen*` dirs created this
wave with no receipts file yet). All three also exist at `abfbf35`; the bodies
they name hash to the same digest:

| seat | receipt line | url in receipt | http | bytes | sha256 | body file, re-hashed |
|---|---|---|---|---|---|---|
| NoteWalker | 5 | raw…/basecamp/omarchy/v3.8.4/bin/… | 200 | 412 | fd9e93f8… | `omarchy-v3.8.4-bin-omarchy-launch-walker` → fd9e93f8… |
| SrcOmarchyBackground | 17 | raw…/basecamp/omarchy/v3.8.4/bin/… | 200 | 412 | fd9e93f8… | `bin_omarchy-launch-walker` → fd9e93f8… |
| SrcOmarchyWalker | 7 | github.com/…/raw/v3.8.4/bin/… → final `raw…/omacom/…` | 200 | 412 | fd9e93f8… | `bin-omarchy-launch-walker` → fd9e93f8… |

`sha256sum` on all three committed bodies returns
`fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8`. No wave-1
receipt disagrees with the anchor cell, and the independent fetch agrees with all
of them. R17-V3's "body bytes, sha256, byte count, fetch time" is satisfied for
this row (the third receipt's URL is a redirect of the same path, and its
`final_url` is genuine).

## Tag resolution and pinning

- `git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 refs/tags/v3.8.4^{} refs/heads/master`
  → only `8fcc9d6048af4cb0e3af8512c78049857a3b53dd refs/tags/v3.8.4`; no peeled
  `^{}` line ⇒ **lightweight tag**.
- `git ls-remote https://github.com/basecamp/omarchy 'refs/heads/*'` has no
  `refs/heads/v3.8.4`, so the raw URL's `v3.8.4` path component resolves the tag,
  not a same-named branch.
- The commit-pinned URL returns identical bytes, so at read time the tag names
  `8fcc9d60…` and that commit carries this file.
- Host checkout bytes: `~/.local/share/omarchy/.git/HEAD` = `ref: refs/heads/master`;
  `.git/packed-refs:2` and `:508` both pin `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`
  at `refs/heads/master` and `refs/tags/v3.8.4`, matching the note's statement.

**Verdict: the URL is tag-pinned (lightweight tag), not commit-pinned.** The
anchor is reproducible while the tag is not moved, and the row states the tag
honestly. A stricter anchor would be the commit `8fcc9d60…`; that is a hardening
option, not a defect in the row.

## Host-copy cell

`sha256sum ~/.local/share/omarchy/bin/omarchy-launch-walker` →
`fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8`; 412 bytes,
14 lines, equal to the tag body. The anchor's "(equal to host copy)" is true at
read time; it is a host fact that drifts on upgrade, which the `on-change`
recheck column covers.

## Further files named in the row's source/anchor cells

None. S086's source cell names only `bin/omarchy-launch-walker`, and the anchor
cell names the same file plus the host copy — so there was nothing else to
re-fetch. The sibling scripts (`omarchy-restart-walker`,
`omarchy-refresh-walker`) are separate rows S087/S088, not part of this row.

## Judgments

- **kind = code** — correct: an executable bash launcher, not docs or a spec.
- **tier = A** — correct for the scope. The scope is "this omarchy launcher at
  tag v3.8.4"; the raw repository file at that tag is primary for exactly that
  scope. (Tier is scoped, per the registry contract: A = primary/authoritative
  for that scope. It is not a claim about walker's upstream behaviour, which the
  note sources separately from S072-S079.)
- **scope** — accurate: lines 5-7 start elephant, 10-12 start the walker
  service, 14 execs walker. The scope names the P3 surface keywords (`walker`,
  `elephant`), so rubric V's T4 keyword gate is met by the scope cell even
  before the source cell's filename.
- **teaches** — grounded, with one cross-row clause. "the launcher, not walker,
  starts elephant when pgrep finds none" is shown by lines 5-7; "not walker" is
  supported by S075's `walker-v2.17.2-src-main.rs` (`which("elephant")` at 125,
  `set_has_elephant` at 126, `println!("Please install elephant.")` at 673, no
  spawn of elephant), i.e. by a different credited row, not by S086 alone.
  "fixed window size flags" matches line 14 (`--width 644 --maxheight 300
  --minheight 300`). No overstatement found.
- **anchor** — "file lines 5-14" matches every claim; the sha256 matches all
  four bodies (three wave-1, one independent).
- **`used-by` / rubric credit** — `corpus/knowledge/walker-route-r18.md` cites
  S086 in its head `source:` line (line 15) and the row's `used-by` names that
  note; status `mined`, tier `A`, upstream `https://` source of kind `code`
  naming `walker`/`elephant`. Under `.ufo/waves/round-17/measure.py` c2 this row
  satisfies `mined_a` and the T4 upstream condition.
- **note uses it truthfully** — the three note bullets that cite OL are exact:
  OL:5-7 elephant start under `setsid uwsm-app --`; OL:10-12 walker service
  under `uwsm-app` with `GSK_RENDERER=cairo` guarded by `pgrep -f`; OL:14 the
  `exec walker --width 644 …` line. The note's host table entry (sha `fd9e93f8…`,
  412 bytes, "equal to OL") is also exact, and its packed-refs claim is verified
  by file bytes. No quotation drift, no paraphrase that adds behaviour.

## Remaining unknowns / caveats

- `[UNK]` Whether the tag stays at `8fcc9d60…`: lightweight tags are movable; only
  the commit-pinned URL is immutable. Recorded, not a row defect.
- `[UNK]` Whether the host's `~/.local/share/omarchy` checkout equals upstream
  commit contents beyond the files the note compares: only this file (and the
  refs) was re-checked here.
- The `basecamp/omarchy` → `omacom/omarchy` redirect is observed for the
  `github.com/.../raw/...` path only; `raw.githubusercontent.com/basecamp/...`
  serves directly with `final_url` unchanged. Both resolve to the same commit.
- No behaviour was exercised: the launcher was read, never run; no `walker`,
  `elephant`, `omarchy-*`, `pgrep`, or process/socket operation was performed.

GATE | S086 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-launch-walker | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS086/omarchy-launch-walker-tag:6 "setsid uwsm-app -- elephant &" (5 words) | fd9e93f830bc228610df15d754136e066ee920fea5f20817aa93e65d5a1d81d8 | agree: independent 412-byte fetch and all three wave-1 receipts agree on the sha; light-weight tag v3.8.4 resolves to 8fcc9d60 and the commit-pinned URL returns identical bytes; kind/tier/scope match the file and the note's OL:5-14 citations are exact
