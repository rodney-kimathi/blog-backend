FROM python:3.12.3-alpine

WORKDIR /usr/src/blog

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["fastapi", "run", "app/main.py"]
