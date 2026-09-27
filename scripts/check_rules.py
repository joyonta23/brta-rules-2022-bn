import json

with open(
    "../json/RTR_2022_master.json",
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)


rules = []

for chapter in data["chapters"]:
    for rule in chapter["rules"]:
        rules.append(rule["rule_no"])


print("Total rules:", len(rules))

print("Rules:")
print(rules)