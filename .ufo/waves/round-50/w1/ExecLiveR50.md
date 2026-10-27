# ExecLiveR50 — C1 live receipt (round 50 w1, BUILD+ATTACK)

Seat `ExecLiveR50`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `8ae47b957034ae21012bbf09173cca2c48be345e`,
lane HEAD at start `13631f24050f22db92bf5bd33e0f4d014192992e` (round-50 claims commit). Writes: this report +
`.ufo/waves/round-50/w1/ExecLiveR50/**`. Nothing tracked was touched; no git/jj mutation; no dispatcher, keyword, reload,
batch, output or plugin call was made; no GUI or terminal launched; no package transaction; no tool installed.

## Verdict

The host's bind surface is **byte-identical to round 49**: same raw-JSON digest, same total, same four key-form counts,
same modmask histogram, same `resolve_binds_by_sym` value. The round-50 receipt is therefore a re-capture that confirms
S361's numbers rather than moving them, and the C1 entry can be ported with its counts unchanged — only paths move.

## Deliverables (all exist; `test -f` run at the end)

| path (lane-relative) | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-50/w1/ExecLiveR50/binds-live-r50.txt` | `9f16e5a5ce7fe39fc30d8a6041fcdf733f7b794f20310796bae09d01ae51590` | 1768 |
| `.ufo/waves/round-50/w1/ExecLiveR50/binds-shape-r50.txt` | `fca6e79b1dfca54314867ab120ce367bd3cd9768d0e0e8a2b14ecd0889c2c77d` | 1173 |
| `.ufo/waves/round-50/w1/ExecLiveR50/make-receipt.py` | `73b6a7eb52f16e77abf02d56c9f7201f16700c23665b71d558cadf9040d56a36` | — |
| `.ufo/waves/round-50/w1/ExecLiveR50/receipt-run-log.txt` | generator stdout of the canonical run | — |

`binds-shape-r50.txt` is the per-field companion produced from the **same** capture (round 49 shipped the same pair);
it is not a second capture and its own header states the raw digest so the two can never drift apart.

## What the receipt states (all measured by the generator, never typed)

```
command: hyprctl version
hyprctl version: Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
command: hyprctl binds -j
sha256: 9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779   (raw JSON bytes, 90401; not embedded in this file)
key_form_rule: key starting code:/mouse/switch: -> that form; key == "" AND keycode != 0 -> code; otherwise named
binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0
modmask_histogram (modmask count): 0 23 / 1 2 / 8 7 / 9 2 / 12 2 / 13 1 / 64 42 / 65 37 / 68 26 / 69 3 / 72 19 / 73 22 / 76 6
command: hyprctl getoption input:resolve_binds_by_sym -j
input:resolve_binds_by_sym int=0 set=false
```

(the histogram appears as one `  <mask> <count>` line per mask in the file; it is collapsed here only for reading). The
histogram sums to 192 and the form counts sum to 192 — the generator refuses to emit if either sum disagrees, if any
form is empty, or if the three in-run captures disagree.

Privacy: no bind arg, description, dispatcher text, submap, device name, window title or home path is written. The
embed-guard clauses were checked by substring, not by eye:

```
for lit in ('"modmask"', '"dispatcher"', '"arg"', '"description"', '"submap"', '/home/', 'vgpnk'): lit in text
  -> all False;  "hyprctl binds -j" named: True; size 1768
