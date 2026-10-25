# ScoutGrammar — is S277's community-tier grammar independently corroborated?

**Lane:** mado-shokunin (read-only attack on round 38, wave 1)
**Seat:** `L1Mado38.ScoutGrammar` (scout, leaf — no subagent dispatch)
**Date of all accesses:** 2026-10-25 (UTC-agnostic local clock; all fetches same day)
**Question assigned:** cross-check the request-grammar claims against a SECOND independent source; for each opened, does it confirm `[flag(s)]/command args`, no length prefix/newline, and the flag list; verdict on whether S277's community-tier grammar corroborates independently or is the only non-first-party voice.

**Bounds honoured.** No lane production file was edited. No git write in LANE (`git -C LANE` was never run with a mutating verb; LANE `git status` not used). No socket was connected; no hyprctl invoked. All fetched bytes live in `/tmp/mado38-ScoutGrammar/` and `/tmp/tmp.*` (scratch clones made with `mktemp -d` + `git init -q`, verified `rev-parse --show-toplevel`). One `git clone`-style scratch fetch of a public repo was done in a `mktemp -d` sandbox only. No tool was installed (nothing needed installing; `curl`, `git`, `python3` were already present).

---

## 0. Verdict up front

**S277 is NOT the only non-first-party voice — but the community tier it belongs to is thin in exactly the way that matters, and the corpus overstates one thing.**

Three separate verdicts, because the three sub-claims have different answers:

| Sub-claim | First-party corroboration | Independent (non-first-party) corroboration | Verdict |
|---|---|---|---|
| `[flag(s)]/command args` grammar | **Yes** — wiki IPC page (current + 0.56.0 + 0.54.0 + 0.41.0), verbatim, stable across 4 versions | **Yes, in code** — 5 independent re-implementations emit `j/<cmd>` / `/<cmd> args` | Corroborated |
| no length prefix / no newline | **Yes, in code** — hyprctl client writes `arg` verbatim, no terminator; server accumulates raw bytes | **Yes, in code** — 6+ independent clients write raw bytes; **only S277 states it in prose** | Corroborated; prose attribution is S277's alone |
| the flag list (`j`, `i`, `r`) | **Yes (docs) + NO (server)** — see §3, a real divergence | **No** — not one community source enumerates the flags | **Weakest link** — see finding F-1 |

**Headline finding (F-1, divergence, first-party):** the corpus's flag-list claim rests on the *hyprctl CLI* flag list, but the *request-socket* flag alphabet is different. The wiki's `flag list:` block publishes `j`, `i`, `r`. The server's own flag parser (S158, the host's own v0.56.2 `HyprCtl.cpp`) accepts **`j`, `r`, `a`, `c`** — `i` is *not* a socket flag at all; it is a **client-side** `hyprctl -i` instance selector that never reaches the socket. The published list omits `a` and `c` (both are real socket flags at v0.56.2) and includes `i` (which is not). `corpus/knowledge/hyprctl-flags-r28.md` §1 states the published list as *"the published flag vocabulary of the request socket"* and §3 admits the server-side handling of each flag was "not re-read this round". S158 *is* in the round-38 fetch set, so this is a re-grounding gap, not a missing-source gap.

**Second headline finding (F-2, provenance, community tier):** S277's pinned commit is **not reachable** — the SHA `707cf7f8b39d0b4e2cba46d0a2559b562d8821ce` is absent from all 192 branch refs and all 88 `refs/pull/*` refs of the repo; `git fetch` of that SHA fails `upload-pack: not our ref`. The *content* is still live at `main` and is **byte-identical** to the lane's receipt (sha256 `ff561fe0…781e6`), so the citation's *bytes* are sound today, but the *pin* is dead. `corpus/SOURCES.md:223` also cites the URL under owner `chriskearney` while `corpus/knowledge/request-socket-live-bound-r8.md:9` cites the same commit under `iconidentify` — same repository (one redirects to the other, `HEAD` = `c37fbe3e439dc27db9ce8176546febb58680dfc5` for both), but the two citations are not the same string.

**Third finding (F-3, benign but worth recording):** the community tier's *prose* claim is uniquely S277's. No other community source states "no length prefix or newline" in words. Every other corroborating source is a *client implementation* whose code implies it. The corpus currently cites S277 as if it were the only community voice on the grammar; that is **half true** — it is the only community voice on the *framing*, but five other community voices exist on the *grammar* (`[flags]/command args`). The corpus is under-crediting its own evidence.

---

## 1. What exactly is being claimed (the attack surface)

Frozen spec: `LANE/.ufo/waves/round-38/registration.md`. The claims under test, as they appear in the committed corpus at HEAD:

`corpus/knowledge/request-socket-live-bound-r8.md:42-45`:
> **OBS** S277: a third party that re-implements Hyprland's IPC measured the grammar off a real client and reports the same — `There is no length prefix or newline.` and `[[BATCH]]` batch requests with `;` separators — a community-tier cross-check, not first-party evidence.

`corpus/SOURCES.md:223` (S277 row), flags cell:
> `[flags]/command [arguments]`, no length prefix or newline, `[[BATCH]]` batch - matches S187, at community-tier weight

`corpus/lessons/round-38.md:17`:
> GATE S277 receipt=.ufo/waves/round-38/fetch/S277.bin sha256=ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6 quote="There is no length prefix or newline."

`corpus/knowledge/hyprctl-flags-r28.md:15-16`:
> **OBS** S221: the 0.56.0 documentation publishes the flag list as three flags — `j -> output in JSON`; `i -> select instance (id or index in hyprctl instances)`; `r -> force state refresh after issuing commands (e.g. layout or rule changes)` — inside the page's `flag list:` code block.

