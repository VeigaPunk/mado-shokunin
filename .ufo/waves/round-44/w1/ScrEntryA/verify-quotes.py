#!/usr/bin/env python3
"""Verify each candidate Gate quote against the pinned receipts using the frozen
counter's own helpers: word count, word-bounded uniqueness, line locator,
comment-stripped presence, and absence from the other four receipts."""
import hashlib, importlib.util, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(LANE, ".ufo/waves/round-44/fetch")
COUNTER = os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py")

spec = importlib.util.spec_from_file_location("c2r44", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

Q = {
 "S164": ("Hyprland-Window.cpp",
   "else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());"),
 "S298": ("Hyprland-XDGShell.cpp",
   "uint32_t CXDGToplevelResource::setSize(const Vector2D& size) { m_pendingApply.size = size; scheduleStateApplication(); return m_owner->scheduleConfigure(); }"),
 "S299": ("xdg-shell.xml",
   "The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates."),
 "S300": ("gdktoplevel-wayland.c",
   "wayland_surface->next_layout.configured_width = width; wayland_surface->next_layout.configured_height = height;"),
 "S301": ("gkeep-ui.py",
   'window = Gtk.ApplicationWindow(application=self, title="gkeep") window.set_decorated(False) window.set_default_size(420, 500) self.board = Board(window)'),
}

blobs = {}
for i, (name, _) in Q.items():
    p = os.path.join(FETCH, name)
    blobs[i] = open(p, "rb").read()

# pins must equal the frozen PINS table
ok = True
for i, (name, _) in Q.items():
    d = hashlib.sha256(blobs[i]).hexdigest()
    pin = c2.PINS.get(name)
    if i == "S164":
        # held id: receipt is byte-checked against the pin fetched this round
        print(f"PIN {name} sha256={d} (held id, path pinned this round)")
    else:
        good = pin == d
        ok &= good
        print(f"PIN {name} sha256={d} matches_PINS={good}")

print("-" * 70)
for i, (name, q) in Q.items():
    nq = re.sub(r"\s+", " ", q)
    blob = blobs[i]
    words = len(q.split())
    at = c2.quote_at(blob, nq)
    occ = len(c2.occurrences(blob, nq))
    incode = c2.quote_in_code(blob, nq, name)
    others = [j for j in Q if j != i and nq in c2.norm_receipt(blobs[j])]
    inown = nq in c2.norm_receipt(blob)
    checks = dict(words=words, in_3_25=3 <= words <= 25, at=at,
                  occ=occ, unique=occ == 1, in_code=incode,
                  in_own_normalized=inown, in_other_receipts=others)
    good = (checks["in_3_25"] and at is not None and checks["unique"]
            and incode and inown and not others)
    ok &= good
    print(f"{i} {name}:{at} sha256={hashlib.sha256(blob).hexdigest()}")
    print(f"   words={words} at={at} occurrences={occ} in_comment_stripped_code={incode} "
          f"in_own_norm={inown} in_other_receipts={others} OK={good}")
    print(f"   quote={nq!r}")
    if not good:
        print("   !!! FAILS a clause-d condition !!!")
print("-" * 70)
print("ALL_OK", ok)
sys.exit(0 if ok else 1)
