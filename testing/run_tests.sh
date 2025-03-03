#!/bin/bash

# Check if the correct number of arguments is provided
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <prog> <prog_input>"
  exit 1
fi

prog=$1
prog_input=$2
prog_output="prog_output"

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
cat "$prog_input" | python ./"$prog" > "$prog_output"

echo "Output has been saved to $prog_output"
