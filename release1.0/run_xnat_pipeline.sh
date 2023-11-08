#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 0 ]; then
    echo "Usage: $0"
    exit 1
fi

# Define an array of strings
strings=("CUPS003" "CUPS004" "CUPS005" "CUPS008" "CUPS009")

# Loop through the array and run the Python script with each string
for string_arg in "${strings[@]}"; do
    echo "Running with argument: $string_arg"
    python XNAT_file_pipeline.py -id "$string_arg"
done
