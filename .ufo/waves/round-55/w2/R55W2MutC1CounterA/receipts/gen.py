import hashlib, json, os, sys
SRC = "/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/export/quality/counters/c1-r55-kbd-entry.py"
OUT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutC1CounterA/mutants"
os.makedirs(OUT, exist_ok=True)
src = open(SRC, encoding="utf-8").read()
# (id, name, old, new, kind, description)
M = [
 ("m01","entry_absent",'missed["entry_absent"].append("entry_absent")',"pass","leg-drop","entry_absent never reported"),
 ("m02","provenance",'missed["provenance"].append("provenance")',"pass","leg-drop","provenance trio never reported"),
 ("m03","index",'missed["index"].append("index")',"pass","leg-drop","README index leg never reported"),
 ("m04","row",'missed["row"].append("row:" + rid)',"pass","leg-drop","row:<id> never reported"),
 ("m05","anchor",'missed["anchor"].append("anchor:" + rid)',"pass","leg-drop","anchor:<id> never reported"),
 ("m06","quote",'missed["quote"].append("quote:" + rid)',"pass","leg-drop","quote:<id> never reported"),
 ("m07","pin_hash",'missed["pin_hash"].append("pin_hash")',"pass","leg-drop","pin_hash never reported"),
 ("m08","source_cell",'missed["source_cell"].append("source_cell:" + rid)',"pass","leg-drop","source_cell:<id> never reported"),
 ("m09","new_rows",'missed["new_rows"].append("new_rows")',"pass","leg-drop","new_rows never reported"),
 ("m10","host",'missed["host"].append("host:" + rid)',"pass","leg-drop","host:<id> never reported"),
 ("m11","tables_sha",'missed["tables_sha"].append("tables_sha")',"pass","leg-drop","tables_sha never reported"),
 ("m12","anchor-flip",'if cells[3] != "%s:%d"','if cells[3] == "%s:%d"',"flip","anchor comparison inverted"),
 ("m13","new_rows-threshold",'if new_rows < new_min:','if new_rows < new_min - 1:',"flip","new_rows threshold off by one (accepts 2/3)"),
 ("m14","exit-code-flip",'(0 if verdict == "TARGET_MET" else 1)','(1 if verdict == "TARGET_MET" else 0)',"flip","exit status inverted"),
 ("m15","tables-sha-flip",'if not sha_ok:','if sha_ok:',"flip","tables_sha leg fires on the match, not the mismatch"),
 ("m16","source-commit-dropped",'if pin.startswith("Hyprland-") and c["commit"] not in url:','if False and c["commit"] not in url:',"drop-clause","source_ok no longer requires the frozen commit in the URL"),
 ("m17","source-status-dropped",'if cells[7] != "mined" or not url.endswith("/" + c["source_suffix"][pin]):','if not url.endswith("/" + c["source_suffix"][pin]):',"drop-clause","source_ok no longer requires status mined"),
 ("m18","source-suffix-dropped",'not url.endswith("/" + c["source_suffix"][pin])','not url',"drop-clause","source_ok no longer requires URL suffix = pin source_suffix"),
 ("m19","prop-strip-dropped",'or prop != prop.strip() ','',"drop-clause","proposition leading/trailing whitespace accepted"),
 ("m20","id-cell-check-dropped",'if (cells[0] != rid or not prop','if (not prop',"drop-clause","id cell compared to rid no longer checked"),
 ("m21","new-row-opened-dropped",'cells[8] != c["opened"] or ','',"drop-clause","new_rows ignores the opened date"),
 ("m22","new-row-tier-dropped",'cells[3] != "A" or ','',"drop-clause","new_rows accepts any tier"),
 ("m23","new-row-usedby-dropped",'if c["entry"] not in cells[10]:','if False:',"drop-clause","new_rows ignores used-by naming the entry"),
 ("m24","pipe-check-cells3",'for x in cells[:4]','for x in cells[:3]',"drop-clause","a pipe inside the anchor cell is no longer a row-grammar failure"),
 ("m25","pin-line-bound",'return lines[n - 1] if n <= len(lines) else None','return lines[n - 1] if n < len(lines) else None',"flip","pin_line: last line of a pin unreachable"),
 ("m26","quote-substring-dropped",'or pl is None or fr["quote"] not in pl:','or pl is None:',"drop-clause","quote:<id> ignores the frozen quote's presence in the pin line"),
 ("m27","html-comment-ignored",'if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:','if False:',"drop-clause","rows inside HTML comments are visible"),
 ("m28","fence-ignored",'fence = m.group(1)','pass',"drop-clause","rows inside fenced code are visible"),
 ("m29","verified-at-prefix",'ver = any(ln == "verified-at: 2026-10-28" for ln in head)','ver = any(ln.startswith("verified-at:") for ln in head)',"flip","provenance accepts any verified-at date"),
 ("m30","source-sid-in-line",'src = any(ln.startswith("source:") and S_IN_LINE.search(ln) for ln in head)','src = any(ln.startswith("source:") for ln in head)',"drop-clause","provenance source line need not cite an S-id"),
 ("m31","index-lt1",'if n_idx != 1:','if n_idx < 1:',"flip","duplicate README index rows accepted"),
 ("m32","backslash-pipe-check-dropped",'if "\\\\|" in line:','if False:',"drop-clause","a backslash-escaped pipe no longer makes the row malformed (equivalent under the other checks, run for completeness)"),
]
manifest = {"original_sha256": hashlib.sha256(src.encode()).hexdigest(), "mutants": []}
for mid, name, old, new, kind, desc in M:
    n = src.count(old)
    assert n == 1, (mid, n, old)
    mut = src.replace(old, new, 1)
    assert mut != src
    fn = "%s-%s.py" % (mid, name)
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as fh:
        fh.write(mut)
    import difflib
    d = [l for l in difflib.unified_diff(src.splitlines(), mut.splitlines(), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    manifest["mutants"].append({"id": mid, "name": name, "file": fn, "kind": kind, "desc": desc,
                                "old": old, "new": new, "changed_lines": len(d),
                                "sha256": hashlib.sha256(mut.encode()).hexdigest()})
json.dump(manifest, open("/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterA/gen/manifest.json", "w"), indent=1)
print(len(M), "mutants written; original sha256", manifest["original_sha256"])
