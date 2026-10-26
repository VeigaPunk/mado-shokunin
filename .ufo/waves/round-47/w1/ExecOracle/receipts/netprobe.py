"""Network probe run inside the oracle sandbox (receipt helper)."""
import socket

out = []
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(("127.0.0.1", 53))
    out.append("connected 127.0.0.1:53")
except OSError as exc:
    out.append("connect 127.0.0.1:53 rejected: %s (errno %s)" % (exc.strerror, exc.errno))
try:
    socket.getaddrinfo("example.com", 80)
    out.append("dns resolved example.com")
except OSError as exc:
    out.append("dns example.com failed: %s" % exc.__class__.__name__)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 0))
    out.append("udp bind ok")
except OSError as exc:
    out.append("udp bind failed: %s" % exc.strerror)
with open("/proc/net/dev") as fh:
    ifaces = [line.split(":")[0].strip() for line in fh.read().splitlines()[2:]]
out.append("interfaces: " + " ".join(ifaces))
print("\n".join(out))
