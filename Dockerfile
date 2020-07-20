FROM python:3.8.3-alpine

MAINTAINER Maxim Karpov <incognito@turbokach.me>

WORKDIR /usr/src/app

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# create folder for static files
RUN mkdir /usr/src/app/staticfiles

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

#  copy requirements to workdir (<src> -> <docker_filesystem>)
#COPY requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

#  copy project
COPY . .


EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

#CMD ["/usr/src/app/runserver.sh"]
# as an alternative
#  python manage.py createsuperuser --username=admin --email=admin@example.com

# populate DB with test data
#RUN python manage.py loadlog https://raw.githubusercontent.com/TurboKach/apache_log_parser/master/test_data/test_access.log

# container launch hints
# docker build -t my-python-app .
# docker run -it -p 8000:8000 --rm --name my-running-app my-python-app