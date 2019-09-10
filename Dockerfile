FROM python:3.7.4-slim-buster

COPY src/server.py .
COPY src/shared ./shared

EXPOSE 5672

CMD ["python", "server.py"]
