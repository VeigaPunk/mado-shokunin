#!/usr/bin/env python3
"""MutEntryQuotes: single-token mutation sweep of the round-41 DATA bytes,
scored by the frozen v2 C2 counter run from the scratch clone."""
import json, os, re, subprocess, sys

ROOT = "/tmp/mutentryq"
CLONE = os.path.join(ROOT, "clone")
PRI = os.path.join(ROOT, "pristine")
OUT = os.path.join(ROOT, "muts")
DATA = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
BASE = "ab2bfaab661c846d1de9d58c01651cd156a13949"
FILES = {
    "entry": "corpus/knowledge/hyprland-focus-grab-r41.md",
    "sources": "corpus/SOURCES.md",
    "lesson": "corpus/lessons/round-41.md",
    "readme": "corpus/README.md",
}

E = "entry"; S = "sources"; L = "lesson"; R = "readme"

def ed(anchor, old, new):
    return {"anchor": anchor, "old": old, "new": new}

MUTS = [
 # ---- entry: prose numbers that are not quotes/locators/class-counts/versions/dates/pids
 dict(id="E01", file=E, cls="prose-number", what="header 'Round: 41.' -> 'Round: 42.'",
      edits=[ed("Lane: mado-shokunin. Round: 41.", "Round: 41.", "Round: 42.")]),
 dict(id="E02", file=E, cls="prose-number", what="slice-session adverts 15 -> 16 (checkable vs journal)",
      edits=[ed("are a lower bound", "its 15 adverts", "its 16 adverts")]),
 dict(id="E03", file=E, cls="prose-number", what="census bullet 'two portal sessions' -> 'three'",
      edits=[ed("The census is one host, one day", "two portal sessions", "three portal sessions")]),
 dict(id="E04", file=E, cls="prose-number", what="bind-branch count 'ten named branches' -> 'nine' (checkable vs receipt)",
      edits=[ed("a fixed set of ten named branches", "ten named branches", "nine named branches")]),
 dict(id="E05", file=E, cls="prose-number", what="grep exit code 'exits 1' -> 'exits 2' (checkable vs receipt)",
      edits=[ed("exits 1 - the string does not occur", "exits 1", "exits 2")]),
 dict(id="E06", file=E, cls="prose-number", what="'occurs exactly once' -> 'exactly twice' (checkable vs journal)",
      edits=[ed("occurs exactly once, on the advert line", "exactly once", "exactly twice")]),
 dict(id="E07", file=E, cls="prose-number", what="latest-session distinct names 63 -> 62 (checkable vs census/journal)",
      edits=[ed("which is the only session that can be compared", "63 distinct names", "62 distinct names")]),
 dict(id="E08", file=E, cls="prose-number", what="first-session adverts 'with 15 adverts' -> '14'",
      edits=[ed("opens mid-stream at 13:16:45", "with 15 adverts", "with 14 adverts")]),
 dict(id="E09", file=E, cls="scalar-recheck", what="entry recheck 90d -> 95d (any \\d+d passes)",
      edits=[ed("recheck: 90d - re-pull", "90d", "95d")]),
 dict(id="E10", file=E, cls="prose-sectionrefs", what="assimilated-from 'sections 1, 2 and 4' -> 'and 5'",
      edits=[ed("assimilated-from:", "sections 1, 2 and 4;", "sections 1, 2 and 5;")]),
 # ---- entry: OBS -> INF flips
 dict(id="E11", file=E, cls="obs-to-inf", what="S281 §1 first OBS -> INF",
      edits=[ed("the grab interface's description", "**OBS**", "**INF**")]),
 dict(id="E12", file=E, cls="obs-to-inf", what="§2 CFocusGrab::start OBS -> INF",
      edits=[ed("CFocusGrab::start", "**OBS**", "**INF**")]),
 dict(id="E13", file=E, cls="obs-to-inf", what="§3 journal census OBS -> INF",
      edits=[ed("saved journal, latest session", "**OBS**", "**INF**")]),
 dict(id="E14", file=E, cls="obs-to-inf", what="§4 quickshell sync OBS -> INF",
      edits=[ed('`FocusGrab::sync`): "if (!this->active)', "**OBS**", "**INF**")]),
 dict(id="E15", file=E, cls="obs-to-inf", what="§5 issue-565 body OBS -> INF",
      edits=[ed("issue 565, body", "**OBS**", "**INF**")]),
 dict(id="E16", file=E, cls="obs-to-inf", what="§6 decision-table state cell OBS -> INF (row 1)",
      edits=[ed("What can a client ask for?", "| OBS |", "| INF |")]),
 dict(id="E17", file=E, cls="obs-to-inf", what="§6 decision-table state cell OBS -> INF (last row)",
      edits=[ed("Is the protocol part of wayland-protocols?", "| OBS |", "| INF |")]),
 # ---- entry: table cell swaps
 dict(id="E18", file=E, cls="cell-swap", what="§1 interface table: add_surface kind 'request' <-> cleared 'event'",
      edits=[ed("add_surface(surface: wl_surface)", "| request |", "| event |"),
             ed("the compositor cancelled an active grab", "| event |", "| request |")]),
 dict(id="E19", file=E, cls="cell-swap", what="§6: 'Does the portal use it?' OBS <-> 'Who binds it' UNK",
      edits=[ed("Does the portal use it?", "| OBS |", "| UNK |"),
             ed("Who binds it on this host?", "| UNK |", "| OBS |")]),
 # ---- entry: controls (expected kills)
 dict(id="X01", file=E, cls="control", what="verified-at 2026-10-25 -> 2026-10-24 (expect kill b)",
      edits=[ed("verified-at: 2026-10-25", "2026-10-25", "2026-10-24")]),
 dict(id="X02", file=E, cls="control", what="census sessions=2 -> 3 (expect kill h)",
      edits=[ed("journal sessions=2 adverts=78", "sessions=2", "sessions=3")]),
 dict(id="X03", file=E, cls="control", what="S289 line quote (ver 1) -> (ver 2) (expect kill g/d)",
      edits=[ed('pid 1952): "Got interface', '(ver 1)"', '(ver 2)"')]),
 # ---- registry rows
 dict(id="R01", file=S, cls="cell-swap", what="S283 kind 'spec' <-> tier 'A'",
      edits=[ed("| S283 |", "| spec | A |", "| A | spec |")]),
 dict(id="R02", file=S, cls="cell-swap", what="S284 kind 'code' <-> tier 'A'",
      edits=[ed("| S284 |", "| code | A |", "| A | code |")]),
 dict(id="R03", file=S, cls="cell-swap", what="S289 kind 'own-work' <-> tier 'A' (expect kill h)",
      edits=[ed("| S289 |", "| own-work | A |", "| A | own-work |")]),
 dict(id="R04", file=S, cls="receipt-metadata-number", what="S283 anchor '5447 B' -> '5448 B'",
      edits=[ed("| S283 |", "5447 B", "5448 B")]),
 dict(id="R05", file=S, cls="receipt-metadata-number", what="S285 anchor '2568 B' -> '2560 B'",
      edits=[ed("| S285 |", "2568 B", "2560 B")]),
 dict(id="R06", file=S, cls="receipt-metadata-number", what="S286 anchor '24182 B' -> '24128 B'",
      edits=[ed("| S286 |", "24182 B", "24128 B")]),
 dict(id="R07", file=S, cls="receipt-metadata-number", what="S287 anchor '475170 B' -> '475071 B'",
      edits=[ed("| S287 |", "475170 B", "475071 B")]),
 dict(id="R08", file=S, cls="receipt-metadata-number", what="S288 anchor '1903 B' -> '1904 B'",
      edits=[ed("| S288 |", "1903 B", "1904 B")]),
 dict(id="R09", file=S, cls="receipt-metadata-number", what="S289 anchor '19130 B' -> '19131 B'",
      edits=[ed("| S289 |", "19130 B", "19131 B")]),
 dict(id="R10", file=S, cls="receipt-metadata-number", what="S289 anchor '153 lines' -> '152 lines'",
      edits=[ed("| S289 |", "153 lines", "152 lines")]),
 dict(id="R11", file=S, cls="prose-number", what="S286 scope 'which nine it binds' -> 'ten'",
      edits=[ed("| S286 |", "which nine it binds", "which ten it binds")]),
 dict(id="R12", file=S, cls="scalar-recheck", what="S037 (held) recheck 'on-release' -> 'on-sunday'",
      edits=[ed("| S037 |", "on-release", "on-sunday")]),
 dict(id="R13", file=S, cls="receipt-metadata-number", what="S283 anchor sha256 '0bc60c14' -> '0bc60c15'",
      edits=[ed("| S283 |", "sha256 0bc60c14", "sha256 0bc60c15")]),
 dict(id="R14", file=S, cls="receipt-metadata-number", what="S285 anchor sha256 '6f7cecf1' -> '6f7cecf2'",
      edits=[ed("| S285 |", "sha256 6f7cecf1", "sha256 6f7cecf2")]),
 dict(id="R15", file=S, cls="prose-fetchfact", what="S288 'HTTP 200' -> 'HTTP 201'",
      edits=[ed("| S288 |", "HTTP 200", "HTTP 201")]),
 dict(id="R16", file=S, cls="cell-swap", what="tier swap S283 'A' <-> S285 'B'",
      edits=[ed("| S283 |", "| spec | A |", "| spec | B |"),
             ed("| S285 |", "| code | B |", "| code | A |")]),
 # registry controls
 dict(id="X04", file=S, cls="control", what="S283 status mined -> raw (expect kill c)",
      edits=[ed("| S283 |", "| mined |", "| raw |")]),
 dict(id="X05", file=S, cls="control", what="S037 used-by drops the entry (expect kill c)",
      edits=[ed("| S037 |", ", corpus/knowledge/hyprland-focus-grab-r41.md |", " |")]),
 dict(id="X06", file=S, cls="control", what="S283 opened 2026-10-25 -> 2026-10-24 (expect kill c)",
      edits=[ed("| S283 |", "| 2026-10-25 |", "| 2026-10-24 |")]),
 # ---- README row
 dict(id="M01", file=R, cls="cell-swap", what="README r41 row: Note cell <-> Holds cell",
      edits="swapcells:1,2|" + "| `knowledge/hyprland-focus-grab-r41.md` (MADO-R41-1"),
 dict(id="M02", file=R, cls="prose-number", what="README row '63 globals' -> '62' (checkable vs census)",
      edits=[ed("| `knowledge/hyprland-focus-grab-r41.md` (MADO-R41-1", "63 globals", "62 globals")]),
 dict(id="M03", file=R, cls="prose-number", what="README row 'one focus-grab manager advert' -> 'no'",
      edits=[ed("| `knowledge/hyprland-focus-grab-r41.md` (MADO-R41-1", "one focus-grab manager advert", "no focus-grab manager advert")]),
 dict(id="M04", file=R, cls="prose-number", what="README row 'issue 565' -> 'issue 564' (checkable vs S287 locator)",
      edits=[ed("| `knowledge/hyprland-focus-grab-r41.md` (MADO-R41-1", "(issue 565)", "(issue 564)")]),
 # ---- lesson Gate
 dict(id="L01", file=L, cls="receipt-metadata-number", what="Gate prose S037 receipt '1442 B' -> '1443 B'",
      edits=[ed("1442 B, the installed package record", "1442 B", "1443 B")]),
 dict(id="L02", file=L, cls="receipt-metadata-number", what="Gate prose journal '153 lines' -> '154'",
      edits=[ed("19130 B, 153 lines", "153 lines", "154 lines")]),
 dict(id="L03", file=L, cls="prose-number", what="Gate prose 'the seven pre-wave receipts' -> 'eight'",
      edits=[ed("the seven pre-wave receipts", "seven", "eight")]),
 dict(id="L04", file=L, cls="admit-swap", what="ADMIT staged path -> focus-grab-observed-semantics-r9.md",
      edits=[ed("ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as",
                "focus-grab-protocol-live-on-host-r14.md", "focus-grab-observed-semantics-r9.md")]),
 dict(id="L05", file=L, cls="refuse-swap", what="REFUSE staged path -> focus-grab-keyboard-routing-r13.md",
      edits=[ed("REFUSE merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md",
                "privileged-client-surface-r29.md", "focus-grab-keyboard-routing-r13.md")]),
 dict(id="L06", file=L, cls="prose-number", what="Gate prose lesson ref 'M41-6' -> 'M41-7'",
      edits=[ed("M41-6: held ids are not pinned", "M41-6", "M41-7")]),
 # lesson controls
 dict(id="X07", file=L, cls="control", what="GATE S284 sha256 flip (expect kill d)",
      edits=[ed("GATE S284", "sha256=53b762f7", "sha256=53b762f8")]),
 dict(id="X08", file=L, cls="control", what="GATE S285 quote not in receipt (expect kill d/g)",
      edits=[ed("GATE S285", 'deactivated,"', 'deactivated!"')]),
]


