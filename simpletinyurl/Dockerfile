FROM python:alpine
WORKDIR /code

COPY ./requirements.txt .
COPY ./entrypoint.sh .
COPY ./app app
RUN pip install -r requirements.txt

RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["sh", "/code/entrypoint.sh"]