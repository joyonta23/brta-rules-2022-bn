import json


input_file = "../json/RTR_2022_master.json"

output_file = "../json/RTR_2022_RAG.json"


with open(
    input_file,
    "r",
    encoding="utf-8"
) as f:
    data = json.load(f)



rag_documents = []



for chapter in data["chapters"]:

    chapter_name = chapter["chapter"]


    for rule in chapter["rules"]:

        rule_no = rule["rule_no"]
        title = rule.get("title", "")



        for sub in rule.get("sub_rules", []):


            sub_rule_no = sub.get(
                "sub_rule_no",
                ""
            )


            base_content = sub.get(
                "text",
                ""
            )


            source_page = sub.get(
                "source_page",
                ""
            )



            # ----------------------------
            # Sub-rule level chunk
            # ----------------------------

            if base_content.strip():

                rag_documents.append({

                    "id":
                    f"RTR_2022_{source_page}_RULE_{rule_no}_SUB_{sub_rule_no}",


                    "act_code":
                    "RTR_2022",


                    "doc_type":
                    "Rule",


                    "source_title":
                    data["document"],


                    "section_or_clause":
                    f"বিধি {rule_no}({sub_rule_no})",


                    "source_page":
                    source_page,


                    "doc_category":
                    "PRIMARY",


                    "subject":
                    title,


                    "offence_type":
                    "",


                    "applicable_vehicle_types":
                    "",


                    "penalty":
                    "",


                    "content":
                    f"""
আইন:
{data["document"]}

অধ্যায়:
{chapter_name}

বিধি:
{rule_no} - {title}

উপ-বিধি:
{sub_rule_no}

বিষয়:
{title}

মূল বক্তব্য:
{base_content}
""".strip(),


                    "language":
                    "bn",


                    "tags":
                    [
                        chapter_name,
                        title,
                        f"বিধি {rule_no}"
                    ],


                    "status":
                    "active",


                    "last_verified":
                    "2026-09-15"

                })




            # ----------------------------
            # Clause level chunks
            # ----------------------------

            for clause in sub.get(
                "clauses",
                []
            ):


                clause_no = clause.get(
                    "clause_no",
                    ""
                )


                clause_source_page = clause.get(
                    "source_page",
                    source_page
                )


                rag_documents.append({

                    "id":
                    f"RTR_2022_{clause_source_page}_RULE_{rule_no}_SUB_{sub_rule_no}_CLAUSE_{clause_no}",


                    "act_code":
                    "RTR_2022",


                    "doc_type":
                    "Clause",


                    "source_title":
                    data["document"],


                    "section_or_clause":
                    f"বিধি {rule_no}({sub_rule_no})({clause_no})",


                    "source_page":
                    clause_source_page,


                    "doc_category":
                    "PRIMARY",


                    "subject":
                    title,


                    "offence_type":
                    "",


                    "applicable_vehicle_types":
                    "",


                    "penalty":
                    "",


                    "content":
                    f"""
আইন:
{data["document"]}

অধ্যায়:
{chapter_name}

বিধি:
{rule_no} - {title}

উপ-বিধি:
{sub_rule_no}

দফা:
({clause_no})

বিষয়:
{title}

মূল বক্তব্য:
{clause["text"]}
""".strip(),


                    "language":
                    "bn",


                    "tags":
                    [
                        chapter_name,
                        title,
                        f"বিধি {rule_no}",
                        f"দফা {clause_no}"
                    ],


                    "status":
                    "active",


                    "last_verified":
                    "2026-09-15"

                })




with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        rag_documents,
        f,
        ensure_ascii=False,
        indent=2
    )



print("==============================")
print("RAG JSON CREATED")
print("==============================")


print(
    "Total chunks:",
    len(rag_documents)
)


print(
    "Saved:",
    output_file
)