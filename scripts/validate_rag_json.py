import json


json_file = "../json/RTR_2022_RAG.json"


with open(
    json_file,
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)



print("==============================")
print("RTR 2022 RAG JSON CHECK")
print("==============================")


print(
    "Total chunks:",
    len(data)
)



empty_source_pages = []
empty_content = []
duplicate_ids = []


ids = []



for item in data:


    # Check source page

    if not item.get("source_page"):

        empty_source_pages.append(
            item.get("id")
        )


    # Check content

    if not item.get("content", "").strip():

        empty_content.append(
            item.get("id")
        )


    # Collect IDs

    ids.append(
        item.get("id")
    )



# Find duplicate IDs

for item_id in ids:

    if ids.count(item_id) > 1:

        duplicate_ids.append(
            item_id
        )



duplicate_ids = list(
    set(duplicate_ids)
)



print()

print(
    "Empty source_page:",
    len(empty_source_pages)
)


print(
    "Empty content:",
    len(empty_content)
)


print(
    "Duplicate IDs:",
    len(duplicate_ids)
)



print("==============================")
print("Validation Completed")
print("==============================")