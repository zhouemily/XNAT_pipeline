#!/usr/bin/env python
#
#  #!/usr/local/bin/python absolute path for python this line can replace code at line one
#  The way at line one is better: it use env utility to invoke python with relative path (python could locate at /usr/bin or /usr/local/bin, etc
#

import os
import csv


DEBUG=1

root_path="/System/Volumes/Data/Volumes/CUPS/"
cups_id="sub-CUPS003"

##csv_file_path ='test.csv'  # Replace with the actual path to CSV file

csv_file_path =root_path+ 'PipelineOutputs/bids/derivatives/xcp/ses-A/xcp_minimal_aroma/'+cups_id+"/"+cups_id+'_ses-A_quality_aroma.csv'  
# Replace with the actual path to CSV file
key1="motionDVCorrInit"
key2="motionDVCorrFinal"
key3="estimatedLostTemporalDOF"

if DEBUG:
  print('DEBUG: csv_file_path='+csv_file_path)

# Initialize an empty dictionary to store the key-value pairs
data_dict = {}

# Check if the CSV file exists
try:
    with open(csv_file_path, 'r') as csvfile:
        lines = csvfile.readlines()
        if DEBUG:
            print("DEBUG: print out csv file content\n")
            for line in lines:
                print(line)
        
        # Check if there are at least two lines in the file
        if len(lines) >= 2:
            # Extract the keys (line 1) and values (line 2)
            keys = lines[0].strip().split(',')
            values = lines[1].strip().split(',')
            
            # Create key-value pairs and store them in the dictionary
            data_dict = dict(zip(keys, values))
        else:
            print("The CSV file does not contain enough data.")
        
except FileNotFoundError:
    print(f"The CSV file '{csv_file_path}' does not exist.")

# Print the extracted key-value pairs
for key, value in data_dict.items():
    print(f"Key: {key}, Value: {value}")

print(key1+"="+data_dict{key1}+"\n")
print(key2+"="+data_dict{key1}+"\n")
print(key3+"="+data_dict{key1}+"\n")
