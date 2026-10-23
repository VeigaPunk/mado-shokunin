#!/usr/bin/env python3
r"""mado round 24, claim C1 (coverage: Hyprland window-rule attribution route) frozen counter.

Usage: python3 -I .ufo/waves/round-24/c1/count.py REV [--offline] [--json]
Run from anywhere; reads the lane repo read-only with `git show REV:<path>`.

Frozen predicate v2 (same sentence in registration.md, this code, and every receipt;
v2 adds the claim-anchor clause before any data seat, after control CtlC1LabelShortcut's design):
"PASS_ROW: a claim row `| A<n> | <claim> | S### | \"<quote>\" |` in
corpus/knowledge/rule-attribution-r24.md at REV whose S### is a SOURCES.md row with
status `mined`, opened `2026-10-23`, used-by naming the note, a source URL pinned to a
tag or 40-hex commit under github.com or raw.githubusercontent.com /hyprwm/Hyprland or
/hyprwm/hyprland-wiki, and a recorded sha256 equal to the sha256 of the bytes re-fetched
from that URL now, where the quote (<=25 words, containing a rule-topic word) occurs
verbatim (whitespace-collapsed) in those bytes, and whose claim cell contains a run of
at least 4 consecutive words of that quote or a backticked identifier of at least 4
characters that occurs in that quote."
COUNTER_VERSION = v2

Counted value: number of distinct PASS_ROW rows. The round target needs PASS_ROW >= 6
from >= 3 distinct S### rows AND the note indexed by a coverage-map row in
corpus/README.md (`| \`knowledge/rule-attribution-r24.md\``) -> verdict line `TARGET_MET`.
--offline replaces the network re-fetch with the committed copy
.ufo/waves/round-24/fetch/<S###>.bin (diagnostic only; the counted mode re-fetches).
Exit 0 TARGET_MET, 1 not met, 2 setup error.
"""
import hashlib, json, os, re, subprocess, sys, urllib.request

LANE = os.environ.get("MADO_LANE", "/home/vgpnk/Projects/shokunin/mado-shokunin")  # sandbox clones for controls
NOTE = "corpus/knowledge/rule-attribution-r24.md"
OPENED = "2026-10-23"
URL_RE = re.compile(
    r"https://(?:raw\.githubusercontent\.com/hyprwm/(?:Hyprland|hyprland-wiki)/(?P<p1>[^/\s]+)/"
    r"|github\.com/hyprwm/(?:Hyprland|hyprland-wiki)/blob/(?P<p2>[^/\s]+)/)[^\s|`)]+")
PIN_RE = re.compile(r"^(?:[0-9a-f]{40}|v\d+(?:\.\d+)+)$")
SHA_RE = re.compile(r"sha256[ :`]*([0-9a-f]{64})")
TOPIC_RE = re.compile(r"\b(?:window ?rules?|windowrules?(?:v2)?|layerrules?|rules?|getprop|props?|tags?|match(?:es|ing)?)\b", re.I)
ROW_RE = re.compile(r'^\|\s*(A\d+)\s*\|(.*?)\|\s*(S\d{3,})\s*\|\s*"(.+)"\s*\|\s*$')


