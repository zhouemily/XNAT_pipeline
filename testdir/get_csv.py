#!/usr/bin/env python
#
#  #!/usr/local/bin/python absolute path for python this line can replace code at line one
#  The way at line one is better: it use env utility to invoke python with relative path (python could locate at /usr/bin or /usr/local/bin, etc
#

import os
import csv

DEBUG=1

##csv_file_path = 'PipelineOutputs/bids/derivatives/xcp/ses-A/xcp_minimal_aroma/sub-CUPS003/sub-CUPS003_ses-A_quality_aroma.csv'  # Replace with the actual path to your CSV file
cups_id=sub-CUPS003
csv_file_path = 'PipelineOutputs/bids/derivatives/xcp/ses-A/xcp_minimal_aroma/'+cups_id+"/sub-CUPS003/cups_id+'_ses-A_quality_aroma.csv'  # Replace with the actual path to your CSV file
if DEBUG:
  print('DEBUG: csv_file_path='+csv_file_path)

"""
if os.path.exists(csv_file_path):
    # The CSV file exists
    # Proceed to open and extract data
else:
    print(f"The CSV file '{csv_file_path}' does not exist.")
"""

######################################################################
#In this code:
#1. open the CSV file and read it using the csv module.
#2. use the next(csvreader) function to read the first row (header) and store it in the header variable.
#3. use next(csvreader) again to read the second row (data) and store it in the data variable.
#4. create key-value pairs by zipping the header and data lists together and convert them into a dictionary, data_dict.
#5. Finally, print the key-value pairs extracted from the CSV file.
###########################################

#
# Initialize an empty dictionary to store the key-value pairs
data_dict = {}

# Check if the CSV file exists
try:
    with open(csv_file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)      
        # Read the header row (first row) to get column names (keys)
        header = next(csvreader)
        # Read the data row (second row) to get values
        data = next(csvreader)
        # Create key-value pairs and store them in the dictionary
        data_dict = dict(zip(header, data))    
except FileNotFoundError:
    print(f"The CSV file '{csv_file_path}' does not exist.")
except StopIteration:
    print("The CSV file is empty or missing data.")
# Print the extracted key-value pairs
for key, value in data_dict.items():
    print(f"Key: {key}, Value: {value}")
