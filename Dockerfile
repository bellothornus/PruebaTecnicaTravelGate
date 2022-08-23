FROM python:3

RUN apt-get update -y && \
    apt-get install python3-pip python-dev -y

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python","main.py","production"]