### 1.1 Verbatim check of S277 against the lane's own receipt

The quote is real and in the receipt:

```
$ cd LANE/.ufo/waves/round-38/fetch
$ python3 - <<'EOF'
d=open('S277.bin','rb').read()
for q in [b"There is no length prefix or newline.", b"[flags]/command [arguments]", b"[[BATCH]]"]:
    i=d.find(q); print(q, '->', i, 'line', d[:i].count(b'\n')+1 if i>=0 else None)
EOF
There is no length prefix or newline. -> 3703 line 84
[flags]/command [arguments] -> 3602 line 80
[[BATCH]] -> 3787 line 85
$ sha256sum S277.bin
ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6  S277.bin
```

**PASS** — the quote is verbatim, at `S277.bin:84`, sha256 matches the SOURCES row and the round-38 Gate line.

The full S277 grammar block (`S277.bin:77-86`), which is what the corpus paraphrases:

```
The request grammar, measured from the real client, is:

```text
[flags]/command [arguments]       hyprctl
command [arguments]               Quickshell dispatch
```

There is no length prefix or newline. `j` requests JSON. Batch requests
start with `[[BATCH]]` and use `;` separators.
```

Note the second line: `command [arguments]  Quickshell dispatch` — **no leading slash**. This is a claim the corpus does *not* restate, and it is falsified by upstream source: S158's `getReply` strips flags only `if (!request.starts_with("[[BATCH]]") && request.contains("/"))` (`S158.bin:2069`), then matches the remainder against registered command names. A slash-less `dispatch foo` therefore arrives with the literal text `dispatch foo` and would match the non-exact command `dispatch` only if the name were a prefix of the request — it is (`registerCommand(SHyprCtlCommand{"dispatch", false, dispatchRequest})`, `S158.bin:2036`), because non-exact commands are matched with `request.starts_with(cmd->name)` (`S158.bin:2113`). So the slash-less form works *by accident of prefix matching*, not by design. The corpus omits this nuance; it is not a defect in the S277 quote, but it is a place where the corpus's paraphrase ("reports the same") is looser than the source.

---

## 2. Independent source #1 — the wiki IPC page, current and three historical versions

Fetched 2026-10-25, all four return the *same* grammar sentence, so the grammar claim is stable across the whole version range the lane cares about.

| URL | bytes | sha256 (first 16) | "newline" count | "length prefix" count | `flag(s)` count |
|---|---|---|---|---|---|
| https://wiki.hypr.land/IPC/ | 243,981 | `58e726f89951a4a5` | 0 | 0 | 1 |
| https://wiki.hypr.land/0.41.0/IPC/ | 130,309 | — | 0 | 0 | 1 |
| https://wiki.hypr.land/0.54.0/IPC/ | 137,039 | — | 0 | 0 | 1 |
| https://wiki.hypr.land/0.56.0/IPC/ (= lane `S187.bin`) | 268,731 | — | 0 | 0 | 1 |

> **Quote (wiki.hypr.land/IPC/, accessed 2026-10-25, ≤25 words):** "basically, write `[flag(s)]/command args`"

Extraction, all four versions identical:

```
S187-0.56.0 -> 'basically, write [flag(s)]/command args . Note Hyprland '
current     -> 'basically, write [flag(s)]/command args . Note Hyprland '
```

**Verdict on this source:** confirms the **grammar** (`[flag(s)]/command args`) — verbatim, byte-identical across 0.41.0 / 0.54.0 / 0.56.0 / current. **Does NOT mention** "newline" or "length prefix" *at all* (0 occurrences in every version) — the upstream wiki never states the framing rule. **Does NOT publish a flag list** on this page (0 occurrences of `flag list`; the flag list lives on the separate *Using hyprctl* page, which is `S221`). The page revision string on the current page is `Last updated on <time datetime="2026-08-26T14:50:40.000Z"`.

This is the crux of the round's structure: **upstream documents the grammar but never the framing.** That is precisely why the lane reached for a community source, and why S277 is doing real work.

---

## 3. Independent source #2 — the host's own code (first-party, and the flag-list divergence)

### 3.1 Server side: S158 = `HyprCtl.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f`

The flag parser, `S158.bin:2062-2097`:

```
std::string CHyprCtl::getReply(std::string request) {
    ...
    // process flags for non-batch requests
    if (!request.starts_with("[[BATCH]]") && request.contains("/")) {
        long unsigned int sepIndex = 0;
        for (const auto& c : request) {
            if (c == '/') { // stop at separator
                break;
            }
            ...
            sepIndex++;

            if (c == 'j')
                format = eHyprCtlOutputFormat::FORMAT_JSON;
            else if (c == 'r')
                reloadAll = true;
            else if (c == 'a')
                m_currentRequestParams.all = true;
            else if (c == 'c')
                m_currentRequestParams.sysInfoConfig = true;
        }

        if (sepIndex < request.size())
            request = request.substr(sepIndex + 1); // remove flags and separator so we can compare the rest of the string
    }
```

**Socket-level flag alphabet at the host's own v0.56.2 = `{j, r, a, c}`.** No `i`. No `f`. (`f` is client-side `--follow`, handled in the hyprctl binary, and `i` is client-side `--instance`, likewise.)

### 3.2 Client side: S169 = `hyprctl/src/main.cpp` @ the same commit

