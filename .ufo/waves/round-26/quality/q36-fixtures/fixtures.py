"""Fixture and mutant declarations for the round-26 Q36 checker repair (repair R4 of M25-3).

Every fixture is a synthetic git repository built by run_fixtures.py under
/fast/scratch/hyaku/mado-r26/q36/repos/<name>/; nothing here touches the lane.

A fixture is:
    name                  directory name and table label
    why                   what the fixture is for
    created / updated     the data registry's JSON fields (only createdAt is read by the checker)
    commits[]             linear history; commit 0 also receives REGISTRY with created/updated
    args                  extra checker arguments ([] means "defaults, no --counter-sha")
    expect_exit           pristine successor exit code on this fixture
    expect_stdout[]       substrings the pristine stdout must contain
    expect_receipt_commit index into commits whose sha must be the printed receipt_commit
    kills[]               mutant ids this fixture is designed to kill

The registry commit is always commit index 0 (see run_fixtures.py) and carries no control
files, so a receipt commit can never be commit 0.
"""

ROUND = 99
CONTROLS = ".ufo/waves/round-99/controls/"
REGISTRY = ".ufo/waves/round-99/w1/reports/swarm-registry.json"

# Two distinct counter sha256 values. SHA_X is the one the sha fixtures select; SHA_Y is a
# decoy that must never qualify a receipt that names only SHA_X.
SHA_X = "3f" * 32
SHA_Y = "7c" * 32

MARKER = "CONTROL Fixture control best: cases_pass=0/1 verdict=not met\n"


def receipt(body=""):
    return MARKER + body


def sha_receipt(sha_text):
    """A receipt whose FIRST line (the CONTROL line) names the given counter sha text."""
    return ("CONTROL Fixture control best: cases_pass=0/1 verdict=not met counter sha256: %s\n"
            % sha_text)


# One filename slug that covers the default --shapes list, so a qualifying receipt with this
# name never fails shape coverage for an unrelated reason.
SHAPE_SLUG = "doNothing-emptyArray-junk-echo-labelKeyed-noReader"


ALL_SHAPES = {
    CONTROLS + "control-doNothing.md": receipt(),
    CONTROLS + "control-emptyArray.md": receipt(),
    CONTROLS + "control-junk.md": receipt(),
    CONTROLS + "control-echo.md": receipt(),
    CONTROLS + "control-labelKeyed.md": receipt(),
    CONTROLS + "control-noReader.md": receipt(),
}

NO_NOREADER = {k: v for k, v in ALL_SHAPES.items() if "noReader" not in k}

FIXTURES = [
    {
        "name": "green",
        "why": "baseline the round-25 checker already passed: all six shapes, receipt before data",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": ALL_SHAPES},
        ],
        "args": [],
        "expect_exit": 0,
        "expect_stdout": ["order=ok", "shapes_missing=-", "CONTROL_RECEIPTS verdict=PASS"],
        "expect_receipt_commit": 1,
        "kills": [],
    },
    {
        "name": "equal-time",
        "why": "receipt commit committer second equals createdAt exactly; strict '<' must fail it",
        "created": "2026-10-22T00:01:00Z",
        "updated": "2026-10-22T00:01:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": ALL_SHAPES},
        ],
        "args": [],
        "expect_exit": 1,
        "expect_stdout": ["order=LATE gap_s=0 shapes_missing=-", "CONTROL_RECEIPTS verdict=FAIL"],
        "kills": ["M1-nonstrict"],
    },
    {
        "name": "missing-shape",
        "why": "order ok but the NoReader shape is not covered by any qualifying receipt name",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": NO_NOREADER},
        ],
        "args": [],
        "expect_exit": 1,
        "expect_stdout": ["order=ok", "shapes_missing=NoReader", "CONTROL_RECEIPTS verdict=FAIL"],
        "kills": ["M2-ignore-shapes"],
    },
    {
        "name": "later-receipt",
        "why": "two receipt-adding commits; the later one is after createdAt and must not supply the time",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": ALL_SHAPES},
            {"at": "2026-10-22T00:09:00+0000",
             "files": {CONTROLS + "control-extra.md": receipt("later note\n")}},
        ],
        "args": [],
        "expect_exit": 0,
        "expect_stdout": ["order=ok", "shapes_missing=-", "CONTROL_RECEIPTS verdict=PASS"],
        "expect_receipt_commit": 1,
        "kills": ["M3-newest-receipt"],
    },
    {
        "name": "nonreceipt-md",
        "why": "the only .md under controls/ carries no CONTROL marker; its name covers every shape",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": {
                CONTROLS + "control-doNothing-emptyArray-junk-echo-labelKeyed-noReader.md":
                    "Fixture note: this file mentions no control and no marker line.\n",
            }},
        ],
        "args": [],
        "expect_exit": 1,
        "expect_stdout": ["receipts=0", "reason=no-receipt-under-", "CONTROL_RECEIPTS verdict=FAIL"],
        "kills": ["M4-any-md"],
    },
    {
        "name": "updated-at",
        "why": "createdAt is after the receipt commit, updatedAt is before it; only createdAt may decide",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:00:30Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": ALL_SHAPES},
        ],
        "args": [],
        "expect_exit": 0,
        "expect_stdout": ["order=ok", "CONTROL_RECEIPTS verdict=PASS"],
        "kills": ["M5-updatedAt"],
    },
    {
        "name": "sha-green",
        "why": "receipt's first line names the selected counter sha; the filter must match it",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": {
                CONTROLS + "control-%s-sha-green.md" % SHAPE_SLUG: sha_receipt(SHA_X),
            }},
        ],
        "args": ["--counter-sha", SHA_X],
        "expect_exit": 0,
        "expect_stdout": ["counter_sha=%s excluded_by_counter_sha=0" % SHA_X,
                          "order=ok", "CONTROL_RECEIPTS verdict=PASS"],
        "kills": [],
    },
    {
        "name": "sha-not-first-line",
        "why": "the counter sha appears only after line 1; the first line names SHA_Y instead",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": {
                CONTROLS + "control-%s-sha-elsewhere.md" % SHAPE_SLUG:
                    sha_receipt(SHA_Y) + "\nElsewhere in this note: %s\n" % SHA_X,
            }},
        ],
        "args": ["--counter-sha", SHA_X],
        "expect_exit": 1,
        "expect_stdout": ["receipts=0", "excluded_by_counter_sha=1",
                          "reason=no-receipt-under-", "CONTROL_RECEIPTS verdict=FAIL"],
        "kills": ["M7-sha-anywhere"],
    },
    {
        "name": "sha-prefix",
        "why": "the first line names only the first 12 hex chars of the counter sha",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": {
                CONTROLS + "control-%s-sha-prefix.md" % SHAPE_SLUG:
                    sha_receipt(SHA_X[:12]),
            }},
        ],
        "args": ["--counter-sha", SHA_X],
        "expect_exit": 1,
        "expect_stdout": ["receipts=0", "excluded_by_counter_sha=1",
                          "CONTROL_RECEIPTS verdict=FAIL"],
        "kills": ["M8-sha-prefix"],
    },
    {
        "name": "sha-late",
        "why": "the sha-X receipt lands after createdAt; an earlier receipt names only SHA_Y",
        "created": "2026-10-22T00:05:00Z",
        "updated": "2026-10-22T00:05:00Z",
        "commits": [
            {"at": "2026-10-22T00:00:00+0000", "files": {}},
            {"at": "2026-10-22T00:01:00+0000", "files": {
                CONTROLS + "control-sha-y-early.md": sha_receipt(SHA_Y),
            }},
            {"at": "2026-10-22T00:09:00+0000", "files": {
                CONTROLS + "control-%s-sha-x.md" % SHAPE_SLUG: sha_receipt(SHA_X),
            }},
        ],
        "args": ["--counter-sha", SHA_X],
        "expect_exit": 1,
        "expect_stdout": ["receipts=1", "order=LATE", "shapes_missing=-",
                          "CONTROL_RECEIPTS verdict=FAIL"],
        "kills": ["M6-ignore-counter-sha"],
    },
]

