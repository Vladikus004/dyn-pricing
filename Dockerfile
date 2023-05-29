FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]