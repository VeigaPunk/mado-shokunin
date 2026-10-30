# Cross-source inotify plane — R56W3ConnCrossSrc

## Scope and axes

Attack: cross-source pattern finding across S383, S390, queued S396/S397, and the explicitly authorized Linux inotify_user.c source. Coverage = sourced understanding; operability = capability to reconcile predicted add attempts with registrations; calibration = distinguish documented, observed and inferred facts (C3 itself measures token-level back-reference consistency, not this semantic calibration). Frozen predicates/targets remain unchanged. This is one documentation-navigation proposal, not a claim judgment or integration.

Fixed lane revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. S383/S390 pins were compared byte-for-byte with the git objects at that revision. New queued-page pins are attempt-2 working-cache artifacts explicitly named by the assignment, not claimed to exist at that revision. The optional Linux master fetch is supplementary source evidence, not evidence about the running kernel build.

## Agreement / disagreement / gap table

| Surface | Evidence and relationship | Consequence / severity |
|---|---|---|
| Request versus path lookup | S383 ConfigWatcher.cpp:54-70 supplies `IN_CLOSE_WRITE\|IN_DONT_FOLLOW` for files, adds create/delete/move bits for directories, and separately requests `IN_CLOSE_WRITE` on a symlink's canonical target. S390 inotify.7.html:261-262 defines DONT_FOLLOW as pathname lookup behavior. Linux inotify_user.c:754-757 conditionally sets LOOKUP_FOLLOW / LOOKUP_DIRECTORY. **AGREE.** | The lookup flag is not an independently observed subscription event. Entry line134 already makes the observation limit explicit; do not report it as a new defect. |
| Requested mask versus observed mask | Cached w2 comparison and capture show mask `8`, versus requested primary-file mask `0x02000008`; the cached probe reports directory request `0x020003c8` -> fdinfo `0x3c8`. Kernel inotify_arg_to_mask:99-114 masks arguments with INOTIFY_USER_MASK and adds internal bits; inotify_arg_to_flags:120-129 stores some options separately. **AGREE at the plane boundary**, not numeric identity. | Compare event subscriptions separately from path-resolution flags. The named kernel file does not define INOTIFY_USER_MASK or implement the fdinfo formatter; it alone does not prove the exact printed projection. No new frozen-predicate defect. |
| `800afff` provenance | S397 proc_pid_fdinfo.5.html:157-158 contains `mask:800afff` in its illustrative inotify output. Fixed-revision w2 fdinfo-capture.txt has 80 inotify lines (two fd blocks), every mask `8`, no `800afff`. Entry line134 says 40 watches on one instance through two descriptors. **DISAGREE with the premise that this example value was observed on this compositor; not with the entry.** | Weakens any empirical claim that transfers the manual's example to this host. It does not falsify C1 or C2. Eighty printed lines do not imply eighty distinct watches. |
| Add attempts versus distinct registrations | S396 inotify_add_watch.2.html:80-100 says existing inode in the same instance returns its existing wd, including another link. S383:59-71 nevertheless appends a record for each call and does not check errors. **AGREE**, but different cardinalities. | Count attempted registrations, successful distinct `(instance,inode)` registrations, and stored callback paths separately. Permission/ENOENT/ENOSPC failures in S396:108-131 can produce no live watch despite an attempted record. This is a documented model boundary, not a fresh failure of frozen fixtures. |
| Alias collision can change more than counts | S390:276-280 says MASK_ADD ORs rather than replaces; :293-302 warns multiple paths can clobber masks. Linux :536-568 returns existing wd and clears/replaces the mask without IN_MASK_ADD. S383 never passes IN_MASK_ADD, and callback lookup :100 returns the first matching wd. **AGREE**, with a second-order gap in path-only comparisons. | [INFERENCE] If a directory D gets the full directory mask, then a symlink-to-D adds its canonical-target watch later with CLOSE_WRITE only, the later call can narrow D's existing subscription while callbacks still use the first stored path. Reverse order can restore the directory mask. No runtime case was executed here. This weakens a generalization from watch-path parity to event-mask parity; route any new model/fixture requirement to round57, never widen C2 now. |
| `wd` radix | S397:164 explicitly says wd is decimal. Cached capture:18 has `wd:1f`, and :9 has `wd:28`; cached comparison presents sequential decimal descriptors 1..40. **LITERAL CONTRADICTION** between the man-page field description and this captured format. | Weakens a parser or verification procedure that follows that sentence literally. `int(token,10)` cannot parse `1f`. Retain raw tokens and use the capture's hexadecimal convention for this cached comparison; do not silently call the man page correct. The authorized kernel file only references inotify_show_fdinfo at :358, so its formatter cannot resolve this independently. |
| `ignored_mask` scope | S397:157-158 includes ignored_mask:0 in an inotify example, but its explicit definition at :207-209 is under **fanotify**, following :178. The cached inotify capture also has ignored_mask:0. S390:307-310 defines **IN_IGNORED**, a watch-removal event, not an ignored_mask field. The fetched inotify_user.c has no ignored_mask token or formatter implementation. **GAP**, not agreement by shared spelling. | Weakens any assertion that the fanotify ignored-mask definition establishes inotify semantics, or that ignored_mask:0 proves no IN_IGNORED notifications occurred. Neither conclusion is warranted here. No runtime ignored-mask behavior was verified. |
| Event and callback plane | S390:242-244 describes event `name` for directory children; S383:100-107 uses matched watch's stored file and never reads event name or mask. **AGREE as API usage**, not evidence of per-child callback paths. | A path/inode registration match does not establish which callback name or reload count a save produces. Entry's event-delivery UNKNOWN remains. |

