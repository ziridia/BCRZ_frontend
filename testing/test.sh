#!/bin/bash

# this script runs the program and feeds the input into it

# Check if the correct number of arguments is provided
if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <program path> <test directory> <current bank accounts file path>"
  exit 1
fi

prog=$1
prog_input="$2/input.txt"
prog_output="$2/output.test"
log_output="$2/transaction_log.test"
accounts_path="$3"

# run the program and pipe the test input in
# then pipe program output to the output file
cat "$prog_input" | python "$prog" log=$log_output accounts=$accounts_path > "$prog_output"

# echo "Output has been saved to $prog_output"
