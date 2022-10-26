FROM python:3.11
WORKDIR /app/web-cache
COPY . .
CMD [ "python", "server.py"]
