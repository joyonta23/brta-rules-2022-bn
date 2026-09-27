import os
from bs4 import BeautifulSoup


# HTML folder location
html_folder = "../html"


# Reports
total_files = 0
empty_files = []
unclear_files = []
broken_files = []
missing_structure_files = []


# Get all HTML files
files = sorted(os.listdir(html_folder))


for file in files:

    if file.endswith(".html"):

        total_files += 1

        path = os.path.join(
            html_folder,
            file
        )


        # Read HTML file
        try:
            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:
                content = f.read()


        except Exception as e:
            broken_files.append(file)
            continue



        # Check empty file
        if len(content.strip()) == 0:
            empty_files.append(file)



        # Check OCR uncertainty
        if "[UNCLEAR]" in content:
            unclear_files.append(file)



        # Check HTML parsing
        try:

            soup = BeautifulSoup(
                content,
                "html.parser"
            )


            # Check legal structure exists
            has_structure = (
                soup.find("h2")
                or soup.find("rule")
                or soup.find("sub_rule")
                or soup.find("clause")
            )


            if not has_structure:
                missing_structure_files.append(file)


        except Exception:
            broken_files.append(file)



# Final Report

print("\n========== RTR 2022 HTML VALIDATION ==========\n")


print("Total HTML pages:", total_files)



print("\nEmpty files:")
if empty_files:
    for file in empty_files:
        print("-", file)
else:
    print("None")



print("\nPages containing [UNCLEAR]:")
if unclear_files:
    for file in unclear_files:
        print("-", file)
else:
    print("None")



print("\nPages without legal structure:")
if missing_structure_files:
    for file in missing_structure_files:
        print("-", file)
else:
    print("None")



print("\nBroken HTML files:")
if broken_files:
    for file in broken_files:
        print("-", file)
else:
    print("None")



print("\n==============================================")
print("Validation completed.")