FROM node:latest as build-stage
WORKDIR /code
COPY ./src/frontend /code
RUN npm install
RUN npm run build

FROM python:3.7
WORKDIR /code
COPY --from=build-stage /code/build /code/src/frontend/build
COPY ./ /code
RUN pip install poetry && poetry config settings.virtualenvs.create false && poetry install
WORKDIR /code/src
RUN python manage.py makemigrations api
RUN python manage.py migrate
RUN python manage.py collectstatic
CMD gunicorn -w 3 -b 0.0.0.0:8000 --access-logfile - --error-logfile - --log-level debug backend.wsgi