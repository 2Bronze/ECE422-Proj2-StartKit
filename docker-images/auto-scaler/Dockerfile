FROM python:3.11-alpine
ARG SERVICE_ID
ADD . /code
WORKDIR /code
VOLUME ["/var/run/docker.sock"]
RUN pip install -r requirements.txt
CMD ["python3", "scaler.py", "$SERVICE_ID"]
