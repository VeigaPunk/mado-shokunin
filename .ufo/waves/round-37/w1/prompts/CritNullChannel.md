# CritNullChannel — critic seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: critic

Attack the round's central inference: "with debug:disable_logs = 1 the core logger writes nothing, so a zero marker count in the session log or journal cannot show never-overflowed". Read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/S214.bin (Logger.cpp) fully and /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/S213.receipt.txt. Hunt for holes: does `m_logsEnabled` start true before config load (so early markers could be logged)? Could the hyprutils CLI logger (m_logger) be written to by another path that bypasses CLogger::log? Is the 21-core-line observation consistent with a logger that was enabled but quiet? Is "27,280 aquamarine lines" evidence the file channel is live for aquamarine only? Verdict per sub-claim: holds / overreaches / wrong, with the line that decides.
