#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 0 ]; then
    echo "Usage: $0"
    exit 1
fi

# Define an array of strings
#strings=("CUPS003" "CUPS004" "CUPS005" "CUPS008" "CUPS009")
strings=('CUPS003' 'CUPS005' 'CUPS006' 'CUPS008' 'CUPS009' 'CUPS010' 'CUPS012' 'CUPS013' 'CUPS015' 'CUPS016' 'CUPS017' 'CUPS018' 'CUPS019' 'CUPS022' 'CUPS023' 'CUPS027' 'CUPS029' 'CUPS030' 'CUPS035' 'CUPS037' 'CUPS039' 'CUPS040' 'CUPS041' 'CUPS042' 'CUPS044' 'CUPS047' 'CUPS048' 'CUPS051' 'CUPS053' 'CUPS054' 'CUPS055' 'CUPS056' 'CUPS057' 'CUPS058' 'CUPS059' 'CUPS060' 'CUPS061' 'CUPS062' 'CUPS064' 'CUPS065' 'CUPS066')

# Loop through the array and run the Python script with each string
for string_arg in "${strings[@]}"; do
    echo "Running with argument: $string_arg"
    python XNAT_file_pipeline.py -id "$string_arg"
done

