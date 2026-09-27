import json
import os


json_file = "../json/RTR_2022_master.json"


with open(
    json_file,
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)



print("==============================")
print("RTR 2022 MASTER JSON CHECK")
print("==============================")



print(
    "Document:",
    data.get("document")
)



chapters = data.get(
    "chapters",
    []
)


print(
    "Total Chapters:",
    len(chapters)
)


rule_count = 0
sub_rule_count = 0
clause_count = 0



for chapter in chapters:

    for rule in chapter.get("rules", []):

        rule_count += 1

        for sub in rule.get("sub_rules", []):

            sub_rule_count += 1

            clause_count += len(
                sub.get("clauses", [])
            )



print(
    "Total Rules:",
    rule_count
)

print(
    "Total Sub Rules:",
    sub_rule_count
)

print(
    "Total Clauses:",
    clause_count
)


print("==============================")
print("Validation Completed")
print("==============================")