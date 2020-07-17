FROM python:3.8-alpine

MAINTAINER Maxim Karpov <incognito@turbokach.me>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

#  copy requirements to workdir (<src> -> <docker_filesystem>)
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#  copy project folder contents to workdir
COPY . .


EXPOSE 8000

CMD ["/usr/src/app/runserver.sh"]
# as an alternative
#  python manage.py createsuperuser --username=admin --email=admin@example.com

# populate DB with test data
#RUN python manage.py loadlog https://raw.githubusercontent.com/TurboKach/apache_log_parser/master/test_data/test_access.log

# container launch hints
# docker build -t my-python-app .
# docker run -it -p 8000:8000 --rm --name my-running-app my-python-app