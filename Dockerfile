FROM python:3.9.7

LABEL AUTHOR="rikardoroa"

LABEL DESCRIPTION="A dockerfile container"

WORKDIR  /app

COPY . /app

COPY  requirements.txt app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r app/requirements.txt

ENV PYTHONUNBUFFERED=1

ENV FLASK_DEBUG=TRUE

EXPOSE 5000
EXPOSE 15672

CMD [ "python", "./main.py"]