```

The bare word `dispatcher` does appear once, in the sentence stating that no dispatcher was called; clause f's guard is
the quoted `"dispatcher"` token, which is absent.

## What moved vs round 49 — nothing

Round-49 receipt `.ufo/waves/round-49/receipts/binds-live-r49.txt` parsed by the generator's `--compare`:

```
vs_prior: sha256_equal=True total=192/192
vs_prior: named=142/142
vs_prior: code=42/42
vs_prior: mouse=6/6
vs_prior: switch=2/2
vs_prior: histogram_in_prior=no (sha and counts compared; the prior receipt states no histogram)
```

The round-49 *shape* receipt does carry a histogram, and it matches mine mask for mask:
round-49 `.ufo/waves/round-49/receipts/binds-shape-r49.txt` lists `0 23, 1 2, 8 7, 9 2, 12 2, 13 1, 64 42, 65 37, 68 26,
69 3, 72 19, 73 22, 76 6` — identical to the round-50 lines above. `input:resolve_binds_by_sym` is still `int=0
set=false`. Round-49's per-field shape also matches: 18 fields, `keycode_nonzero: 42`, `key_empty: 42`, `mouse_flag_true:
2`, `key_mouse_prefix: 6`, `key_switch_prefix: 2`, `key_single_upper_letter: 60`, `catch_all_true: 0`, `submap_empty: 192`.

Consequence for the freeze: **no S361 number changes in round 50.** The entry port needs new paths (receipt, pin, base,
lesson) and nothing else; the three count lines round 49's entry states at
`.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md:103-105` are still the true values. The receipt itself got
longer (1302 → 1768 B) because round 50 adds the modmask histogram, so a byte count copied from S361's round-49 text is
stale.

Digest stability: every invocation takes 3 captures and refuses to emit if they disagree. Across the wave, 7 generator
invocations (21 captures) plus one ad-hoc probe — **22 captures** — returned **one** digest, `9a47199e…c779`. Because
the generator measures the in-run stability it states, no receipt can claim a stability it did not observe.

## Generator contract (`make-receipt.py`)

`python3 -I make-receipt.py --out F [--shape-out G] [--work DIR] [--compare PRIOR] [--verify COUNTER.py] [--date
YYYY-MM-DD] [--seat NAME]`

- **Reads only** `hyprctl version`, `hyprctl binds -j`, `hyprctl getoption input:resolve_binds_by_sym -j`; stdin is
  `/dev/null`. It never dispatches.
- **Host guard:** `env` is rebuilt (`PATH=/usr/bin`, `LANG=C.UTF-8`) plus only `XDG_RUNTIME_DIR` and
  `HYPRLAND_INSTANCE_SIGNATURE`; `HOME`, `XDG_{CONFIG,CACHE,DATA,STATE}_HOME` are fresh dirs inside a `mkdtemp` under the
  work root, removed afterwards. The real home is never bound or written.
- **Scratch:** `--work` defaults to `TMPDIR`. A work dir under `/tmp`, `/var/tmp`, `/dev/shm`, `/home`, `/root` or
  `/Users`, or under the account home as `$HOME` *or* the passwd entry names it, is refused — a SIGKILL must never leave
  the sandbox inside real home state (sentinel `SentHostState` measured the same gap in the round-50 instruments). An
  absent work root, or one that cannot be created, is a clean rc 2, never a traceback. Nothing is hardcoded to `/tmp`.
- **Determinism:** every value is measured or derived; the only clock input is the capture date. Reproduced from the
  seat copy into two scratch dirs:

```
cd $S/b && python3 -I $D/make-receipt.py --out live.txt --shape-out other-name.txt
cmp $S/a/live.txt $S/b/live.txt   -> equal (LIVE_INDEPENDENT_OF_SHAPE_NAME)
```

  i.e. the live bytes do not depend on the output file name, only on the capture, the date and `--seat`.
  `--date 2026-10-27` reproduces today's bytes on any later day.
- **Refusals measured** — all eight paths `rc=2`, nothing written:

```
rc=2 /home, /home/vgpnk/x, /root/x, /Users/x, /tmp/x, /var/tmp/x, /dev/shm/x, absent-TMPDIR
  -> FAILED work dir under <root> refused: <path>   |   FAILED work dir required: pass --work or set TMPDIR
```
- **Tracks its data (mutant test):** a stub `hyprctl` emitting a doctored table (last bind dropped, one keycode bind
  turned into a named bind) moved every derived value coherently —
  `sha=cae41075bbf9 binds=191 forms=named:142,code:41,mouse:6,switch:2`, mask 73 `22 → 21`, sums still 191. So the
  receipt is not a constant that would pass a replay regardless of the host.
- **Tracks the version (mutant test):** the same stub with `0.55.0` on the version line →
  `FAILED hyprctl version carries no Hyprland 0.56.2 + commit line`, rc 2. A wrong compositor cannot be receipted as
  0.56.2.

## Counter-side readiness (attacked, not assumed)

The round-49 counter's live-capture clause is what this file must satisfy; I re-parsed the emitted bytes with that
counter's **own** helpers instead of trusting my own regexes:

```
python3 -I make-receipt.py --out F --shape-out G \
  --verify quality/counters/c2-r49-bind-entry.py --compare .ufo/waves/round-49/receipts/binds-live-r49.txt
