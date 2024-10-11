import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('traffic_control_final.csv')


# Function to create labels for specific workflows
def create_short_label(full_label):
    # Extract the last word after '/' for specific workflow_name entries
    if (full_label.endswith('.github/workflows/ansible.molecule.fo.yml') or
            full_label.endswith('.github/workflows/ansible.molecule.todb.yml') or
            full_label.endswith('ghcr.io/${{ github.repository }}/ci/trafficserver-alpine')):
        return full_label.split('/')[-1].split('.')[0]  # Get the word before the '.'
    else:
        # Split the label into words and return the first two, or full label if it's short
        words = full_label.split()
        return ' '.join(words[:2]) if len(words) >= 2 else full_label


# Apply the function to shorten the workflow names
df['short_workflow'] = df['workflow_name'].apply(create_short_label)

# Aggregate data by short_workflow, label and measure the size and sum for bubble size
aggregated_data = df.groupby(['short_workflow', 'label']) \
    .agg({'files_changed': ['size', 'sum']}) \
    .reset_index()

# Rename columns for easier access
aggregated_data.columns = ['short_workflow', 'label', 'count', 'files_changed_sum']

# Create a scatter plot, where bubble size is proportional to the files_changed_sum
fig, ax = plt.subplots()

# Loop through each label type and plot them as separate scatter plots
for label in aggregated_data['label'].unique():
    # Filter for each label type
    label_data = aggregated_data[aggregated_data['label'] == label]

    # Create scatter plot (bubble chart)
    ax.scatter(x=label_data['short_workflow'], y=label_data['count'],
               s=label_data['files_changed_sum'],  # Bubble sizes
               label=f'Label {label}', alpha=0.6)  # Label for the legend and transparency

# Adding labels, title, and legend
ax.set_xlabel('Workflow')
ax.set_ylabel('Count of Files Changed')
ax.set_title('Bubble Chart of Workflows with Files Changed')
ax.legend()

# Rotate x-axis labels for readability
plt.xticks(rotation=45, ha='right')

# Set y-axis to logarithmic if large range (optional)
ax.set_yscale('log')
ax.set_yticks([1, 10, 100], minor=False)
ax.set_yticklabels(['1', '10', '100'], minor=False)

# Show grid
ax.grid(True)

# Save the figure to a file
plt.savefig('bubble_chart.pdf', bbox_inches='tight')

# Display the plot
plt.show()
