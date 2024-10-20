import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
data = pd.read_csv('dataset/traffic_control_final.csv')

# Filter data for workflow run triggered by pull request
commit = data[data['event'] == 'push'].copy()

# Determine the event type and corresponding time for each run
commit['time'] = commit.apply(lambda row: row['commit_date'], axis=1)

# Aggregate the data based on class, affected files, workflow name
commit_label = commit['class'].value_counts()

affected_files = commit.groupby('files_changed').size().reset_index(name='counts')

# Convert the time column to datetime for timeline plotting
commit['time'] = pd.to_datetime(commit['time'])

# Save the prepared data for analysis into a new CSV file
prepared_data_path = 'data/prepared_data1.csv'
commit.to_csv(prepared_data_path, index=False)


# Pie chart for the TD distribution within workflow runs triggered by commit
plt.figure(figsize=(8, 8))
plt.pie(commit_label, labels=commit_label.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of TD within Workflow run that are triggered by commits')
plt.savefig('pie_chart.png')
plt.show()


# Plot for the TD distribution over time, segmented by class (TD or Not_TD)
plt.figure(figsize=(14, 7))
sns.scatterplot(x='time', y='run_number', hue='class', style='workflow_name', data=commit)
plt.title('TD distribution within workflows over time')
plt.xlabel('Time')
plt.ylabel('Workflow_run Number')
plt.savefig('td_distribution_overTime.png')
plt.show()