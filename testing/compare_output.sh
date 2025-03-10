#!/bin/bash

# this script compares the terminal output of the test and the program

# Check if the correct number of arguments is provided
if [[ $# -ne 5 ]]; then
  echo "Usage: $0 <prog_output> <expected_output> <input file> <test name> <report file>"
  exit 1
fi

# set variables based on parameters
prog_output=$1
expected_output=$2
input_file=$3
test_name=$4
report_file_path=$5

# Check if the necessary files exist
if [[ ! -f "$prog_output" || ! -f "$expected_output" ]]; then
  echo "Error: '$prog_output' or '$expected_output' file not found!"
  exit 1
fi

# set flag for whether there were any failures
passed=1

while IFS=$'\t' read -r prog_line expected_line input_line; do
  # If the lines don't match, print them side by side
  if [[ "$prog_line" != "$expected_line" ]]; then
    echo -e "$test_name | fail | $prog_line | $expected_line | $input_line"  >> "$report_file_path"
    passed=0
  fi
done < <(paste <(tail -n +4 "$prog_output") "$expected_output" "$input_file")

# Check the final value of 'passed' after the loop
if [[ $passed -eq 1 ]]; then
  echo -e "$test_name\t pass" >> "$report_file_path"
fi