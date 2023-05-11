FROM python:3.8

WORKDIR /opt/app

COPY backend/configs/requirements.txt .

RUN pip3 install -r /opt/app/requirements.txt

COPY ./backend .

CMD python3 manage.py