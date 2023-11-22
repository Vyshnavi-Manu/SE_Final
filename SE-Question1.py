# -*- coding: utf-8 -*-
import json
import re
from collections import Counter
import matplotlib.pyplot as plt
import netsparker
import openvas
import pyt
import yosai


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        print(f"Line {e.lineno}, Column {e.colno}: {e.msg}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def check_security_issues(data):
    issues_counter = Counter()

    # Check for passwords, addresses, names, and keys
    for key, value in recursive_items(data):
        if isinstance(value, str):
            if re.search(r'\bpassword\b|\bpass\b', key, re.IGNORECASE):
                issues_counter['Passwords'] += 1
            if re.search(r'\baddress\b', key, re.IGNORECASE):
                issues_counter['Addresses'] += 1
            if re.search(r'\bname\b', key, re.IGNORECASE):
                issues_counter['Names'] += 1
        elif isinstance(value, (int, float)):
            if key.lower() == 'key':
                issues_counter['Keys'] += 1

    return issues_counter
#recursive function
def recursive_items(item):
    if isinstance(item, dict):
        for key, value in item.items():
            yield key, value
            yield from recursive_items(value)
    elif isinstance(item, list):
        for value in item:
            yield from recursive_items(value)

def plot_security_issues(issues_counter):
    if issues_counter:
        labels, values = zip(*issues_counter.items())
        plt.bar(labels, values)
        plt.xlabel('Security Issues')
        plt.ylabel('Count')
        plt.title('Security Issues in JSON File')
        plt.show()
    else:
        print("No security issues found.")

def main():
    file_path = '/content/users_100.json'
    json_data = read_json_file(file_path)

    if json_data:
        issues_counter = check_security_issues(json_data)
        print("Security Issues:")
        for issue, count in issues_counter.items():
            print(f"{issue}: {count}")

        plot_security_issues(issues_counter)

if __name__ == '__main__':
    main()
