FROM python:3.11-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["sudo", "/usr/local/bin/python3 scaler.py"]
