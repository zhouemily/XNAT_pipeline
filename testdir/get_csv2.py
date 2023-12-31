#!/usr/bin/env python
#
#  #!/usr/local/bin/python absolute path for python this line can replace code at line one
#  The way at line one is better: it use env utility to invoke python with relative path (python could locate at /usr/bin or /usr/local/bin, etc
#

import os
import csv

DEBUG=1
cups_id=sub-CUPS003
##csv_file_path = 'PipelineOutputs/bids/derivatives/xcp/ses-A/xcp_minimal_aroma/sub-CUPS003/sub-CUPS003_ses-A_quality_aroma.csv'  # Replace with the actual path to CSV file
csv_file_path = 'PipelineOutputs/bids/derivatives/xcp/ses-A/xcp_minimal_aroma/'+cups_id+"/sub-CUPS003/cups_id+'_ses-A_quality_aroma.csv'  
# Replace with the actual path to CSV file

if DEBUG:
  print('DEBUG: csv_file_path='+csv_file_path)

# Initialize an empty dictionary to store the key-value pairs
data_dict = {}

# Check if the CSV file exists
try:
    with open(csv_file_path, 'r') as csvfile:
        lines = csvfile.readlines()
        
        # Check if there are at least three lines in the file
        if len(lines) >= 3:
            # Extract the keys (line 2) and values (line 3)
            keys = lines[1].strip().split(',')
            values = lines[2].strip().split(',')
            
            # Create key-value pairs and store them in the dictionary
            data_dict = dict(zip(keys, values))
        else:
            print("The CSV file does not contain enough data.")
        
except FileNotFoundError:
    print(f"The CSV file '{csv_file_path}' does not exist.")

# Print the extracted key-value pairs
for key, value in data_dict.items():
    print(f"Key: {key}, Value: {value}")
