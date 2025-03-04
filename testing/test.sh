#!/bin/bash

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

# Check if the necessary files exist
# if [[ ! -f "$prog" || ! -f "$prog_input" ]]; then
#   echo "Error: '$prog' or '$prog_input' file not found!"
#   exit 1
# fi

# Open the prog_input file and read line by line
# while IFS= read -r line
# do
#   # Pass each line from prog_input as input to prog and save the output
#   echo "$line" | python ./"$prog" >> "$prog_output"
# done < "$prog_input"

# run the program and pipe the test input in
# then pipe program output to the output file
cat "$prog_input" | python "$prog" log=$log_output accounts=$accounts_path > "$prog_output"

# echo "Output has been saved to $prog_output"
