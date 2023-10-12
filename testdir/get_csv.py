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

if os.path.exists(csv_file_path):
    # The CSV file exists
    # Proceed to open and extract data
else:
    print(f"The CSV file '{csv_file_path}' does not exist.")

if os.path.exists(csv_file_path):
    # The CSV file exists
    with open(csv_file_path, 'r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            # Access the values by column headers
            key = row['Column1']  # Replace 'Column1' with your actual column name
            value = row['Column2']  # Replace 'Column2' with your actual column name
            
            # Process the key and value as needed
            print(f"Key: {key}, Value: {value}")
