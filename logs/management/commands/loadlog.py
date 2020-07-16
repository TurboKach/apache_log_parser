from django.core.management.base import BaseCommand, CommandError
from logs.models import Log
import requests
import os

from apachelogs import LogParser, LogEntry

#  Init a parser with log format string: http://httpd.apache.org/docs/current/mod/mod_log_config.html
log_parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%l\"")


class Command(BaseCommand):
    help = 'Downloads Apache log file and inserts its events to database'

    def add_arguments(self, parser):
        parser.add_argument('log_url', nargs='+', type=str)

    def handle(self, *args, **options):
        for url in options['log_url']:
            try:
                logfile_path = download_logfile_by_url(url)

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
        response = requests.get(url, stream=True)
        file_size = response.headers.get('Content-Length')
        print(file_size)

    except requests.RequestException as e:
        print(e)
        return ''

    local_filename = url.split('/')[-1]

    full_path = path + local_filename

    with open(full_path, 'wb') as log_file:
        for line in response.iter_lines(delimiter=b'\n'):
            if line:  # filter out keep-alive new lines TODO check necessarity
                #  TODO write to DB on a go

                try:
                    log_line = log_parser.parse(line.decode("utf-8"))
                    parse_logline_to_db(log_line)
                except Exception as e:
                    print(e)

                log_file.write(line + b'\n')
                log_file.flush()

    return full_path


def parse_logline_to_db(logentry: LogEntry) -> Log:
    url = logentry.headers_in["Referer"]
    urn = logentry.request_line.split()[1]
    uri = url.replace(urn, '')
    log = Log(
        ip_address=logentry.remote_host,
        created_date=logentry.request_time,
        http_method=logentry.request_line.split()[0],
        uri=uri,
        url=url,
        urn=urn,
        response_code=logentry.final_status,
        content_length=logentry.bytes_sent,
        user_agent=logentry.headers_in["User-Agent"],
    )
    log.save()


def write_log_to_db(log: Log = '') -> int:
    #  TODO UPSERT
    """
    reads apache log file and inserts lines by chunked transactions to DB
    :param path: path to Apache log file
    :return: amount of rows inserted to DB
    """
    rows = 0

    # TODO dont forget to split URN part from URL

    return rows
