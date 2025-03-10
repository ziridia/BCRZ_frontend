#!/bin/bash

# this script recursively travels through all test directories and creates a line in the report file
# for each test that is run. Report files are saved with the unix epoch appended in /testing/reports

traverse_subdirectories() {
  # Loop through each directory in the current directory
  for dir in */; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
      # Navigate into the directory
      cd "$dir"

      # check to see if `input.txt` is present
      # if it is, run the tests and comparisons
      if [ -f "input.txt" ]; then
        
        # call the test script
        bash $test_path $program_path $(pwd) $accounts_path

        # call the comparison script for console output
        bash $compare_output_path "$(pwd)/output.test" "$(pwd)/output.txt" "$(pwd)/input.txt" "$dir" "$report_path"
        # call the comparison script for transaction logs
        bash $compare_log_path "$(pwd)/transaction_log.test" "$(pwd)/transaction_log.txt" "$dir" "$report_path"

      fi
      

      # Recursively call the function on this subdirectory
      traverse_subdirectories
      # Navigate back to the previous directory
      cd ..
    fi
  done
}

# set variables
test_path=$(find "$(pwd)" -maxdepth 1 -type f -name "test.sh")
compare_output_path=$(find "$(pwd)" -maxdepth 1 -type f -name "compare_output.sh")
compare_log_path=$(find "$(pwd)" -maxdepth 1 -type f -name "compare_logs.sh")
accounts_path=$(find "$(pwd)" -maxdepth 1 -type f -name "CurrentBankAccounts")
program_path=$(find "$(pwd)/../" -maxdepth 1 -type f -name "main.py")

epoch_time=$(date +%s)
current_dir=$(pwd)

# add epoch timestamp for tracking different test results
report_path="${current_dir}/reports/report_${epoch_time}.txt"

# write template to the report file
echo -e "Path | pass/fail | actual output | expected output | input" > "$report_path"

# Call the function to start the process
traverse_subdirectories

# print where the report was saved to
echo "Report saved to $report_path"