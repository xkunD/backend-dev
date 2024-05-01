FROM python:3.7

RUN mkdir usr/app
WORKDIR user/app

COPY . .

RUN pip3 install -r requirements.txt

CMD python app.py