def apply_mut(text, spec):
    lines = text.split("\n")
    if isinstance(spec["edits"], str) and spec["edits"].startswith("swapcells:"):
        tag, anchor = spec["edits"].split("|", 1)
        idxs = [i for i, l in enumerate(lines) if anchor in l]
        assert len(idxs) == 1, (spec["id"], "anchor", anchor, idxs)
        i = idxs[0]
        a, b = [int(x) for x in tag.split(":")[1].split(",")]
        parts = lines[i].split("|")
        parts[a], parts[b] = parts[b], parts[a]
        lines[i] = "|".join(parts)
        return "\n".join(lines), i + 1
    first = None
    for e in spec["edits"]:
        idxs = [i for i, l in enumerate(lines) if e["anchor"] in l]
        assert len(idxs) == 1, (spec["id"], "anchor", e["anchor"], idxs)
        i = idxs[0]
        assert e["old"] in lines[i], (spec["id"], "old-missing", e["old"], lines[i][:120])
        lines[i] = lines[i].replace(e["old"], e["new"], 1)
        if first is None:
            first = i + 1
    return "\n".join(lines), first


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def main():
    os.makedirs(OUT, exist_ok=True)
    run(["git", "-C", CLONE, "config", "user.email", "mut@seat.invalid"])
    run(["git", "-C", CLONE, "config", "user.name", "MutEntryQuotes"])
    run(["git", "-C", CLONE, "config", "commit.gpgsign", "false"])
    run(["git", "-C", CLONE, "reset", "-q", "--hard", DATA])
    run(["git", "-C", CLONE, "clean", "-qfd"])
    pristine = {k: open(os.path.join(PRI, v), encoding="utf-8").read() for k, v in FILES.items()}
    # baseline sanity: pristine tree at DATA already committed; counter must be green
    rc, out, err = run(["python3", "quality/counters/c2-r41-focus-entry-v2.py",
                        "--repo", CLONE, "--rev", DATA, "--base", BASE], cwd=CLONE)
    base_ok = "admitted=1/1 verdict=TARGET_MET" in out
    print("baseline green:", base_ok, file=sys.stderr)
    assert base_ok
    rows = []
    for spec in MUTS:
        tgt = os.path.join(CLONE, FILES[spec["file"]])
        orig = pristine[spec["file"]]
        mut, lineno = apply_mut(orig, spec)
        assert mut != orig, spec["id"]
        open(tgt, "w", encoding="utf-8").write(mut)
        run(["git", "-C", CLONE, "add", "-A"])
        rc, co, ce = run(["git", "-C", CLONE, "commit", "-qm", spec["id"]])
        assert rc == 0 or "nothing to commit" not in co + ce, (spec["id"], ce)
        rev = run(["git", "-C", CLONE, "rev-parse", "HEAD"])[1].strip()
        rc, out, err = run(["python3", "quality/counters/c2-r41-focus-entry-v2.py",
                            "--repo", CLONE, "--rev", rev, "--base", BASE], cwd=CLONE)
        final = [l for l in out.splitlines() if "admitted=" in l and "clauses=" in l]
        m = re.search(r"clauses=((?:[a-i]:\d+\s+)+)admitted=(\d)", final[0]) if final else None
        clauses = dict(kv.split(":") for kv in m.group(1).split()) if m else {}
        killed = sorted(k for k, v in clauses.items() if v == "0")
        detail = [l for l in out.splitlines() if "ok=0" in l or "bound=0" in l or "obs=0" in l]
        # save mutant bytes for the reviewer pass
        md = os.path.join(OUT, spec["id"])
        os.makedirs(md, exist_ok=True)
        for k, v in FILES.items():
            p = os.path.join(md, v)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(mut if k == spec["file"] else pristine[k])
        rows.append(dict(id=spec["id"], cls=spec["cls"], file=spec["file"], line=lineno,
                         what=spec["what"], admitted=bool(m) and m.group(2) == "1" and not killed,
                         killed_clauses=killed, rev=rev, detail=detail[:3]))
        print("%-4s %-24s %-8s admitted=%s killed=%s" % (
            spec["id"], spec["cls"], spec["file"], "no" if killed else "YES", ",".join(killed) or "-"),
            flush=True)
        open(tgt, "w", encoding="utf-8").write(orig)
    json.dump(rows, open(os.path.join(ROOT, "results.json"), "w"), indent=1)
    n_sur = sum(1 for r in rows if r["admitted"])
    print("TOTAL %d mutants, %d admitted (survivors), %d killed" % (len(rows), n_sur, len(rows) - n_sur))


if __name__ == "__main__":
    main()
