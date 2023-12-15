import json
import re
from collections import Counter
import matplotlib.pyplot as plt

def load_json_file(file_path):
    """
    Load and return JSON data from a file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def categorize_security_issues(json_data):
    """
    Categorize security issues into critical, major, minor, and less impacting.
    """
    # Regular expressions for different categories of data
    critical_pattern = r'(?i)"password"\s*:\s*"[^"]+"'
    major_pattern = r'(?i)"api_key"\s*:\s*"[^"]+"'
    minor_pattern = r'(?i)"email"\s*:\s*"[^"]+"'
    less_impacting_pattern = r'(?i)"username"\s*:\s*"[^"]+"'

    # Finding matches
    critical_issues = re.findall(critical_pattern, json.dumps(json_data))
    major_issues = re.findall(major_pattern, json.dumps(json_data))
    minor_issues = re.findall(minor_pattern, json.dumps(json_data))
    less_impacting_issues = re.findall(less_impacting_pattern, json.dumps(json_data))

    # Counting issues
    issues_counter = Counter({'Critical': len(critical_issues),
                              'Major': len(major_issues),
                              'Minor': len(minor_issues),
                              'Less Impacting': len(less_impacting_issues)})

    return issues_counter

def plot_security_issues(issues_counter):
    """
    Plot the distribution of security issues in a pie chart with color coding.
    """
    # Check if there are any issues to plot
    if sum(issues_counter.values()) == 0:
        print("No security issues found.")
        return

    labels = issues_counter.keys()
    sizes = issues_counter.values()
    colors = ['red', 'orange', 'yellow', 'green']  # Color coding

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=(0.1, 0, 0, 0))
    ax.axis('equal')

    plt.title('Categorized Security Issues in JSON Data')
    plt.show()


file_path = '/content/20230831_061926_discussion_sharings.json'
json_data = load_json_file(file_path)
security_issues = categorize_security_issues(json_data)
plot_security_issues(security_issues)
