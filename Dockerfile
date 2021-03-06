FROM python:3.9.10
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python3","src/app.py"]