`hyprctl/src/main.cpp:413-427` (byte-identical to the lane's held receipt, verified):

```
$ sha256sum hyprctl-main.cpp LANE/.ufo/waves/round-25/fetch/S169.bin
f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f  hyprctl-main.cpp
f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f  .../round-25/fetch/S169.bin
```

| line | code | meaning |
|---|---|---|
| 413-414 | `ARGS[i] == "-j"` → `fullArgs += "j"` | `j` → socket flag |
| 416-417 | `ARGS[i] == "-r"` → `fullArgs += "r"` | `r` → socket flag |
| 418-419 | `ARGS[i] == "-a"` → `fullArgs += "a"` | `a` → socket flag |
| 420-421 | `ARGS[i] == "-c" \|\| "--config"` → `fullArgs += "c"` | `c` → socket flag |
| 422-423 | `ARGS[i] == "-f" \|\| "--follow"` → `fullArgs += "f"` | `f` → client-side only |
| 425-426 | `ARGS[i] == "--batch"` → `fullRequest = "--batch "` | client-side only |
| 427-428 | `ARGS[i] == "--instance" \|\| "-i"` → `overrideInstance = ARGS[i]` | **`i` → client-side only; selects the socket path** |
| 480 | `fullRequest = fullArgs + "/" + fullRequest;` | **the wire form is literally `<flags>/<command>`** |
| 239 | `writeAll(SERVERSOCKET, arg)` | **the request bytes are written verbatim — no terminator, no length prefix** |
| 57-68 | `writeAll(fd, data)` loops `write(fd, data.data()+totalWritten, data.size()-totalWritten)` | writes exactly `data.size()` bytes — nothing appended |
| 347 | `std::string rq = "[[BATCH]]" + commands;` | `[[BATCH]]` prefix, first-party |

> **Quote (hyprctl/src/main.cpp @ efb50993, accessed 2026-10-25, ≤25 words):** `fullRequest = fullArgs + "/" + fullRequest;` — then `writeAll(SERVERSOCKET, arg)`, no terminator.

> **Quote (src/debug/HyprCtl.cpp @ efb50993, accessed 2026-10-25, ≤25 words):** `if (c == 'j') format = …FORMAT_JSON; else if (c == 'r') reloadAll = true; else if (c == 'a') …all = true; else if (c == 'c') …sysInfoConfig = true;`

### 3.3 F-1 — the flag-list divergence (finding, severity: medium)

`corpus/knowledge/hyprctl-flags-r28.md:15-16` says the published list is "the published flag vocabulary of the **request socket**". The wiki page it cites (`S221` = 0.56.0 *Using hyprctl*) publishes, verbatim (`S221.bin:3392-3397`):

```
flag list:
j -> output in JSON
i -> select instance (id or index in hyprctl instances)
r -> force state refresh after issuing commands (e.g. layout or rule changes)
```

Cross-checked against the **current** wiki page (`https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/`, 281,934 B, sha256 `24c3987dd95986ef306edf14804c4a959c5846d4a105d70bb1d58f6b78c6b468`, `Last updated on <time datetime="2026-08-26T14:50:40.000Z">`): **identical three-flag list**. So the *documentation* is stable and current — the corpus is right about what the docs say.

But three divergences from the **socket**:

1. **`i` is not a socket flag.** It is `hyprctl --instance/-i`, consumed at `hyprctl/src/main.cpp:427` and used at `:494-510` to pick the *instance signature* (hence the socket path). It never enters `fullArgs` and never appears in `fullRequest`. The server's parser has no `i` branch. The published list describes the **CLI**, not the socket.
2. **`a` and `c` are socket flags the published list omits.** `hyprctl -a` and `hyprctl -c/--config` both map to real server flags (`S158.bin:2090, 2092`). The wiki's `flag list:` block does not mention them. The hyprctl **man page** at the same commit (`docs/hyprctl.1.rst`) is worse still — it documents **only** `-j`.
3. The corpus's own §3 already flags the gap: *"The server-side handling of each flag was not re-read this round"* — and marks it `[UNK]`. S158 is **already in the round-38 fetch set** (`.ufo/waves/round-38/fetch/S158.bin`, 97,582 B), so this `[UNK]` is closable from bytes the lane already holds. It was not.

**What this does and does not falsify.** It does not falsify the *documented* claim — the docs really do publish `j`, `i`, `r`, and the corpus quotes them accurately. It falsifies the *gloss*: calling that list "the flag vocabulary of the request socket" and inferring from `i` that "**`i` chooses which compositor instance answers**" a socket-level behaviour. The instance choice happens **client-side, before the socket is opened**. And the published list is **not exhaustive** for the socket (`a`, `c` missing), so a reader who takes the entry's framing would under-count the socket's flag alphabet by two flags while over-counting it by one.

Recommendation (for the owning reviewer, not applied by me — read-only seat): `hyprctl-flags-r28.md` §1 should distinguish the **CLI flag list** (what `S221` publishes: `j`, `i`, `r`) from the **socket flag alphabet** (what `S158` parses at v0.56.2: `j`, `r`, `a`, `c`), and §3's `[UNK]` should be closed from `S158.bin:2069-2097` + `S169.bin:413-427, 480`.

### 3.4 Batch syntax — first-party corroboration of S277's `[[BATCH]]` claim

`S158.bin:2041`: `registerCommand(SHyprCtlCommand{"[[BATCH]]", false, dispatchBatch});`
`S158.bin:1309-1332`: `dispatchBatch` does `request = request.substr(9);` (strips the 9-byte `[[BATCH]]`), splits on `;` while tracking `[`/`]` bracket depth so a `;` inside `[]` is not a separator, and joins the replies with `DELIMITER = "\n\n\n"`.
`hyprctl/src/main.cpp:339-349`: `batchRequest` builds `std::string rq = "[[BATCH]]" + commands;` and, under `-j`, rewrites `;\s*` → `;j/`.

**PASS** — S277's "`[[BATCH]]` batch requests with `;` separators" is confirmed by first-party source at the host's own commit, independently of S277.

---

## 4. Independent sources #3-#8 — community re-implementations (the actual "second voice")

Six independent third-party Hyprland IPC client implementations were opened. All six are **code**, not prose; none enumerates the flag list; none states the framing rule in words. Each is a genuinely separate codebase from S277's chonkstep and from each other.

### 4.1 `hyprland-rs` — hyprland-community/hyprland-rs (Rust), default branch `master`

URL: https://github.com/hyprland-community/hyprland-rs — accessed 2026-10-25.

`src/shared.rs` (8,348 B, sha256 `37fe6bba4d527f25aed51fba903f4b28f285c14a7aec272bde33919991ad52c1`):

```rust
match &self.flag {
    CommandFlag::JSON => write!(f, "j/{}", &self.data),   // :234
    CommandFlag::Empty => write!(f, "/{}", &self.data),    // :235
}
```

`src/instance.rs` (5,748 B, sha256 `0e0423b7819c002ae2b0c943060d4ff3897761116ea13ec62cef7bc6764283cc`):

```rust
pub(crate) fn write_to_socket(&self, content: CommandContent) -> crate::Result<String> {
    let mut stream = std::os::unix::net::UnixStream::connect(&self.stream)?;
    stream.write_all(&content.as_bytes())?;                 // :69
    let mut response = Vec::new();
    stream.read_to_end(&mut response)?;                     // :71
```

> **Quote (hyprland-rs src/shared.rs, accessed 2026-10-25, ≤25 words):** `CommandFlag::JSON => write!(f, "j/{}", &self.data), CommandFlag::Empty => write!(f, "/{}", &self.data),`

**Verdict:** confirms the **grammar** — `j/` prefix and `/` separator, independently of the wiki. Confirms **no length prefix / no newline** by construction (`write_all` of exactly the encoded command bytes; read to EOF). Its flag enum has only `JSON` and `Empty` — it does **not** implement `r`, `a`, `c`, or `i`, so it cannot corroborate the flag list.

### 4.2 `pyprland` — hyprland-community/pyprland (Python), default branch `main`

URL: https://github.com/hyprland-community/pyprland — accessed 2026-10-25.

`pyprland/adapters/hyprland.py` (7,562 B, sha256 `08cb8d1134056778148b50200271a19650984a797f4ca2d5841c333c0d2392c1`):

```python
ctl_writer.write(f"[[BATCH]] {' ; '.join(self._format_command(command, base_command))}".encode())  # :91
ctl_writer.write(f"/{base_command} {command}".encode())                                          # :94
ret = await get_response(f"-j/{command}".encode(), log)                                          # :118
ctl_writer.write(f"[[BATCH]] {' ; '.join(formatted_cmds)}".encode())                               # :173
```

`pyprland/ipc.py` (5,721 B, sha256 `9717f6050fc3ddd41f7af7165358587affb01b3805e7d0c987eba78e46c582a2`):

```python
async with hyprctl_connection(logger) as (reader, writer):
    writer.write(command)          # :163  — raw bytes, no terminator
    await writer.drain()
    reader_data = await reader.read()
```

> **Quote (pyprland adapters/hyprland.py, accessed 2026-10-25, ≤25 words):** `ctl_writer.write(f"/{base_command} {command}".encode())` … `ctl_writer.write(f"[[BATCH]] {' ; '.join(...)}".encode())`

**Verdict:** confirms the **grammar** (`/command args`, `[[BATCH]]`, `;` separators — the separator is `' ; '` with spaces, matching the client's `--batch` doc) and **no newline/length prefix** by construction. Divergence worth noting: pyprland sends **`-j/command`** (hyprctl-style dash) on the wire, not `j/command`. The server's loop only inspects characters before the first `/` and reacts to `j` — so `-j/monitors` still selects JSON (the `-` is simply an unrecognised char that is skipped by the `else if` chain and the `sepIndex` still advances past it). It works, but it is not the documented `j/` form, and it is a *different* byte string from what hyprctl sends. **Corroborates the grammar; does not corroborate the flag list** (no flag enumeration anywhere in the file).

### 4.3 `morr0ne/hyprland-ipc` — Rust crate, `main`

URL: https://github.com/morr0ne/hyprland-ipc — accessed 2026-10-25. `src/dispatch.rs` (3,238 B, sha256 `63e9a3e35138c04dc1fd62f85010d694aa70a5c3d134ada3a12ac5501b9ed390`):

```rust
socket.write_all(command.as_bytes()).await?;                        // :26, :42
self.call_command_json("j/clients").await                          // :52
self.call_command(&format!("/dispatch togglefloating {window}"))    // :57
self.call_command("/dispatch togglefloating").await                 // :60
```

> **Quote (morr0ne/hyprland-ipc src/dispatch.rs, accessed 2026-10-25, ≤25 words):** `self.call_command_json("j/clients").await` … `socket.write_all(command.as_bytes()).await?;`

**Verdict:** confirms the **grammar** (`j/` and `/dispatch args`) and **no newline/length prefix**. Note: this crate hardcodes `/tmp/hypr/{his}/.socket.sock` (`src/dispatch.rs:21`) — the pre-`$XDG_RUNTIME_DIR` path — so it is stale relative to this host, and its authority on the *socket path* is nil. Irrelevant to the grammar question, relevant to anyone tempted to cite it for transport.

### 4.4 `BlueManCZ/hyprland-socket` — typed Python library, `main`

URL: https://github.com/BlueManCZ/hyprland-socket — accessed 2026-10-25.

`src/hyprland_socket/_socket.py` (1,882 B, sha256 `a3e3416800852334ad00fce18fc861861ce43f5c029573a0a29b4384a79d6342`):

```python
sock.connect(_socket_path())
sock.sendall(command.encode())          # :48 — raw bytes, no terminator
```

`src/hyprland_socket/commands.py` (sha256 `d40fb3823b8119c165c99f33087488adff5687721f6dc33c2382645648c90a21`):

```python
_BATCH_SEPARATOR = "\n\n\n"            # :12 — "Hyprland separates batch command results with triple newlines"
response = _send(f"j/{command}")       # :17
response = _send(f"/keyword {key} {_format_value(value)}")   # :60
```

> **Quote (BlueManCZ/hyprland-socket src/hyprland_socket/commands.py, accessed 2026-10-25, ≤25 words):** `_BATCH_SEPARATOR = "\n\n\n"` … "Hyprland separates batch command results with triple newlines."

**Verdict:** confirms the **grammar** (`j/`, `/keyword args`) and **no newline/length prefix** on the request side. Independently confirms the batch **reply** separator `"\n\n\n"` — matching `S158.bin:1314` `const std::string DELIMITER = "\n\n\n";` — from a community codebase. Its README (4,057 B, sha256 `6ec37afd9e695c59372875f81c193143be14281df5709e18c90b9263a410f5f7`) states the lifecycle rule ("Hyprland processes command-socket connections synchronously — an unclosed …") but **not** the framing rule; its "Socket lifecycle" section is the only prose.

### 4.5 `Quickshell` — outfoxxed/quickshell (C++/Qt), branch `master`

URL: https://github.com/outfoxxed/quickshell — accessed 2026-10-25. `src/wayland/hyprland/ipc/connection.cpp` (29,404 B, sha256 `334f2df04ff0634be3a83966cc25fc3d6a2cc540437cdcd7c04af9d6ee75b7c4`):

```cpp
this->makeRequest("j/status", [&, this](bool success, QByteArray resp) {   // :89
...
requestSocket->write(request);          // :198 — raw bytes, no terminator
requestSocket->flush();
...
void HyprlandIpc::dispatch(const QString& request) {
    this->makeRequest(
        ("dispatch " + request).toUtf8(),                                  // :218
```

> **Quote (Quickshell src/wayland/hyprland/ipc/connection.cpp, accessed 2026-10-25, ≤25 words):** `this->makeRequest("j/status", …` … `("dispatch " + request).toUtf8(),`

**Verdict:** confirms the **grammar** (`j/status`, `dispatch <args>`) and **no newline/length prefix**. Note the dispatch form is `dispatch <args>` — **no leading slash** — which corroborates S277's second grammar line (`command [arguments]  Quickshell dispatch`) as a *real* client behaviour, not a typo. And it is exactly the case §1.1 flagged: a slash-less request only works because `dispatch` is registered non-exact and matched by `starts_with`. A slash-less `version` would **fail** (exact match, `cmd->name == request`). So S277's grammar table is describing two genuinely different request shapes, and the corpus's paraphrase drops the second one entirely.

### 4.6 `gtkshell` — dawsers/gtkshell (C++/GTK4), branch `master`

URL: https://github.com/dawsers/gtkshell — accessed 2026-10-25. `hyprland.cpp` (sha256 `4154f1d9ca71d0a36d4396b2819000fc229699ddb4467872a72c167bc8ce711b`):

```cpp
json json_workspaces = json::parse(message("j/workspaces"));            // :83
json json_activewindow = json::parse(message("j/activewindow"));        // :98
bool Hyprland::write_socket(const Glib::ustring &message, ...)          // :164
    connection->get_output_stream()->write(message, nullptr);           // :170
```

> **Quote (gtkshell hyprland.cpp, accessed 2026-10-25, ≤25 words):** `json json_workspaces = json::parse(message("j/workspaces"));`

**Verdict:** confirms the **grammar** and **no newline/length prefix** by construction.

### 4.7 `caelestia-dots/cli` and `waybar` — attempted, blocked

- `caelestia-dots/cli` `src/caelestia/cli/hypr.py` — **404** (path does not exist at `main`); GitHub API rate-limited (HTTP 403) before the tree could be listed. Not counted.
- `Alexays/Waybar` `src/modules/hyprland/HyprlandIPC.cpp` — **404** on `master` and `main`; the module path has moved. GitHub API rate-limited before the tree could be listed. Not counted.
- `waycrate/hypridle` / `hyprwm/hypridle` — **404** as a `waycrate/` path; the real repo is `hyprwm/hypridle`. Fetched `src/main.cpp` and `src/core/Hypridle.cpp`: **hypridle does not use the IPC socket at all** — `grep -c -i "socket.sock\|hyprctl\|dispatch"` returns 0 for `main.cpp` and 4 for `Hypridle.cpp`, and those 4 hits are all `wl_display_dispatch*` (Wayland dispatch, unrelated). **hypridle is not a source on the request grammar.** It was named in the task prompt as a candidate; it is a dead end and should not be cited.

### 4.8 Summary table — what each community source actually confirms

| Source | URL | `[flags]/command args` | no length prefix / newline | flag list | `[[BATCH]]` + `;` |
|---|---|---|---|---|---|
| chonkstep (**S277**) | raw.githubusercontent.com/…/chonkstep/…/docs/hyprland-ipc.md | ✅ prose + measured | ✅ **prose (unique)** | ❌ | ✅ prose |
| hyprland-rs | github.com/hyprland-community/hyprland-rs | ✅ code (`j/`, `/`) | ✅ code (`write_all`) | ❌ | ❌ |
| pyprland | github.com/hyprland-community/pyprland | ✅ code (`/`, `[[BATCH]]`) | ✅ code (`write`) | ❌ | ✅ code |
| morr0ne/hyprland-ipc | github.com/morr0ne/hyprland-ipc | ✅ code (`j/`, `/dispatch`) | ✅ code (`write_all`) | ❌ | ❌ |
| BlueManCZ/hyprland-socket | github.com/BlueManCZ/hyprland-socket | ✅ code (`j/`, `/keyword`) | ✅ code (`sendall`) | ❌ | ✅ code (`\n\n\n`) |
| Quickshell | github.com/outfoxxed/quickshell | ✅ code (`j/status`) | ✅ code (`write`) | ❌ | ❌ |
| gtkshell | github.com/dawsers/gtkshell | ✅ code (`j/…`) | ✅ code (`write`) | ❌ | ❌ |

**Every community source confirms the grammar and the framing-by-construction. Not one confirms the flag list.**

---

## 5. Prose-level hunt — is any *other* community voice stating the framing rule in words?

Searched, with negative results recorded so the negative is evidenced rather than assumed:

| Source searched | URL | result |
|---|---|---|
| r/hyprland "IPC broken?" (2025-09) | reddit.com/r/hyprland/comments/1nroft7/ipc_broken/ | **BLOCKED** — `403`, "You've been blocked by network security"; `.json` API also 403 (browser UA, `api.reddit.com`, `old.reddit.com`, and the `read` reader all fail). Could not be quoted. |
| wayland-ricing-guide ch.88 | raw.githubusercontent.com/jreuben11/wayland-ricing-guide/main/part-06-advanced/ch88-hyprland-ipc-scripting.md (11,486 B) | Uses `hyprctl` and `socat` for the **event** socket only; `socket.sock` appears 1×, `flag list` 0×, no framing prose. Does not address request framing. |
| ArchWiki Hyprland | wiki.archlinux.org/title/Hyprland (124,024 B) | "newline" 0×, "length prefix" 0×, "flag(s)" 0×, "j/" 0×. Only "2 UNIX Sockets" prose. |
| Hyprland wiki FAQ | wiki.hypr.land/FAQ/ | "newline" 0×, "length prefix" 0×, "socket.sock" 0×. |
| petronellatech setup guide | petronellatech.com/blog/hyprland-setup-guide-install-ubuntu-2026/ | "newline" 0×, "length prefix" 0×, "socket.sock" 0×. |
| rafaelcosquiere notes | rafaelcosquiere.com/en/notes/my-arch-linux-installation-and-configuration-notes/ | same, all 0×. |
| Astal Hyprland library guide | aylur.github.io/astal/guide/libraries/hyprland | describes monitoring only; no request framing. |
| `hyprland-rs` README | github.com/hyprland-community/hyprland-rs | "An unofficial rust wrapper for Hyprland's IPC" — no framing prose. |
| `pyprland` README | github.com/hyprland-community/pyprland | no framing prose. |
| `BlueManCZ/hyprland-socket` README | github.com/BlueManCZ/hyprland-socket | lifecycle prose only; no framing prose. |
| `OpulentiaAI/cua-spaces` v3 protocol | github.com/OpulentiaAI/cua-spaces/…/cua-input-v3.md | A **private plugin** wire protocol, not Hyprland IPC. "Packets contain printable ASCII fields separated by exactly one space, with no newline." — true, but about a different socket; must not be cited as Hyprland IPC. |
| `MasonRhodesDev/hypr-ipc` | github.com/MasonRhodesDev/hypr-ipc | `src/lib.rs:17`: `/// Command socket filename. Prefer `hyprctl` over framing this yourself.` — a client that deliberately avoids the framing question. Not a corroboration. |
| `waybar` Hyprland module | github.com/Alexays/Waybar | 404 at the historic path; not retrieved. |

**Conclusion for the assigned verdict:** on the *framing* claim ("no length prefix or newline"), **S277 is the only non-first-party voice in prose that could be found** — every other corroboration is a client implementation, and one high-signal candidate (the r/hyprland thread that search engines quote for exactly this point) is behind a network block and could not be opened. On the *grammar* claim, S277 is **not** the only non-first-party voice: five other independent community codebases confirm `[flags]/command args`.

So the honest answer to "does S277's community-tier grammar corroborate independently, or is it the only non-first-party voice?" is **split**:

- **Grammar — corroborated independently.** Six community implementations (S277 + five more) plus four first-party/host-byte sources (wiki ×4 versions, hyprctl client, HyprCtl server) agree. S277 is *redundant* for the grammar, not load-bearing.
- **Framing — S277 is the only non-first-party *prose* voice**, and it is **not redundant**: no wiki version says it, and no other community prose found says it. Its value is in being the only source that states the rule in words.
- **Flag list — corroborated by nobody outside first-party docs**, and the first-party docs are *about the CLI*, not the socket (F-1).

**This means the round's coverage claim is understated in one place and overstated in another.** The corpus credits S277 as the sole community grammar corroboration (it is not — five more exist); and it credits S221 as publishing the request socket's flag vocabulary (it publishes the CLI's, and the socket's alphabet differs by three flags).

---

## 6. F-2 — S277's citation pin is dead (provenance finding, severity: medium)

`corpus/SOURCES.md:223` URL:
`https://raw.githubusercontent.com/chriskearney/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md`
`corpus/knowledge/request-socket-live-bound-r8.md:9` names the same commit under `iconidentify/chonkstep`.

Probes run 2026-10-25:

```
$ curl -sSL -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/chriskearney/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md
404
$ curl -sSL -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/iconidentify/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md
404
$ git ls-remote https://github.com/chriskearney/chonkstep.git | grep -c 707cf7f8b39d0b4e2cba46d0a2559b562d8821ce
0                       # 192 branch refs, none at that SHA
$ git ls-remote https://github.com/chriskearney/chonkstep.git 'refs/pull/*' | grep -c 707cf7f8…
0                       # 88 PR refs, none at that SHA
$ D=$(mktemp -d) && git -C "$D" init -q && git -C "$D" remote add o https://github.com/chriskearney/chonkstep.git \
  && git -C "$D" fetch --depth 1 origin 707cf7f8b39d0b4e2cba46d0a2559b562d8821ce
fatal: remote error: upload-pack: not our ref 707cf7f8b39d0b4e2cba46d0a2559b562d8821ce
```

The **content** is still live and **byte-identical** to the lane's receipt:

```
$ curl -sSL https://raw.githubusercontent.com/chriskearney/chonkstep/main/docs/hyprland-ipc.md -o chonk-main.md
$ sha256sum chonk-main.md
ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6  chonk-main.md
$ python3 -c "print(open('chonk-main.md','rb').read()==open('LANE/.ufo/waves/round-38/fetch/S277.bin','rb').read())"
True
```

`main` HEAD = `c37fbe3e439dc27db9ce8176546febb58680dfc5` for both owner names; `github.com/iconidentify/chonkstep` 301s to `github.com/chriskearney/chonkstep`.

**Assessment.** The *evidence* is sound today — the receipt's bytes are exactly what `main` serves, and the sha256 in the SOURCES row and the round-38 Gate line still matches. The *citation* is not: the pinned SHA is unreachably dead (likely a rewritten/force-pushed history), and the two corpus locations cite the same commit under **two different owner names**, so a reader following either will get a 404. A `recheck: 90d` row whose URL 404s is a recheck that cannot be executed. This is a citation-hygiene finding, not a content finding: the S277 claim itself survives.

---

## 7. Exact commands run (reproduction)

All under `/tmp/mado38-ScoutGrammar/` (scratch). LANE was read-only throughout.

```bash
# 1. wiki IPC page, current + 3 historical versions (grammar stability)
for v in "" 0.41.0 0.54.0 0.56.0; do
  curl -sSL --max-time 40 "https://wiki.hypr.land/${v:+$v/}IPC/" -o wiki-ipc-${v:-current}.html
done
# extract + count "newline" / "length prefix" / "flag(s)" in the tag-stripped text

# 2. current Using-hyprctl page (the flag list)
curl -sSL --max-time 40 https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/ -o wiki-hyprctl-current.html

# 3. community re-implementations (raw files)
curl -sSL https://raw.githubusercontent.com/hyprland-community/hyprland-rs/master/src/{shared.rs,instance.rs}
curl -sSL https://raw.githubusercontent.com/hyprland-community/pyprland/main/pyprland/{ipc.py,adapters/hyprland.py}
curl -sSL https://raw.githubusercontent.com/morr0ne/hyprland-ipc/main/src/dispatch.rs
curl -sSL https://raw.githubusercontent.com/BlueManCZ/hyprland-socket/main/src/hyprland_socket/{_socket.py,commands.py}
curl -sSL https://raw.githubusercontent.com/outfoxxed/quickshell/master/src/wayland/hyprland/ipc/connection.cpp
curl -sSL https://raw.githubusercontent.com/dawsers/gtkshell/master/hyprland.cpp

# 4. first-party host bytes (same commit the lane already holds)
curl -sSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/hyprctl/src/main.cpp
curl -sSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/docs/hyprctl.1.rst
curl -sSL https://raw.githubusercontent.com/hyprwm/hypridle/main/src/{main.cpp,core/Hypridle.cpp}

# 5. S277 pin reachability (scratch repo only)
D=$(mktemp -d) && git -C "$D" init -q && git -C "$D" remote add o https://github.com/chriskearney/chonkstep.git \
  && git -C "$D" fetch --depth 1 origin 707cf7f8b39d0b4e2cba46d0a2559b562d8821ce
git ls-remote https://github.com/chriskearney/chonkstep.git | grep -c 707cf7f8…

# 6. verbatim/digest checks against lane receipts
python3 -c "…find(b'There is no length prefix or newline.')…"
sha256sum LANE/.ufo/waves/round-38/fetch/S277.bin LANE/.ufo/waves/round-25/fetch/S169.bin
```

**Tool installs: none.** No pacman transaction, no `uv tool`, no `cargo`/`npm`. Nothing was needed beyond the preinstalled `curl`, `git`, `python3`.

---

## 8. PASS / FAIL per item

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | S277 quote verbatim in lane receipt | **PASS** | `S277.bin:84`; sha256 `ff561fe0…781e6` matches SOURCES + Gate |
| 2 | `[flag(s)]/command args` confirmed by first-party, stable across versions | **PASS** | wiki IPC current/0.56.0/0.54.0/0.41.0, byte-identical sentence |
| 3 | "no length prefix or newline" confirmed by first-party code | **PASS** | `hyprctl/src/main.cpp:480` + `:239` + `writeAll:57-68`; server `S158.bin:2271-2279` accumulates raw bytes, no framing |
| 4 | Grammar confirmed by ≥2 independent community implementations | **PASS** | hyprland-rs `shared.rs:234-235`; pyprland `hyprland.py:94`; morr0ne `dispatch.rs:52,57`; BlueManCZ `commands.py:17,60`; Quickshell `connection.cpp:89`; gtkshell `hyprland.cpp:83` |
| 5 | `[[BATCH]]` + `;` separators confirmed by first-party | **PASS** | `S158.bin:2041,1309-1332` (`substr(9)`, `;` split, `"\n\n\n"` delimiter); `hyprctl main.cpp:347` |
| 6 | Flag list `j`,`i`,`r` corroborated by any independent source | **FAIL** | no community source enumerates flags; 0 of 6 |
| 7 | Published flag list == socket flag alphabet | **FAIL** | server parses `{j,r,a,c}` (`S158.bin:2085-2092`); `i` is client-side only (`hyprctl main.cpp:427`); `a`,`c` undocumented; man page lists only `-j` |
| 8 | Community prose voice for the framing rule beyond S277 | **FAIL (none found)** | 12 sources searched, 0 prose hits; the strongest candidate (r/hyprland "IPC broken?") is 403-blocked and unquotable |
| 9 | S277 cited URL resolves at its pinned SHA | **FAIL** | 404 raw (both owners); SHA absent from 192 branch + 88 PR refs; `fetch` → `not our ref` |
| 10 | S277 content still reproducible | **PASS** | `main` bytes sha256 `ff561fe0…781e6` — byte-identical to receipt |
| 11 | hypridle usable as an IPC-grammar source | **FAIL (dead end)** | `hypridle src/main.cpp` 0 hits; `Hypridle.cpp` 4 hits all `wl_display_dispatch*` |
| 12 | No LANE production file modified | **PASS** | only `read`/`bash` read verbs against LANE; writes confined to `/tmp/mado38-ScoutGrammar/` and this report |

---

## 9. Remaining unknowns (stated, not papered over)

1. **The r/hyprland "IPC broken?" thread** (2025-09-27, `reddit.com/r/hyprland/comments/1nroft7/ipc_broken/`) — the search engines consistently attribute to it the maintainer advice to send `/workspaces` / `j/workspaces` and to drop trailing characters such as newlines. I could **not** open it: every route returned HTTP 403 ("You've been blocked by network security"). **Unresolved.** If a reviewer has Reddit access, that thread would be the natural second *prose* voice on the framing rule and would close item 8. Do not cite it from a search-engine summary.
2. **`refs/pull/*` beyond the first 88** — `git ls-remote 'refs/pull/*'` returned 88 PR refs; GitHub's API rate limit (HTTP 403) blocked a full listing, so a further-deleted PR ref pointing at the pinned SHA cannot be excluded by the ls-remote sweep. The `upload-pack: not our ref` error is the stronger signal that the object is gone from the server's reachable set, but the SHA's history (force-push vs. repo migration) is not established.
3. **The wiki's git-history source of the `flag list:` block** — whether the three-flag list was ever different (e.g. whether `a`/`c` were published and dropped) was not checked; the 0.41.0 page fetched here is the IPC page, not the *Using hyprctl* page, so no historical flag-list comparison was made.
4. **Whether upstream ever documents the request framing in prose** — the wiki was checked at 4 versions of the IPC page plus the FAQ and the 0.56.0 *Using hyprctl* page; a full-history sweep of `hyprland-wiki` for "newline"/"length prefix" was not performed (the git-history clone of the wiki was not attempted, to bound the seat's footprint).

---

## 10. Recommendations (for the owning reviewer — read-only seat, nothing applied)

1. **`hyprctl-flags-r28.md` §1/§3 (F-1, highest value).** Split the published *CLI* flag list (`S221`: `j`, `i`, `r`) from the *socket* flag alphabet (`S158.bin:2085-2092`: `j`, `r`, `a`, `c`), and close the §3 `[UNK]` from bytes already held (`S158.bin:2069-2097`, `S169.bin:413-427,480`). The current phrasing — "the published flag vocabulary of the request socket" plus the inference "`i` chooses which compositor instance answers" — misattributes a client-side CLI option to the socket and under-counts the socket's flags by two.
2. **`SOURCES.md:223` / `request-socket-live-bound-r8.md:9` (F-2).** Re-point the S277 row at a reachable URL — `https://raw.githubusercontent.com/chriskearney/chonkstep/main/docs/hyprland-ipc.md` (sha256 `ff561fe0…781e6`, verified byte-identical to the held receipt) — or at `main`'s tree SHA `c37fbe3e439dc27db9ce8176546febb58680dfc5`; and make the owner name consistent between the two locations (`chriskearney` and `iconidentify` are the same repo; `iconidentify` redirects).
3. **`request-socket-live-bound-r8.md` §2 (coverage, cheap win).** The corpus's "community-tier cross-check" framing implies S277 is the only community voice. It is not: `hyprland-rs`, `pyprland`, `morr0ne/hyprland-ipc`, `BlueManCZ/hyprland-socket`, `Quickshell`, and `gtkshell` all independently confirm `[flags]/command args` and frameless writes. S277's unique contribution is the *prose* statement of the framing rule. Recording that distinction would make the round's coverage claim accurate rather than merely defensible.
4. **`request-socket-live-bound-r8.md` §2 (small fidelity point).** S277's grammar table has **two** rows, and the second (`command [arguments]  Quickshell dispatch`, no leading slash) is dropped by the paraphrase. It is corroborated by Quickshell's own source (`connection.cpp:218` sends `"dispatch " + request`) — and it only works because `dispatch` is registered non-exact and matched by `starts_with` (`S158.bin:2036,2113`); a slash-less `version` would fail. If the entry quotes the table, it should carry that caveat.
5. **Do not cite** `hypridle` for anything IPC-grammar (item 11), `morr0ne/hyprland-ipc` for the socket path (it hardcodes `/tmp/hypr/…`, `dispatch.rs:21`), or the `cua-input-v3` protocol doc for Hyprland IPC (it is a private plugin wire).

---

*Report written 2026-10-25 by `L1Mado38.ScoutGrammar`. Read-only on all lane production files; scratch confined to `/tmp/mado38-ScoutGrammar/` and `mktemp -d` clones. No tools installed. No socket connected. No `git` write in LANE.*
