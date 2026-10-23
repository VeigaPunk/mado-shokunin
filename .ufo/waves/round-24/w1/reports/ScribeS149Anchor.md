# Scribe S149 Anchor

Scope: routed r23 defect 5, reopening foot wiki `Home.md` at commit `2475351ace3c8a618a3f2b8a7a486e987d125e07` and preparing the lesson-24 correction. No product file was edited.

## Behavior and findings

The pinned `Home.md` blob is 32,739 bytes with `sha256:78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7`. The extracted blob has 1,047 lines. Its FAQ text is:

- line 1013: `Restart foot. If you are running in server mode, you **must**`
- line 1014: `restart the server. There is no way to dynamically reload the`
- line 1015: `configuration.`

Therefore the exact sentence “There is no way to dynamically reload the configuration.” spans **`:1014-1015`** in this blob. The task's expected span `:1013-1014` conflicts with the reopened bytes: line 1013 is the preceding sentence, and the final word of the quoted sentence is on line 1015. The earlier spotcheck at `corpus/lessons/round-23-verifier-spotcheck.md:106-109` says the quote wraps across `:1013-1014`; the source bytes do not support that span.

### Draft lesson-24 correction text

> Routed defect 5 / S149 anchor correction: In the pinned foot wiki `Home.md` blob at commit `2475351ace3c8a618a3f2b8a7a486e987d125e07` (`sha256:78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7`, 32,739 B), “There is no way to dynamically reload the configuration.” begins on line 1014 and ends on line 1015. Its complete span is `:1014-1015`, not `:1014` or `:1013-1014`. Leave the existing `corpus/SOURCES.md` S149 anchor cell unchanged; this lesson records the correction append-only.

## Commands and gates

1. `timeout 120 git clone https://codeberg.org/dnkl/foot.wiki.git /fast/scratch/hyaku/mado-r24/footwiki`
   - Outcome: clone completed; output was `Cloning into '/fast/scratch/hyaku/mado-r24/footwiki'...`.
2. `timeout 15 sh -c 'git -C /fast/scratch/hyaku/mado-r24/footwiki show 2475351ace3c8a618a3f2b8a7a486e987d125e07:Home.md > /fast/scratch/hyaku/mado-r24/footwiki/Home-2475351.md && sha256sum /fast/scratch/hyaku/mado-r24/footwiki/Home-2475351.md && wc -c < /fast/scratch/hyaku/mado-r24/footwiki/Home-2475351.md && wc -l < /fast/scratch/hyaku/mado-r24/footwiki/Home-2475351.md'`
   - Outcome: `78bd64dc27cff31a668cd3a0c58391905b9967e51eec5c0a309fe5e7035a5ff7  /fast/scratch/hyaku/mado-r24/footwiki/Home-2475351.md`; `32739`; `1047`.
3. `timeout 30 curl -fsSL https://codeberg.org/dnkl/foot.wiki/raw/commit/2475351ace3c8a618a3f2b8a7a486e987d125e07/Home.md -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/ScribeS149Anchor-1.bin`
   - Outcome: failed with curl exit 22, `curl: (22) The requested URL returned error: 404`; no fetch artifact was present at that path. The pinned blob was reopened using the requested clone and `git show`, not the raw HTTP endpoint. The `src` route was not tested in this seat.
4. Read and searched the extracted blob at lines `1011-1017`; both the raw line view and line-numbered search placed the sentence across lines 1014-1015.

The reopened hash and byte count match the requested values. The requested `:1013-1014` span did not pass against the pinned blob. The existing S149 row in `corpus/SOURCES.md` was read and left unchanged; its full anchor cell is `Home.md:1011-1015` and includes the FAQ heading/context.

## Gates, surfaces, and limits

- **Passed:** pinned commit blob is readable; SHA-256 and byte count match; sentence line span determined from the blob.
- **Conflict:** expected `:1013-1014` is inconsistent with the actual bytes; correction draft uses `:1014-1015`.
- **Touched surfaces:** created the requested report; created the clone and extracted blob under `/fast/scratch/hyaku/mado-r24/` for read-only inspection.
- **Not changed:** `corpus/SOURCES.md`, lesson files, product code, host configuration, compositor state, services, or packages. No checks or counters outside this scoped source re-open were run.
- **Known limit:** pinned raw Codeberg fetch returned 404; source verification for this task relies on the cloned repository's pinned git blob. No tool was installed or updated.

## Artifact paths

- Report: `.ufo/waves/round-24/w1/reports/ScribeS149Anchor.md`
- Clone: `/fast/scratch/hyaku/mado-r24/footwiki`
- Extracted blob: `/fast/scratch/hyaku/mado-r24/footwiki/Home-2475351.md`
- Failed raw-fetch destination: `.ufo/waves/round-24/fetch/w1/ScribeS149Anchor-1.bin` (not created)

**Verdict:** blob identity verified; the requested `:1013-1014` span is contradicted by the pinned bytes, which place the quoted sentence at `:1014-1015`. The source row remains untouched.