COUNTER_HELPERS: ok forms=named:142,code:42,mouse:6,switch:2 sha=9a47199e2297
MADO_BINDS_RECEIPT: sha=9a47199e2297 binds=192 forms=named:142,code:42,mouse:6,switch:2 out=…
```

(excerpt — the same run also prints the six `vs_prior:` lines quoted above; full stdout is `receipt-run-log.txt`.)

Receipt-side clause-f requirements and their state:

| requirement (`quality/counters/c2-r49-bind-entry.py`) | receipt |
|---|---|
| names `hyprctl binds -j` (`PROBE_CMD`) | present, twice (command line, prose) |
| embeds no JSON (`"modmask"`, `"dispatcher"` absent) | absent (bare `modmask_histogram` header only) |
| `version_ok`: one line with `Hyprland 0.56.2` **and** `efb50993…d9f` | yes, the `hyprctl version` line |
| exactly one 64-hex on `sha256` lines | one, the raw-JSON digest |
| exactly one unambiguous total (`binds=<n>`) | one, `binds=192` |
| one value per form label, `named+code+mouse+switch == total` | 142+42+6+2 = 192, verified by the counter's `forms_in` |
| `resolve_in` reads exactly `{0}` | `int=0 set=false` |
| size inside 512…262144 | 1768 |

Two clause-f details a round-50 port must keep, both load-bearing here:

1. `forms_in` reads `code\s+(\d+)` as well as `code=(\d+)`, so any prose that puts a different number directly before a
   form label breaks the file. My prose says "over 14 distinct keycodes 10,11,…,201" and never a count before a label;
   the `--verify` call above is what proves it, and it is cheap enough to keep in the port's selftest.
2. The histogram block only survives if the embed-guard keeps the *quoted* token (`'"modmask"'`) it has today. A port that
   tightens it to a bare `modmask` substring would reject a receipt whose only "JSON" is a histogram header. If w2 wants
   that tightening, the histogram header must be renamed (e.g. `mask_histogram`), not the guard relaxed elsewhere.

**Pin state (observed, not written by me).** My write scope excludes `.ufo/waves/round-50/fetch/`; another seat copied the
receipt there and the copy is byte-equal to my final bytes:

```
sha256sum .ufo/waves/round-50/fetch/binds-live-r50.txt   -> 9f16e5a5…1590  (1768 B)
cmp fetch/binds-live-r50.txt w1/ExecLiveR50/binds-live-r50.txt           -> equal
grep -n binds-live .ufo/waves/round-50/fetch/SHA256SUMS  -> 8:9f16e5a5…1590  binds-live-r50.txt
```

So S361's `pin … sha256:<hex>` anchor can use `9f16e5a5ce7fe39fc30cd8a6041fcdf733f7b794f20310796bae09d01ae51590` and the
pin name `binds-live-r50.txt` as it stands. Pin name matters: the entry must cite `receipts/binds-live-r50.txt` — clause
`f`/`r` resolve receipt paths under `.ufo/waves/round-50/receipts/` (`RECEIPTS` in the round-49 counter), so the pin under
`fetch/` is a byte anchor and the `receipts/` copy is what the counter opens.

## Risks

- **Cross-day replay (clause r).** `clause r` re-runs the live capture and compares the digest. It passes today; it will
  fail the moment the operator edits a bind, which is the clause working as intended — but it also means a receipt
  generated on 2026-10-27 and replayed after a config change is a *mismatch*, not a defect. The round-50 registration
  should say which date the freeze binds to.
- **`recheck: on-release`.** Nothing in this receipt changes if Hyprland stays at `efb50993`; the entry's recheck trigger
  for S361 (bind plane leaves the receipt) should say *digest*, not *counts*, since the counts survived a whole round.
- The `mouse` field is the `bindm` flag, not "the key is a mouse button" (round-49 finding, values unchanged: 2 true, 6
  `mouse:` key prefixed). The shape receipt keeps the two separate (`mouse_flag_true` vs `key_mouse_prefix`) precisely so
  the entry cannot conflate them.

## Housekeeping

- Scratch `/fast/scratch/hyaku/mado-r50/ExecLiveR50/` removed at the end; no scratch path is cited as evidence, and every
  number above comes from files inside the seat dir.
- No tool installed or upgraded (`python3` 3.x stdlib only, `/usr/bin/hyprctl`).
- `test -f` on every path this report names, run before the yield (round-49 M49-3):

```
OK  .ufo/waves/round-50/w1/ExecLiveR50/binds-live-r50.txt
OK  .ufo/waves/round-50/w1/ExecLiveR50/binds-shape-r50.txt
OK  .ufo/waves/round-50/w1/ExecLiveR50/make-receipt.py
OK  .ufo/waves/round-50/w1/ExecLiveR50/receipt-run-log.txt
OK  .ufo/waves/round-50/w1/ExecLiveR50.md
```

- Final `sha256sum` of the seat dir (what a reviewer should see): `binds-live-r50.txt 9f16e5a5…1590`,
  `binds-shape-r50.txt fca6e79b…c77d`, `make-receipt.py 73b6a7eb…a36`.
- The run log is path-clean: the generator's own `out=` is lane-relative (`.ufo/waves/round-50/w1/ExecLiveR50/…`), so the
  seat dir contains no absolute home path and no scratch path at all (`grep -rn '/fast/scratch\|/home/vgpnk'` → none).
- Coordination: peer `ScrRowsR50` (C1 registry rows) asked for this receipt's sha256/size and `binds=` line; replied with
  `9f16e5a5…1590`, 1768 B, `binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0`, the resolve line, the raw digest,
  the changed byte count vs round 49, and the quoted-token caveat on the embed-guard.
- The canonical run was repeated **in place** after the report and again after the home-refusal change: same
  receipt bytes each time (`RECEIPT_BYTES_UNCHANGED`), so hardening the generator cannot silently move the evidence
  (`SAME_BYTES_REGENERATED_IN_PLACE`), which is the property the freeze needs.
