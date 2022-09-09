# build env
FROM python:3.8-slim
RUN mkdir /app
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY foodgram/ /app
WORKDIR /app
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic
CMD ["python3", "manage.py", "runserver", "0:8000"]
