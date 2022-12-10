FROM python:3.10-slim

RUN pip install pipenv

WORKDIR /opt

COPY Pipfile Pipfile.lock .

RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

EXPOSE 5030

CMD uvicorn app.main:create_app --factory --host 0.0.0.0 --port 5030 --reload