FROM python:3.13.3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "fastapi","app/main.py", "--host", "0.0.0.0", "--port", "8000" ]

# docker build -t fastapi
# docker images