## One bounded proposed move: teach the plane boundaries through study order

Draft for the existing SOURCES.md Paths section (not applied):

- Inotify plane: events, inode identity, add requests, then observation — S390 → S396 → S383 → S397: learn event/lookup flags and mask replacement, then per-instance inode identity, read Hyprland's ordered add calls, and only then interpret fdinfo without mistaking requests, registrations or manual examples for runtime events.

This single navigation move improves coverage by connecting already held/queued sources, and improves semantic calibration by making the request/registration/observation distinction explicit. It changes no runtime code, frozen predicates, counters, or source used-by cells, so it does not trade operability or C3 consistency for apparent coverage. S396/S397 are queued draft IDs: applying the line before those rows exist would create an unresolved route; leave this as a proposal until integration owns that decision. Do not promote them to mined merely because the Paths line exists.

## Risks and verification handoff

- The man page's radix wording and ignored_mask prose gap remain explicit contradictions/limits, not averaged into an accuracy score. Navigation does not fix the documentation or establish live behavior.
- Linux master is mutable and not the operator's kernel build; fetched-byte hash and copy are preserved. Do not attribute that code to kernel7.2.11 without a matching versioned source.
- A future verification should inspect version-matched fdinfo formatting and the mask constants, then exercise duplicate directory/alias add order in an isolated scratch instance, including effective mask and callback-path association. This was **not run** by this source connector.
- For this proposal, integration should check that all four IDs exist, the Paths line is unique, queued statuses remain queued, and no used-by cells or frozen artifacts change. No counter/harness suite was run here; this seat did not re-score any claim.
- No host /proc access, state change, fixture mutation, clone, git mutation, tool install, other agent/model invocation or tracked-file edit was performed.

## Executed evidence and decisive outputs

Filesystem reads used the read tool with these absolute ranges:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/man7-inotify.7.html:240-310`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html:65-145`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html:140-215`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2RevProcFdinfo/comparison.md` and `fdinfo-capture.txt:1-18`.

Read-only git commands, executed via subprocess argument arrays (rc0):

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp
  :55 fileMask = IN_CLOSE_WRITE | IN_DONT_FOLLOW
  :56 directoryMask = fileMask | IN_CREATE | IN_DELETE | IN_MOVED_TO | IN_MOVED_FROM
  :69 inotify_add_watch(... CANONICAL.c_str(), IN_CLOSE_WRITE)
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/knowledge/hyprland-config-autoreload-r56.md
  :134 kernel shows mask 0x8 ... IN_DONT_FOLLOW ... not confirmed by observation
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/SOURCES.md
  :333 S383; :340 S390; :347 ## Paths
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/fetch/man7-inotify.7.html
  sha256=79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd working_pin_equal=True
  watcher sha256=8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c working_pin_equal=True
```

Fixed-revision capture check ran in the tool's persistent Python evaluation cell, **not a `python3 -I` CLI invocation**: subprocess git-show, `str.splitlines`, `re.findall(r'\bmask:([0-9a-f]+)', text)` and literal membership checks (no executable lane code imported). This explicitly discloses the interpreter exception; no counter execution is claimed:

```python
b = subprocess.run(['git','-C',lane,'show',rev+':.ufo/waves/round-56/w2/R56W2RevProcFdinfo/fdinfo-capture.txt'], capture_output=True,text=True,check=True).stdout
lines = [s for s in b.splitlines() if s.startswith('inotify ')]
print(len(lines), sorted(set(re.findall(r'\bmask:([0-9a-f]+)', b))), 'wd:1f ' in b, 'mask:800afff' in b)
```

Output: `80 ['8'] True False`. The last value is the exact null check for the alleged host mask example. This is a cached capture check, not a fresh live observation.

Queued pin byte checks (hashlib.sha256 over read_bytes):

```text
man7-inotify_add_watch.2.html sha256=98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d bytes=11345
man7-proc_pid_fdinfo.5.html sha256=f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1 bytes=14694
```

Kernel fetch: initial read-tool URL returned HTTP429. Different retrieval succeeded:

```text
curl -fSL --max-time 40 https://raw.githubusercontent.com/torvalds/linux/master/fs/notify/inotify/inotify_user.c -o /fast/scratch/hyaku/mado-r56/R56W3ConnCrossSrc/inotify_user.c
rc=0 bytes=21756 sha256=f5dd113ad7b7d457dc8453d29d240d6ffaf352d52a2ac8ad374cd703208e1ea0
```

Kernel token census (Python `enumerate(text.splitlines(),1)` and `term in line`): `ignored_mask: []`, `seq_printf: []`, `inotify_show_fdinfo: [358]`. These are exact null results for the named file, not claims that the entire kernel lacks the fields. Kernel copy is preserved beside this receipt as `kernel-inotify_user.c`; scratch was removed before submission.
