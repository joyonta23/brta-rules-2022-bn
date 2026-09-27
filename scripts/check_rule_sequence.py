import json


with open(
    "../json/RTR_2022_master.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)


rules = []

locations = []


for chapter in data["chapters"]:

    for rule in chapter["rules"]:

        rules.append(rule["rule_no"])

        locations.append({
            "rule_no": rule["rule_no"],
            "id": rule["id"],
            "page": rule["source_page"]
        })


print("Total rules:", len(rules))


print("\nDuplicate rule numbers:")

seen = {}

for i, r in enumerate(rules):

    if r in seen:

        print(
            "Duplicate:",
            r,
            "positions:",
            seen[r],
            "and",
            i+1
        )

    else:
        seen[r] = i+1



print("\nMissing expected numbers:")

expected = [
    str(i)
    for i in range(1,168)
]


for num in expected:

    if num not in rules:

        print("Missing:", num)



print("\nDuplicate locations:")

for item in locations:

    if rules.count(item["rule_no"]) > 1:

        print(item)