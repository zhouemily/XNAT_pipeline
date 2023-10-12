


# Define the path to your CSV file
csv_file_path = 'your_csv_file.csv'  # Replace with the actual path to your CSV file

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
