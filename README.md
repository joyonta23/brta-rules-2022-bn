# RTR 2022 Knowledge Base

Digitized and structured source material for the Bangladesh Road Transport Rules, 2022 (`সড়ক পরিবহণ বিধিমালা, ২০২২`). The project contains OCR-generated HTML pages, source images, structured JSON datasets, and validation/conversion scripts.

The source law text is reproduced from public-domain government gazette content. The scripts and original dataset structure in this repository are licensed under the MIT License.

## Project layout

- `images/`: source page images
- `html/`: structured HTML pages
- `json/`: master and retrieval-augmented JSON datasets
- `scripts/`: OCR, conversion, and validation utilities
- `input/`: original input material
- `LICENSE`: MIT License for the original project code and structure

## Running the checks

From the `scripts` directory:

```powershell
python validate_html.py
python validate_json.py
python validate_rag_json.py
```

The scripts expect to be run from `scripts`, because their input paths are relative to that directory.

## OCR script configuration

The OCR script reads the Gemini credential from the `GEMINI_API_KEY` environment variable. Copy `.env.example` as a reference and set the variable in your local shell; do not commit credentials.