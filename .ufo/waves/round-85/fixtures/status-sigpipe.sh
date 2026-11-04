#!/bin/sh
# round-85 contained producer: keeps writing until the downstream reader closes the pipe, so
# the guarded pipeline's status is the producer's death by SIGPIPE (128+13), not the reader's 0
awk 'BEGIN { for (i = 0; i < 20000; i++) print "MADO_STATUS: sigpipe line " i }'
