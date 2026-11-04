#!/usr/bin/env python3
"""Generate six independent mutants of the r82 allocation code."""
import hashlib
import os
import sys

MUTANTS = [
    ("zero-guard-tests-declaration",
     '    if band <= 0:\n'
     '        raise Unmodelled("%s %r was allocated a %d %s band; a zero band reserves nothing"\n',
     '    if spec[axis] <= 0:\n'
     '        raise Unmodelled("%s %r was allocated a %d %s band; a zero band reserves nothing"\n',
     "the zero-band guard is evaluated against the declaration (always 0 in the dynamic "
     "case) instead of the resolved allocation, so a declared allocation can never fill a "
     "dynamic band"),
    ("alloc-wrong-axis",
     '    axis = "height" if spec["position"] in ("top", "bottom") else "width"\n',
     '    axis = "width" if spec["position"] in ("top", "bottom") else "height"\n',
     "the allocation is looked up on the cross axis: horizontal surfaces read width, "
     "vertical surfaces read height"),
    ("alloc-overrides-explicit",
     '    axis = "height" if spec["position"] in ("top", "bottom") else "width"\n'
     '    if spec[axis] > 0:\n'
     '        return spec[axis]\n'
     '    band = allocation.get(spec["namespace"])\n',
     '    axis = "height" if spec["position"] in ("top", "bottom") else "width"\n'
     '    band = allocation.get(spec["namespace"])\n'
     '    if band is not None and band > 0:\n'
     '        return band\n'
     '    if spec[axis] > 0:\n'
     '        return spec[axis]\n',
     "the allocation is consulted before the declaration, so a positive declared band is "
     "overridden by the allocation"),
    ("alloc-bool-accepted",
     '        if not isinstance(value, int) or isinstance(value, bool):\n'
     '            raise Setup("the allocation for %r is not an integer" % name)\n',
     '        if not isinstance(value, int):\n'
     '            raise Setup("the allocation for %r is not an integer" % name)\n',
     "the bool exclusion in parse_allocation is dropped: JSON true/false are accepted as "
     "an allocation (bool is an int subclass)"),
    ("composition-allocation-dropped",
     '    bar_spec[band_axis] = band_of(bar_spec, allocation)\n',
     '    bar_spec[band_axis] = band_of(bar_spec, {})\n',
     "the composition path resolves the bar's band against an empty allocation map, so a "
     "dynamic bar in a composed stack is refused instead of modelled"),
    ("alloc-margin-double-counted",
     '    height = band_of(bar, allocation) if pos in ("top", "bottom") else bar["height"]\n',
     '    height = (band_of(bar, allocation) + m["top"] + m["bottom"] '
     'if bar["height"] == 0 else band_of(bar, allocation)) '
     'if pos in ("top", "bottom") else bar["height"]\n',
     "a dynamic band's height gets both margins added on top of the allocation even though "
     "the dynamic branch already places the origin at the top margin (the margin is counted "
     "twice)"),
]


def main(tool_path, outdir):
    source = open(tool_path).read()
    os.makedirs(outdir, exist_ok=True)
    manifest = []
    for name, anchor, repl, note in MUTANTS:
        count = source.count(anchor)
        if count != 1:
            print("ANCHOR-ERROR %s count=%d" % (name, count))
            return 2
        mutated = source.replace(anchor, repl)
        if mutated == source:
            print("NOOP-ERROR %s" % name)
            return 2
        path = os.path.join(outdir, "mutant-%s.py" % name)
        with open(path, "w") as fh:
            fh.write(mutated)
        manifest.append((name, path, note, hashlib.sha256(mutated.encode()).hexdigest()))
        print("WROTE %s sha256=%s" % (name, manifest[-1][3]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
