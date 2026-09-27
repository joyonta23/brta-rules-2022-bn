import json

file = "../json/RTR_2022_RAG.json"

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0

for item in data:

    if item.get("subject","").strip() == "":
        count += 1

print("Empty subjects:", count)