def git_show(rev, path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def anchored(claim, quote):
    """v2 claim-anchor clause: a >=4-word run of the quote, or a backticked >=4-char identifier from it."""
    c = collapse(claim).lower()
    w = collapse(quote).lower().split()
    if any(" ".join(w[i:i + 4]) in c for i in range(len(w) - 3)):
        return True
    return any(len(t) >= 4 and t in quote for t in re.findall(r"`([^`\s]+)`", claim))


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def raw_url(u):
    m = re.match(r"https://github\.com/hyprwm/([^/]+)/blob/(.+)$", u)
    return f"https://raw.githubusercontent.com/hyprwm/{m.group(1)}/{m.group(2)}" if m else u


def fetch(url, offline_path, rev):
    if offline_path is not None:
        r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{offline_path}"], capture_output=True)
        return r.stdout if r.returncode == 0 else None
    try:
        req = urllib.request.Request(raw_url(url), headers={"User-Agent": "mado-r24-c1-counter"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except Exception:
        return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    as_json = "--json" in sys.argv
    if len(args) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    rev = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", args[0] + "^{commit}"],
                         capture_output=True, text=True)
    if rev.returncode != 0:
        print("setup error: bad REV", file=sys.stderr)
        return 2
    rev = rev.stdout.strip()
    sources = git_show(rev, "corpus/SOURCES.md")
    readme = git_show(rev, "corpus/README.md") or ""
    if sources is None:
        print("setup error: corpus/SOURCES.md missing at REV", file=sys.stderr)
        return 2
    srows = {}
    for line in sources.splitlines():
        m = re.match(r"^\|\s*(S\d{3,})\s*\|", line)
        if m:
            srows[m.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")]
    note = git_show(rev, NOTE)
    results, cache = [], {}
    seen_quotes = set()
    for line in (note or "").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        rid, claim, sid, quote = m.group(1), m.group(2).strip(), m.group(3), m.group(4)
        why = []
        q = collapse(quote)
        if len(q.split()) > 25:
            why.append("quote>25w")
        if not TOPIC_RE.search(q):
            why.append("quote-off-topic")
        if len(claim.split()) < 8:
            why.append("claim<8w")
        if not anchored(claim, quote):
            why.append("claim-not-anchored-to-quote")
        if q in seen_quotes:
            why.append("duplicate-quote")
        row = srows.get(sid)
        url = sha = None
        if row is None or len(row) != 11:
            why.append("no-11-cell-sources-row")
        else:
            if row[7] != "mined":
                why.append("status!=mined")
            if row[8] != OPENED:
                why.append("opened!=" + OPENED)
            if NOTE not in row[10] and NOTE.split("/", 1)[1] not in row[10]:
                why.append("used-by-missing-note")
            um = URL_RE.search(row[1])
            if not um:
                why.append("no-hyprwm-url")
            else:
                url = um.group(0)
                if not PIN_RE.match(um.group("p1") or um.group("p2") or ""):
                    why.append("url-not-pinned")
            sm = SHA_RE.search(" ".join(row))
            if not sm:
                why.append("no-sha256")
            else:
                sha = sm.group(1)
        if url and sha:
            key = (url, sid)
            if key not in cache:
                cache[key] = fetch(url, f".ufo/waves/round-24/fetch/{sid}.bin" if offline else None, rev)
            data = cache[key]
            if data is None:
                why.append("fetch-failed")
            else:
                if hashlib.sha256(data).hexdigest() != sha:
                    why.append("sha256-mismatch")
                elif q not in collapse(data.decode("utf-8", "replace")):
                    why.append("quote-not-in-bytes")
        ok = not why
        if ok:
            seen_quotes.add(q)
        results.append({"row": rid, "source": sid, "label": "PASS_ROW" if ok else "FAIL_ROW", "why": why})
    passing = [r for r in results if r["label"] == "PASS_ROW"]
    distinct = sorted({r["source"] for r in passing})
    indexed = bool(re.search(r"^\| `knowledge/rule-attribution-r24\.md`", readme, re.M))
    met = len(passing) >= 6 and len(distinct) >= 3 and indexed
    me = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    summary = {"counter_version": "v2", "revision": rev, "mode": "offline" if offline else "refetch", "note_present": note is not None,
               "rows": len(results), "PASS_ROW": len(passing), "distinct_sources": len(distinct),
               "readme_indexed": indexed, "verdict": "TARGET_MET" if met else "TARGET_NOT_MET",
               "counter_sha256": me}
    if as_json:
        print(json.dumps({"summary": summary, "rows": results}, indent=1))
    else:
        for r in results:
            print(f"{r['row']}\t{r['source']}\t{r['label']}\t{','.join(r['why']) or '-'}")
        print(" ".join(f"{k}={v}" for k, v in summary.items()))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
