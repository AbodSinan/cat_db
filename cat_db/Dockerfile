FROM python:3.7

COPY . app

RUN pip3 install uwsgi && \
    pip3 install -r app/requirements.txt


EXPOSE 8000

CMD ["python", "./app/manage.py", "runserver", "0.0.0.0:8000"]
