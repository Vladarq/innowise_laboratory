FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN ["pip", "install", "-r", "requirements.txt"]
# project code is only in main.py, need to copy only that one file
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]