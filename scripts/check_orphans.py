import json


file = "../json/RTR_2022_master.json"


with open(
    file,
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)



orphan_count = 0


for chapter in data["chapters"]:

    for rule in chapter["rules"]:

        for sub in rule["sub_rules"]:

            if "_ORPHAN" in sub.get("id", ""):

                orphan_count += 1

                print(
                    "ORPHAN FOUND:",
                    sub["id"]
                )



print("==============================")
print(
    "Total orphan clauses:",
    orphan_count
)
print("==============================")