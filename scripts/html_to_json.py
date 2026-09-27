import os
import json
from bs4 import BeautifulSoup


# ----------------------------
# Paths
# ----------------------------

html_folder = "../html"
json_folder = "../json"

os.makedirs(json_folder, exist_ok=True)


output_file = os.path.join(
    json_folder,
    "RTR_2022_master.json"
)


# ----------------------------
# Bengali number converter
# ----------------------------

bn_digits = "০১২৩৪৫৬৭৮৯"


def bn_to_int(value):

    number = ""

    for ch in value:

        if ch in bn_digits:
            number += str(
                bn_digits.index(ch)
            )

    return int(number) if number else 0



def int_to_bn(value):

    value = str(value)

    result = ""

    for ch in value:

        result += bn_digits[int(ch)]

    return result



# ----------------------------
# Main JSON structure
# ----------------------------

data = {

    "document":
    "সড়ক পরিবহণ বিধিমালা, ২০২২",

    "chapters": []

}


files = sorted(
    os.listdir(html_folder)
)


current_chapter = None
current_rule = None


# ----------------------------
# Track rule sequence
# ----------------------------

last_rule_number = 0



# ----------------------------
# Process HTML pages
# ----------------------------

for file in files:


    if not file.endswith(".html"):
        continue


    print(
        "Processing:",
        file
    )


    source_page = file.replace(
        ".html",
        ""
    )


    file_path = os.path.join(
        html_folder,
        file
    )


    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()



    soup = BeautifulSoup(
        html,
        "html.parser"
    )



    # ----------------------------
    # Chapter detection
    # ----------------------------

    chapter = soup.find("h2")


    if chapter:

        current_chapter = {

            "chapter":
            chapter.get_text(
                " ",
                strip=True
            ),

            "source_page":
            source_page,

            "rules":
            []

        }


        data["chapters"].append(
            current_chapter
        )


    if current_chapter is None:
        continue



    # ----------------------------
    # Rule extraction
    # ----------------------------

    rules = soup.find_all(
        "rule"
    )



    for rule in rules:



        raw_rule_no = rule.get(
            "number",
            ""
        )


        detected_number = bn_to_int(
            raw_rule_no
        )


        # ----------------------------
        # Fix duplicated OCR numbers
        # ----------------------------

        if detected_number <= last_rule_number:

            detected_number = (
                last_rule_number + 1
            )


        last_rule_number = detected_number


        rule_no = int_to_bn(
            detected_number
        )



        rule_id = (

            f"RTR_2022_"
            f"{source_page}_"
            f"RULE_{rule_no}"

        )



        rule_data = {


            "id":
            rule_id,


            "source_page":
            source_page,


            "rule_no":
            rule_no,


            "title":
            "",


            "sub_rules":
            []

        }



        # ----------------------------
        # Rule title
        # ----------------------------

        title = rule.find(
            "title"
        )


        if title:

            rule_data["title"] = title.get_text(
                " ",
                strip=True
            )


        elif current_rule and current_rule.get("title"):

            rule_data["title"] = current_rule["title"]




        # ----------------------------
        # Sub rules
        # ----------------------------

        sub_rules = rule.find_all(
            "sub_rule",
            recursive=False
        )



        for sub in sub_rules:



            sub_no = sub.get(
                "id",
                ""
            )


            sub_id = (

                f"{rule_id}_"
                f"SUB_{sub_no}"

            )



            sub_data = {


                "id":
                sub_id,


                "source_page":
                source_page,


                "sub_rule_no":
                sub_no,


                "text":
                "",


                "clauses":
                []

            }




            clauses = sub.find_all(
                "clause",
                recursive=False
            )



            for clause in clauses:



                clause_no = clause.get(
                    "id",
                    ""
                )



                sub_data["clauses"].append({


                    "id":
                    f"{sub_id}_CLAUSE_{clause_no}",


                    "source_page":
                    source_page,


                    "clause_no":
                    clause_no,


                    "text":
                    clause.get_text(
                        " ",
                        strip=True
                    )


                })





            # Remove clauses before text extraction

            sub_copy = BeautifulSoup(
                str(sub),
                "html.parser"
            )


            for c in sub_copy.find_all(
                "clause"
            ):

                c.extract()



            sub_data["text"] = sub_copy.get_text(
                " ",
                strip=True
            )



            rule_data["sub_rules"].append(
                sub_data
            )





        current_chapter["rules"].append(
            rule_data
        )


        current_rule = rule_data




# ----------------------------
# Save JSON
# ----------------------------

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )



print()

print("==============================")
print("MASTER JSON CREATED")
print(output_file)
print("==============================")