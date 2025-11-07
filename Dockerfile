FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "ustore.wsgi:application", "--bind", "0.0.0.0:8000"]
