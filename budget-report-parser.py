import re
import csv

# Regular expressions
date_re = re.compile(r"— ([0-9/]+) ([0-9:]+ [APM]+)")
event_re = re.compile(
    r"([A-Z]+) » ([\w_]+) has been unfined \$([0-9,]+) by ([\w_]+) for:? (.+)"
)

rows = []
current_date = ""

with open("budget-input.txt", "r", encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()
        date_match = date_re.search(line)
        if date_match:
            current_date = f"{date_match.group(1)} {date_match.group(2)}"
            continue

        event_match = event_re.match(line)
        if event_match:
            department = event_match.group(1)
            user = event_match.group(2)
            amount = event_match.group(3).replace(",", "")
            by = event_match.group(4)
            reason = event_match.group(5).strip()
            event_text = f"{user} has been paid ${amount} by {by} for {reason}"
            rows.append([department, f"-{amount}", event_text, current_date])

# Write to output.csv with comma delimiter
with open("budget-report.csv", "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Department", "Amount", "Event", "Date"])
    writer.writerows(rows)

print("Done! Output written to budget-report.csv")
