FROM python:3.11-slim

RUN pip install -r requiremets.txt

CMD ["python", "app/main.py"]

