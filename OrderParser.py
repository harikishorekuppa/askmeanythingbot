import csv
import re
from collections import defaultdict

def extract_string_till_number(string):
    """Extracts the string up to the first occurrence of a number.

    Args:
        string: The input string.

    Returns:
        The extracted string, or the entire string if no number is found.
    """
    for i, char in enumerate(string):
        if char.isdigit():
            return string[:i].replace("-", "").strip()
    return string.strip()

def extract_number(string):
    match = re.search(r'\d+\.\d+|\d+', string)
    if match:
        return float(match.group())
    return None

def clean_item_name(item):
    """Cleans the item name by removing extra periods and spaces.

    Args:
        item: The item name.

    Returns:
        The cleaned item name.
    """
    return re.sub(r'\s+', ' ', item.replace('.', '').strip()).lower()

# Dictionary to store the merged results
merged_results = defaultdict(lambda: defaultdict(float))

with open('orders.txt', 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ')
    date = ''

    for row in csv_reader:
        line = "".join(row)
        if "morningorder" in line:
            date = re.sub(r'[^\d/]', '', line)
        else:
            item = clean_item_name(extract_string_till_number(line))
            number = extract_number(line)
            if number is not None:
                merged_results[date][item] += number

# Get all unique items
all_items = set()
for items in merged_results.values():
    all_items.update(items.keys())

# Write to CSV
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date'] + sorted(all_items)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for date, items in merged_results.items():
        row = {'Date': date}
        for item in all_items:
            row[item] = items.get(item, 0)
        writer.writerow(row)
