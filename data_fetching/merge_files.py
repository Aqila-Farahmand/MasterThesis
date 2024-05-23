import csv
import os

# Directory containing CSV files
directory = os.path.join(os.getcwd(), 'cache')

# List to store data from all CSV files
merged_data = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        # Open CSV file
        with open(filepath, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            # Skip header if needed
            next(csvreader)
            # Read data from CSV file
            for row in csvreader:
                merged_data.append(row)

# Write merged data to a new CSV file
output_file = 'merged_data.csv'
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header if needed
    # csvwriter.writerow(['Column1', 'Column2', ...])
    # Write data to CSV file
    csvwriter.writerows(merged_data)

print("Merged CSV file saved as:", output_file)
