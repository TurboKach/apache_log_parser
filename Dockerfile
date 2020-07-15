FROM python:3.8-alpine

MAINTAINER Maxim Karpov <incognito@turbokach.me>

WORKDIR /usr/src/app

#  копируем из папки с докерфайлом в workdir (<src> -> <docker_filesystem>)
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#  копируем из папки с докерфайлом всё в workdir
COPY . .

RUN python manage.py loadlog https://raw.githubusercontent.com/TurboKach/apache_log_parser/master/data/test_access.log

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

# container launch hints
# docker build -t my-python-app .
# docker run -it -p 8000:8000 --rm --name my-running-app my-python-app