FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN pip install unittest-xml-reporting

RUN python -m unittest discover -s app/tests -p "*.py"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]