import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
data = pd.read_csv('traffic_control_final.csv')

# Filter data for run failures
failures = data[data['run_conclusion'] == 'failure'].copy()

# Determine the event type and corresponding time for each failure
failures['time'] = failures.apply(lambda row: row['pull_request_created_at'] if row['event'] == 'pull_request' else row['commit_date'], axis=1)

# Aggregate the data based on class, affected files, workflow name, and run failure reasons
failures_by_class = failures['class'].value_counts()
affected_files = failures.groupby('files_changed').size().reset_index(name='counts')

# Convert the time column to datetime for timeline plotting
failures['time'] = pd.to_datetime(failures['time'])

# Save the prepared data for analysis into a new CSV file
prepared_data_path = 'workflows.csv'
failures.to_csv(prepared_data_path, index=False)


# Pie chart for the distribution of run failures by class (TD vs. Not_TD)
plt.figure(figsize=(8, 8))
plt.pie(failures_by_class, labels=failures_by_class.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Run Failures by Class')
plt.savefig('distribution.pdf')
plt.show()


# Timeline chart for the time distribution of run failures, segmented by class (TD or Not_TD)
plt.figure(figsize=(14, 7))
sns.scatterplot(x='time', y='run_number', hue='class', style='workflow_name', data=failures)
plt.title('Time Distribution of Run Failures by Class (TD or Not_TD) and Workflow Name')
plt.xlabel('Time')
plt.ylabel('Run Number')
plt.savefig('time_distribution.pdf')
plt.show()