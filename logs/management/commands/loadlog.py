from django.core.management.base import BaseCommand, CommandError
from logs.models import Log
import requests
import os

from apachelogs import LogParser

#  Init a parser with log format string: http://httpd.apache.org/docs/current/mod/mod_log_config.html
parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")


class Command(BaseCommand):
    help = 'Downloads Apache log file and inserts its events to database'

    def add_arguments(self, parser):
        parser.add_argument('log_url', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['log_url']:
            print(url)
            try:
                logfile_path = download_logfile_by_url(url)
                print(logfile_path)

            except Exception:
                raise CommandError('Error requesting file "%s"' % url)

            self.stdout.write(self.style.SUCCESS('Successfully downloaded and parsed log file "%s"' % url))
            self.stdout.write(f'Path to this file: {logfile_path}')


def download_logfile_by_url(url: str = '', path: str = 'data/') -> str:
    """
    downloads Apache log file to /data directory
    :param path: data folder path to save file into
    :param url: url to download Apache log file
    :return: downloaded file path
    """
    #  TODO add progress bar
    try:
        print(url)
        response = requests.get(url, stream=True)

    except requests.RequestException as e:
        print(e)
        return ''

    local_filename = url.split('/')[-1]

    full_path = path + local_filename

    print([f for f in os.scandir()])

    with open(full_path, 'wb') as log_file:
        for line in response.iter_lines(delimiter=b'\n'):
            if line:  # filter out keep-alive new lines TODO check necessarity
                #  TODO write to DB on a go
                log_file.write(line)
                log_file.flush()

    return full_path


def parse_file_to_db(path: str = '') -> int:
    #  TODO UPSERT
    """
    reads apache log file and inserts lines by chunked transactions to DB
    :param path: path to Apache log file
    :return: amount of rows inserted to DB
    """
    rows = 0

    # TODO dont forget to split URN part from URL


    return rows
