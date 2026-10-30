
# ---- injected into a scratch copy of the frozen harness by harness_proof.py ----
# _mk_patch: a harness-shaped mutation that applies a fixture's git patch.
# _exact:    a harness-shaped check that asserts the EXACT leg set (needed for the CONTROL-N
#            fixtures, where the mutant reports a SUPERSET of the pristine's legs).

def _mk_patch(path):
    def m(d, ctx):
        p = subprocess.run(["git", "apply", "--binary", "--whitespace=nowarn", path],
                           cwd=str(d), env=_env(Path(d)), capture_output=True)
        if p.returncode != 0:
            raise MutationError("fixture patch does not apply: %s"
                                % p.stderr.decode("utf-8", "replace").strip()[:200])
    return m


def _exact(legs):
    want = set(legs)

    def check(rec):
        extra = sorted(set(rec["legs"]) - want)
        missing = sorted(want - set(rec["legs"]))
        if missing or extra:
            return ("leg set differs: missing=%s extra=%s"
                    % (",".join(missing[:6]), ",".join(extra[:6])))
        return None
    return check
