FROM python:3.8.2-alpine

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY hub.py hub.py

CMD ["python3", "-u", "hub.py"]
