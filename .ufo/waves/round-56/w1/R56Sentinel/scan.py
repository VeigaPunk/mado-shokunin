import re, sys, os, math
pats = {
 "pem_private_key": r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----",
 "ssh_public_key": r"\b(ssh-(rsa|ed25519|dss)|ecdsa-sha2-nistp\d+) [A-Za-z0-9+/=]{40,}",
 "aws_access_key_id": r"\b(AKIA|ASIA)[0-9A-Z]{16}\b",
 "github_token": r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
 "slack_token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
 "google_api_key": r"\bAIza[0-9A-Za-z_-]{30,}",
 "jwt_like": r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}",
 "bearer_header": r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{16,}",
 "url_userinfo": r"[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@",
 "kv_secret_assign": r"(?i)\b(api[_-]?key|apikey|secret|secret[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|pwd|private[_-]?key|client[_-]?secret)\b\s*[:=]\s*[\"']?([^\s\"']{6,})",
 "long_hex_32": r"(?<![0-9a-fA-F])[0-9a-fA-F]{32,}(?![0-9a-fA-F])",
 "long_b64_40": r"(?<![A-Za-z0-9+/=_-])[A-Za-z0-9+/_-]{40,}={0,2}(?![A-Za-z0-9+/=_-])",
 "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
 "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}
def entropy(s):
    from collections import Counter
    c = Counter(s); n = len(s)
    return -sum(v/n*math.log2(v/n) for v in c.values())
def scan(path):
    try: data = open(path, "rb").read()
    except Exception as e: return [("UNREADABLE", type(e).__name__)]
    if b"\0" in data[:8192]: kind="binary"
    else: kind="text"
    out=[]
    text = data.decode("utf-8", "replace")
    for ln, line in enumerate(text.split("\n"), 1):
        for name, p in pats.items():
            for m in re.finditer(p, line):
                tok = m.group(0)
                if name == "long_hex_32" or name=="long_b64_40":
                    # shape: only report if entropy high-ish
                    e = entropy(tok)
                    if name=="long_hex_32" and len(tok)<32: continue
                    if e < 3.0: continue
                    shape = f"len={len(tok)} H={e:.2f}"
                elif name=="kv_secret_assign":
                    v=m.group(2); shape=f"key={m.group(1)} valuelen={len(v)} value_class={'placeholder' if re.fullmatch(r'(?i)(x+|\*+|<.*>|\$\{?[A-Z_]+\}?|changeme|example|none|null|false|true|xxx.*|redacted)',v) else 'nonplaceholder'}"
                elif name=="ipv4":
                    shape=f"octets_class={'loopback/private' if tok.startswith(('127.','10.','192.168.','172.')) else 'other'}"
                elif name=="email":
                    shape=f"domain_class={'example' if tok.split('@')[1].endswith(('example.com','example.org')) else 'other'}"
                else: shape=f"len={len(tok)}"
                out.append((ln, name, shape))
    return out, kind
if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = scan(p)
        if isinstance(r, list): print(f"UNREADABLE {p}"); continue
        hits, kind = r
        print(f"FILE {os.path.relpath(p, '/home/vgpnk/Projects/shokunin/mado-shokunin')} kind={kind} bytes={os.path.getsize(p)} hits={len(hits)}")
        from collections import Counter
        for k,v in Counter(h[1] for h in hits).items(): print(f"   {k}: {v}")
        for ln,name,shape in hits[:12]: print(f"   line {ln} {name} {shape}")
