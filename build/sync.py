import csv
import os
import io
import json
import collections
import requests

def read_csv(content):
    reader = csv.DictReader(io.StringIO(content))
    return list(reader)

SHEET_ID = '1yDEbtkPYLHMuIvC07B1fdvtmt-iM9SPsnhwkqWqG7dE'
SHEET_NAME = os.environ.get("SHEET", "")
if SHEET_NAME == "":
    raise RuntimeError("Please specify the sheet name")
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
response = requests.get(url)
response.raise_for_status()
parsed = read_csv(response.text)

MAP_BY_DATE = collections.defaultdict(list)
for item in parsed:
    MAP_BY_DATE[item.get("Date")].append(item)


for key, value in MAP_BY_DATE.items():
    filtered = collections.defaultdict(list)
    title = ""
    for item in value:
        if item.get("Category").lower() == "newsletter title":
            title = item
            continue
        filtered[item.get("Category", "")].append({
            k :v
            for k, v in item.items()
            if k not in ["Characters", "Date", "Category"]
        })
    output = json.dumps(dict(
        content=[
            {
                "category": cat,
                "stories": items,
            }
            for cat, items in filtered.items()
        ],
        title=title.get("Title"),
        date=title.get("Date"),
    ), indent=4)
    path = "./content/" + key.replace("/","-") + ".json"
    with open(path, "w") as out:
        out.write(output)
    print(f"Wrote {key} to {path} with {len(value)} items")
