FROM python:3.11-slim
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y
RUN pip install --no-cache-dir -r requirments.txt
ENTRYPOINT ["python3", "app.py"]