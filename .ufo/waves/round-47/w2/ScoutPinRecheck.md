# ScoutPinRecheck — w2 FALSIFY: are the pins the bytes upstream serves today?

Verdict: NO HOLE. All three pins and the tag tarball match today's upstream; the tag still resolves to 065925df.
Refetched 2026-10-26 (this run); receipts in `waves/round-47/w2/ScoutPinRecheck/`.

| item | URL | sha256 now | pinned/expected | match |
|---|---|---|---|---|
| README.md | raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md | c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40 | same (receipts/fetch-sha256.txt and fetch/ bytes) | yes |
| xdg-terminal-exec | .../v0.14.3/xdg-terminal-exec | 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac | same (also the C1 judge sha256) | yes |
| xdg-terminals.list | .../v0.14.3/xdg-terminals.list | a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034 | same | yes |
| tag tarball | codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3 | 82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe | 82ac2dfd... (registration/C2 control pin) | yes |

- Tarball members `xdg-terminal-exec-0.14.3/{README.md,xdg-terminal-exec,xdg-terminals.list}` hash identically to the three pins (`tarball-members-sha256.txt`).
- `git ls-remote https://github.com/Vladimir-csp/xdg-terminal-exec.git 'refs/tags/v0.14.3*'` -> `065925df9f419008159258ae169018bfd23df71b refs/tags/v0.14.3`
  (single line, no `^{}` peeled entry: lightweight tag pointing straight at the commit). Matches the expected commit (`lsremote.txt`).
- HTTP 200 on all four fetches; sizes 14762 / 44020 / 1053 / 43291 bytes.

## Observations (not holes in the three pins)
- `receipts/fetch-sha256.txt` covers only the three files above. Extra files in `fetch/` are not in that receipt:
  `xdg-terminal-exec.1.scd` (3dba162f...) and `test/tests.bats` (ce4b6342...) DO equal the tag tarball members (checked);
  `xdg-terminal-exec-proposal.md` (c16a717a..., local) is NOT in the v0.14.3 tarball (path absent), so it came from another
  source (not re-checked: outside the assignment); `desktop-entry-spec.xml` and `omarchy/*` likewise not in the tarball.
  If registration clause d ("xdg-terminal-exec files equal the real v0.14.3 bytes") is read to cover files beyond the three
  receipted ones, the proposal file has no receipted origin in this check.

## Reproduce
```
for f in README.md xdg-terminal-exec xdg-terminals.list; do curl -sSL --max-time 60 https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/$f | sha256sum; done
curl -sSL --max-time 90 https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3 | sha256sum
git ls-remote https://github.com/Vladimir-csp/xdg-terminal-exec.git 'refs/tags/v0.14.3*'
```
Files: refetch-{README.md,xdg-terminal-exec,xdg-terminals.list}, refetch-sha256.txt, urls.txt, tarball-sha256.txt, tarball-members-sha256.txt, lsremote.txt.
Scratch dir removed. No tools installed.
