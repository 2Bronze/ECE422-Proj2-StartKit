FROM python:3.11-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python3", "scaler.py"]
