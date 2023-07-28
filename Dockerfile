FROM python:3.11

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY . /server/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80", "--reload"]