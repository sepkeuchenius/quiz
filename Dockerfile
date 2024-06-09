FROM python:3.12
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY *.py .
RUN mkdir src
CMD ["fastapi", "run", "main.py"]