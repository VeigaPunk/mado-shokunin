#!/usr/bin/env python3
"""CritEntryClient (round 44, w2) - a branch-for-branch model of the two pinned GTK 4.24.1
functions, used to test the entry's two universal sentences against reachable states.

This is NOT GTK and NOT an execution of it: it transcribes gdk_wayland_toplevel_handle_configure
(gdktoplevel-wayland.c:606-703) and gdk_wayland_toplevel_compute_size (gdktoplevel-wayland.c:445-552)
plus gdk_surface_constrain_size (gdksurface.c:1576-1615), with the source line that governs each
step. check.py verifies that every cited line exists with the asserted text, so a transcription
error shows up there. Run: python3 trace.py (exit 0 iff every expected outcome holds).
"""
import sys

MAXIMIZED, FULLSCREEN, TILED, RESIZING = "maximized", "fullscreen", "tiled", "resizing"


class Toplevel:
    """The state the two pinned functions keep."""

    def __init__(self, natural=(420, 500), minimum=(200, 150), resizable=True):
        self.resizable = resizable        # layout flag: gdktoplevel-wayland.c:490, gtkwindow.c:4056
        self.natural = natural            # compute-size size: gdktoplevel-wayland.c:543-544
        self.minimum = minimum            # compute-size min: gtkwindow.c:4463
        self.saved = (0, 0)               # gdktoplevel-wayland.c:210-211
        self.surface_wh = natural         # the last applied surface size
        self.surface_state = frozenset()
        # next_layout
        self.should_constrain = False     # :113
        self.size_is_fixed = False        # :114
        self.cw = self.ch = 0             # :115-116
        self.dirty = True
        self.surface = natural

    # gdktoplevel-wayland.c:610-703
    def handle_configure(self, width, height, states=frozenset(), is_resizing=False):
        new_state = frozenset(states)
        fixed_size = bool(new_state & {MAXIMIZED, FULLSCREEN, TILED}) or is_resizing   # :633-637
        was_fixed_size = bool(self.surface_state & {MAXIMIZED, FULLSCREEN, TILED})     # :639-642
        w, h = width, height                                                           # :644-645
        saved_size = (w == 0 and h == 0)                                               # :647
        if saved_size and not fixed_size and was_fixed_size:                           # :656-660
            w, h = self.saved
        if w > 0 and h > 0:                                                            # :663
            if not saved_size:                                                         # :664-668
                self.should_constrain = True
                self.save_size()                                                       # :197-211
            elif is_resizing:                                                          # :671-674
                self.should_constrain = True
            else:                                                                      # :675-678
                self.should_constrain = False
            self.size_is_fixed = fixed_size                                            # :680
            self.cw, self.ch = w, h                                                    # :681-682
        else:                                                                          # :684-690
            self.should_constrain = False
            self.size_is_fixed = False
            self.cw = self.ch = 0
        self.surface_state = new_state                                                 # :699
        self.dirty = True                                                              # :692

    # gdktoplevel-wayland.c:197-212
    def save_size(self, shadows=(0, 0)):
        if self.surface_state & {MAXIMIZED, FULLSCREEN, TILED}:                        # :202-205
            return
        if self.surface_wh[0] <= 1 or self.surface_wh[1] <= 1:                         # :207-208
            return
        self.saved = (self.surface_wh[0] - sum(shadows), self.surface_wh[1] - sum(shadows))  # :210-211

    # gdktoplevel-wayland.c:445-552
    def compute_size(self):
        if not self.dirty:
            return self.surface
        if self.resizable:                                                             # :490-494
            hints, mask = (self.minimum, None), "min-only"
        else:                                                                          # :496-501
            hints, mask = (self.natural, self.natural), "min=max=natural"
        shadow = (0, 0)                                                                # :505-511; 0 for decorated=False, gtkwindow.c:4182-4206
        if self.cw > 0 and self.ch > 0:                                                # :513-514
            w, h = self.cw + sum(shadow), self.ch + sum(shadow)                        # :518-521
            if self.should_constrain:                                                  # :523-528
                w, h = clamp(w, h, *hints)                                             # gdksurface.c:1596-1611
            if not self.size_is_fixed:                                                 # :532-537
                self.should_constrain = False
                self.cw = self.ch = 0
        else:                                                                          # :539-549
            w, h = self.natural
            w, h = clamp(w, h, *hints)
        self.dirty = False                                                             # :551
        self.surface = (w, h)
        self.surface_wh = (w, h)
        return self.surface


def clamp(w, h, mn, mx):
    """gdksurface.c:1596-1611."""
    mnw, mnh = mn
    mxw, mxh = (mx if mx else (2**31 - 1, 2**31 - 1))
    return min(max(w, mnw), mxw), min(max(h, mnh), mxh)


CASES = [
    # label, setup, actions, expected surface, what it tests
    ("A resizable, plain 420x500 configure", dict(),
     [("configure", 420, 500, (), False)], (420, 500), "entry INF: adopted"),
    ("B resizable, configure below the minimum", dict(),
     [("configure", 100, 80, (), False)], (200, 150), "entry INF: raised to the minimum"),
    ("C non-resizable, plain 600x700 configure", dict(resizable=False),
     [("configure", 600, 700, (), False)], (420, 500),
     "COUNTEREXAMPLE to entry:52 - the configured size is replaced by the computed one, not adopted"),
    ("D resizable, 0x0 configure after maximized", dict(),
     [("configure", 500, 400, (), False),
      ("configure", 900, 700, (MAXIMIZED,), False),
      ("configure", 0, 0, (), False)], (500, 400),
     "COUNTEREXAMPLE to entry:50 - the saved size is restored, not the computed size (420x500)"),
    ("E resizable, fresh 0x0 configure", dict(),
     [("configure", 0, 0, (), False)], (420, 500), "entry:50's claim holds only on this path"),
    ("F resizable, tiled configure then a later layout", dict(),
     [("configure", 500, 400, (TILED,), False),
      ("present", 600, 700)], (500, 400),
     "COUNTEREXAMPLE to entry:52's parenthetical - fixed is sticky (532-537), so a later layout "
     "re-applies the latched size instead of the newly computed 600x700"),
    ("G resizable, plain configure then a later layout", dict(),
     [("configure", 500, 400, (), False),
      ("present", 600, 700)], (600, 700),
     "control for F: without the fixed state the latch is cleared and the computed size wins"),
]


def run():
    bad = 0
    for label, kwargs, actions, want, why in CASES:
        t = Toplevel(**kwargs)
        for act in actions:
            if act[0] == "configure":
                t.handle_configure(act[1], act[2], frozenset(act[3]), act[4])
            elif act[0] == "present":
                t.natural = (act[1], act[2])   # gdk_wayland_toplevel_present: :1861-1865
                t.dirty = True
            got = t.compute_size()
        ok = got == want
        bad += 0 if ok else 1
        print("%s %-46s surface=%s want=%s  %s" % ("OK  " if ok else "FAIL", label, got, want, why))
    print("RESULT cases=%d fails=%d" % (len(CASES), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
