FROM python:3.9
WORKDIR /app/web-cache
COPY . .
CMD [ "python", "server.py"]