# Each `old` must occur exactly once in the successor checker; run_fixtures.py refuses to run
# otherwise. `expect` is (pristine exit on killed_by, mutant exit on killed_by).
MUTANTS = [
    {
        "id": "M1-nonstrict",
        "defect": "order comparison uses <= so a receipt in the same second as createdAt counts as early",
        "old": "    order_ok = first[1] < cts",
        "new": "    order_ok = first[1] <= cts",
        "killed_by": "equal-time",
        "expect": [1, 0],
    },
    {
        "id": "M2-ignore-shapes",
        "defect": "shape coverage dropped from the verdict",
        "old": "    ok = order_ok and not missing",
        "new": "    ok = order_ok",
        "killed_by": "missing-shape",
        "expect": [1, 0],
    },
    {
        "id": "M3-newest-receipt",
        "defect": "git log --reverse removed, so the newest receipt-adding commit supplies the time",
        "old": '"--reverse", "--diff-filter=A"',
        "new": '"--diff-filter=A"',
        "killed_by": "later-receipt",
        "expect": [0, 1],
    },
    {
        "id": "M4-any-md",
        "defect": "receipt marker predicate dropped, so every .md under controls/ qualifies",
        "old": "        if not (a.any_md or has_marker(text)):",
        "new": "        if False:",
        "killed_by": "nonreceipt-md",
        "expect": [1, 0],
    },
    {
        "id": "M5-updatedAt",
        "defect": "registry updatedAt read instead of createdAt",
        "old": '        created = json.loads(reg)["createdAt"]',
        "new": '        created = json.loads(reg)["updatedAt"]',
        "killed_by": "updated-at",
        "expect": [0, 1],
    },
    {
        "id": "M6-ignore-counter-sha",
        "defect": "--counter-sha accepted but never applied",
        "old": "    if not counter_shas:",
        "new": "    if True:",
        "killed_by": "sha-late",
        "expect": [1, 0],
    },
    {
        "id": "M7-sha-anywhere",
        "defect": "counter sha matched anywhere in the file, not on the first line",
        "old": '    first = text.split("\\n", 1)[0].lower()',
        "new": "    first = text.lower()",
        "killed_by": "sha-not-first-line",
        "expect": [1, 0],
    },
    {
        "id": "M8-sha-prefix",
        "defect": "counter sha matched as a 12-hex prefix instead of the full 64",
        "old": "    return any(s in first for s in counter_shas)",
        "new": "    return any(s[:12] in first for s in counter_shas)",
        "killed_by": "sha-prefix",
        "expect": [1, 0],
    },
]
