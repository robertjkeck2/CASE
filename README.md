# CASE
**C**ASE: **A** **S**ummarization **E**xpert...Summarizes your cases when you just don't have enough time in the day.

## Basic Usage

Dockerized Usage:
1. Download Docker and make sure it is running on your device.
2. Clone this repository at https://github.com/robertjkeck2/CASE.git.
3. Navigate to the cloned repo and build the Docker container using:
  `docker build CASE .`
4. Run the container with port forwarding using the command:
  `docker run -p 5000:5000 CASE`
5. Navigate to http://127.0.0.1:5000 and choose a .pdf file from Canvas.
6. Select the desired number of sentences for each section and press Upload.

Non-Docker Usage:
1. Download both the case2txt.py and summarize.py files, along with requirements.txt.
2. Set up a virtualenv and `pip install -r requirements.txt`
3. If you are missing dependencies, try to install all required using error messages.
4. Download a case PDF from Canvas.
5. Use the command `python case2txt.py case_pdf_name.pdf` to convert the PDF to a JSON and .txt file.
6. Use the command `python summarize.py case_pdf_name.pdf` to summarize the case.

