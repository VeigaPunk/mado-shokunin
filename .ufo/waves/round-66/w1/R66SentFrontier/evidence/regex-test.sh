#!/usr/bin/env bash
set -u
marker='MADO_CITECHECK: rev=abc123 files=1 citations=1 resolved=1 missing=0 skipped_large=0 verdict=TARGET_MET (VERSION 1)'
if [[ "$marker" =~ \ citations=([0-9]+)\ resolved=([0-9]+)\ missing=([0-9]+)\  ]]; then
  echo "REGEX_MATCH"
else
  echo "REGEX_NO_MATCH rc=$?"
fi
m2='MADO_CITECHECK: rev=abc123 files=1 citations=1 resolved=1 missing=0  skipped_large=0 verdict=TARGET_MET'
if [[ "$m2" =~ \ citations=([0-9]+)\ resolved=([0-9]+)\ missing=([0-9]+)\  ]]; then echo "REGEX2_MATCH"; else echo "REGEX2_NO_MATCH"; fi
