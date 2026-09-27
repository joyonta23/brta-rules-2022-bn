from google import genai
from PIL import Image
import os


API_KEY = os.environ["GEMINI_API_KEY"]


client = genai.Client(
    api_key=API_KEY
)


model_name = "gemini-3-flash-preview"


image_folder = "../images"
output_folder = "../html"


os.makedirs(output_folder, exist_ok=True)


prompt = """
You are digitizing the Bangladesh Gazette:

সড়ক পরিবহণ বিধিমালা, ২০২২

Convert this scanned legal page into structured HTML.

Rules:

1. Preserve Bengali text exactly.
2. Do not summarize.
3. Do not rewrite legal wording.
4. Preserve:
   - অধ্যায় (Chapter)
   - বিধি (Rule)
   - উপ-বিধি (Sub-rule)
   - দফা (Clause)
   - তফসিল (Schedule)
   - Tables


HTML structure:

For chapters:

<h2>Chapter name</h2>


For rules:

<rule number="বাংলা সংখ্যা">
<title>Rule title</title>
</rule>


For sub-rules like (১), (২), (৩):

<sub_rule id="বাংলা সংখ্যা">
Text
</sub_rule>


For clause letters like (ক), (খ), (গ):

<clause id="বাংলা অক্ষর">
Text
</clause>


Additional rules:

- Ignore repeated Gazette headers, page numbers, printed price, registration numbers, and document metadata that appear in page headers or footers.
- Preserve exact Bengali spelling, punctuation, and word spacing from the source image. Do not normalize or correct language.
- Do not merge separate Bengali words.
- If content continues from a previous page, treat it as continuation of the existing Chapter → Rule → Sub_rule → Clause hierarchy.
- Do not create a new rule unless a new বিধি number appears.
- Do not create a new sub_rule unless a new sub-rule number appears.
- Do not create a new clause unless a new clause letter appears.
- Maintain hierarchy:
  Chapter → Rule → Sub_rule → Clause.
- Do not add explanations, comments, or extra HTML outside the extracted legal content.
- Remove clause markers like (ক), (খ), (গ) from clause text because they are already represented in the clause id attribute.

If a word is unclear write:

[UNCLEAR]

Return only HTML.
"""


# PROCESS ALL PAGES WITH RESUME SUPPORT

files = sorted(os.listdir(image_folder))


for file in files:

    if file.endswith(".png"):


        output_file = file.replace(
            ".png",
            ".html"
        )


        output_path = os.path.join(
            output_folder,
            output_file
        )


        # Skip already completed pages
        if os.path.exists(output_path):
            print("Skipping:", file)
            continue


        print("Processing:", file)


        img = Image.open(
            os.path.join(image_folder, file)
        )


        try:

            response = client.models.generate_content(
                model=model_name,
                contents=[
                    prompt,
                    img
                ]
            )


        except Exception as e:

            print("Error processing:", file)
            print(e)


            # Stop when quota finishes
            if "429" in str(e):

                print("Quota finished. Stop processing.")
                break


            # Skip temporary server errors
            if "503" in str(e):

                print("Gemini server busy. Skipping:", file)
                continue


            continue



        html = response.text


        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)



print("Completed")