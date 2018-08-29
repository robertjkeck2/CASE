# CASE
**C**ASE: **A** **S**ummarization **E**xpert...Summarizes your cases when you just don't have enough time in the day.

## Basic Usage

1. Download both the case2txt.py and summarize.py files, along with requirements.txt.
2. Set up a virtualenv and `pip install -r requirements.txt`
3. If you are missing dependencies, try to install all required using error messages.
4. Download a case PDF from Canvas.
5. Use the command `python case2txt.py case_pdf_name.pdf` to convert the PDF to a JSON and .txt file.
6. Use the command `python summarize.py case_pdf_name.pdf` to summarize the case.

## TODO

- Dockerize for simpler dependency management
