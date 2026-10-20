# ReopenS082 — non-author re-open of SOURCES S082

Seat `MadoR18.ReopenS082` (scout, wave 2 = falsify). Target row: S082,
elephant `cmd/elephant/elephant.go` @ v2.22.1. Cited note:
`corpus/knowledge/walker-route-r18.md` (P3). Read-only; no elephant process,
socket or systemd command was touched.

## Commands run and observed output

1. Re-fetch, tag URL:
   `curl -sSL --max-time 60 -o .ufo/waves/round-18/fetch/ReopenS082/elephant.go -w '%{http_code} %{url_effective}' https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/cmd/elephant/elephant.go`
   → `200 https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/cmd/elephant/elephant.go`
   `sha256sum` → `c1c2ecaaafac5282e64467dd93d9e9bc3561fd63c1f160526c5015a8ce5dbd34`;
   `wc -c` → `9283`.
2. `git ls-remote https://github.com/abenz1267/elephant 'refs/tags/v2.22.1*' 'refs/tags/v2.22.1^{}'`
   → `8f1e21d6efe40b8b3953f95b9574f99f717caf91	refs/tags/v2.22.1`
   (one line; no `^{}` peeled line, so the tag is lightweight).
3. Commit-URL cross-check (same file at the tag object):
   `curl … https://raw.githubusercontent.com/abenz1267/elephant/8f1e21d6efe40b8b3953f95b9574f99f717caf91/cmd/elephant/elephant.go`
   → `200`, 9283 B, sha256 `c1c2ecaa…` — byte-identical to the tag-path body.
4. `grep -rn 'elephant/v2.22.1/cmd/elephant/elephant.go' .ufo/waves/round-18/fetch/*/receipts.jsonl`
   → three wave-1 receipts, all `http_status 200`, `bytes 9283`,
   `sha256 c1c2ecaa…`: `NoteWalker/receipts.jsonl:17`,
   `SrcElephantProviders/receipts.jsonl:24`, `ReviewWalkerUpstream/receipts.jsonl:10`.
5. `sha256sum` on the three wave-1 body files named in those receipts
   (`NoteWalker/elephant-v2.22.1-cmd-elephant.go`,
   `SrcElephantProviders/cmd-elephant-elephant.go`,
   `ReviewWalkerUpstream/elephant-2.22.1-elephant.go`) → all
   `c1c2ecaaafac5282e64467dd93d9e9bc3561fd63c1f160526c5015a8ce5dbd34`.
6. Line anchoring on the re-fetched body (`grep -n`, `sed -n … | nl -ba`):
   - 46 `h := xdg.ConfigHome`; 47 `file := filepath.Join(h, "systemd", "user", "elephant.service")`
     (`service enable`); 94–95 the same pair in `service disable`;
   - 124 `common.LoadGlobalConfig()` (in `listproviders`);
   - 177 `{` … 178 `Name: "config"` … 180 usage `"generates a config … Keeps your custom config."` … 187 `handleGenerateConfig(cmd.StringArg("provider"), true)`;
   - 299 `&cli.StringFlag{`, 300 `Name: "config"`, 303 `Usage: "config folder location"`, 305 `common.SetExplicitDir(val)`;
   - 325 `common.LoadGlobalConfig()` in `main`'s Action; `handleGenerateConfig`
     (388–397) ends in `util.GenerateDoc(provider, write)`.
7. My own receipts for both fetches:
   `.ufo/waves/round-18/fetch/ReopenS082/receipts.jsonl` (two
   `mado-fetch-receipt-v1` lines, body files `elephant.go`,
   `elephant.go-at-tagcommit`).

## Findings

**Identity (observed).** My independent fetch reproduces the row's anchor digest
exactly: `c1c2ecaaafac5282e64467dd93d9e9bc3561fd63c1f160526c5015a8ce5dbd34`,
9283 bytes, HTTP 200. All three wave-1 receipts for the same URL carry the same
digest and byte count, and their on-disk bodies re-hash to it. Four seats,
one digest.

**Tag pinning (observed + [INFERENCE]).** The URL names `v2.22.1`, which is a
tag ref (`refs/tags/v2.22.1` = `8f1e21d6…`), not a branch. The same body served
from the tag object's commit SHA is byte-identical, so the tag path served the
tag target's content. [INFERENCE] The tag is lightweight (no peeled line), so
the name could be force-moved upstream; the pin is to tag name plus this
observed digest — the ordinary tag-pin caveat, not a row defect.

**kind / tier / scope.** `kind = code`: it is Go source from the upstream
repository. `tier = A`: the upstream repo at the named tag is the primary
source for the named scope ("elephant CLI … at tag v2.22.1"); nothing
restates another source. The scope cell names the surface keyword `elephant`
(required for P3), and every element it names is present in the bytes:
`--config` flag (299–305), `generate config` (177–187), user systemd unit path
(46–47, 94–95).

**`teaches` grounded.** "--config calls SetExplicitDir" is literally line 305;
"the unit file lives under xdg.ConfigHome/systemd/user" is literally lines
46–47 and 94–95 (`xdg.ConfigHome` + `"systemd"`, `"user"`, `"elephant.service"`).
The anchor list (46-47, 94-95, 124, 177-187, 299-305, 325) resolves line-for-line.

**Citing note truthful.** `walker-route-r18.md:142-144` cites [ED:299-305]
(SetExplicitDir), [ED:325] (main calls LoadGlobalConfig), [ED:177-187]
(`generate config` writes a provider config — line 187 passes `write=true`
into `handleGenerateConfig`, which calls `util.GenerateDoc(provider, write)`);
`:149-152` cites [ED:46-47, 94-95] for `xdg.ConfigHome/systemd/user/elephant.service`.
All quotes match the bytes; the note labels the route documentary and claims no
host process behaviour, so no over-claim. [ED:124] is anchored but unused by
`teaches` — harmless padding, not a false statement.

**Remaining unknowns.** `xdg.ConfigHome` resolving to `~/.config` comes from the
xdg crate, not this file (the note carries a separate XD row for that).
Runtime behaviour of `elephant --config` / `service enable` was not observed
(host pause); the row is documentary, as its status `mined` and the note state.

Verdict: agree with the row as written.

GATE | S082 | https://raw.githubusercontent.com/abenz1267/elephant/v2.22.1/cmd/elephant/elephant.go | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS082/elephant.go:305 | "common.SetExplicitDir(val)" (1 word) | c1c2ecaaafac5282e64467dd93d9e9bc3561fd63c1f160526c5015a8ce5dbd34 | agree: sha matches row anchor and 3/3 wave-1 receipts, tag v2.22.1=8f1e21d6 lightweight and commit-URL body identical, cited lines 46-47/94-95/124/177-187/299-305/325 support teaches, note quotes match
