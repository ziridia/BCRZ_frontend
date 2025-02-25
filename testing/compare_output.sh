#!/bin/bash

# Check if the correct number of arguments is provided
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <prog_output> <expected_output>"
  exit 1
fi

prog_output=$1
expected_output=$2

# Check if the necessary files exist
if [[ ! -f "$prog_output" || ! -f "$expected_output" ]]; then
  echo "Error: '$prog_output' or '$expected_output' file not found!"
  exit 1
fi

# Skip the first 3 lines of prog_output and compare the rest with expected_output
paste <(tail -n +4 "$prog_output") "$expected_output" | while IFS=$'\t' read -r prog_line expected_line; do
  # If the lines don't match, print them side by side
  if [[ "$prog_line" != "$expected_line" ]]; then
    echo "prog_output: $prog_line | expected_output: $expected_line"
  fi
done
