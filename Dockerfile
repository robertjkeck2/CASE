FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated swig git libpulse-dev python-dev libxml2-dev libxslt1-dev antiword poppler-utils pstotext tesseract-ocr \
    flac ffmpeg lame libmad0 libsox-fmt-mp3 sox && \
    apt-get upgrade -y --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated software-properties-common && \
    add-apt-repository ppa:webupd8team/java -y && \
    apt-get update && \
    echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
    apt-get install -y --allow-unauthenticated oracle-java8-installer && \
    apt-get clean
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 5000

# Migrates the database, uploads staticfiles, and runs the production server
CMD ["python", "app.py"]
