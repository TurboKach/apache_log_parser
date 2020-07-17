from sys import getsizeof

import requests
from apachelogs import LogEntry, LogParser
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from logs.models import Log

#  Init a parser with log format string: http://httpd.apache.org/docs/current/mod/mod_log_config.html
log_parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%l\"")


class Command(BaseCommand):
    """
    Custom management command:
    python manage.py loadlog <url:str> (-s, --size <int>)
    """
    help = 'Download Apache log file and insert its events to database.\n' \
           'Pass a -s or --size argument with value in Megabytes to set size limit for downloading a file'

    def add_arguments(self, parser):
        # positional arguments
        parser.add_argument(
            'log_url',
            nargs='?',
            type=str,
        )

        # named (optional) arguments
        parser.add_argument(
            '-s',
            '--size',
            nargs='?',
            type=int,
            default=0,
            action='store',
            help='size limit for downloading a file in MB'
        )

    def handle(self, *args, **options):

        if options['log_url'] is None:
            raise CommandError('URL could not be empty!')

        else:
            url = options['log_url']

            if options['size'] < 0:
                size = options['size']
                raise ValueError(f'Invalid size: {size}')

            try:
                logfile_path = download_logfile_by_url(url, max_size=options['size'])

                self.stdout.write(self.style.SUCCESS('Successfully downloaded and parsed log file "%s"' % url))
                self.stdout.write(f'Local path to file: {logfile_path}')

            except Exception as e:
                raise CommandError(f'Error requesting file.\n{e}')


def download_logfile_by_url(url: str = '', max_size: int = 0, path: str = 'data/') -> str:
    """
    downloads Apache log file to data/ directory and writes its lines into DB
    :param url: url to download Apache log file
    :param max_size: size limit for downloading a part of file
    :param path: data folder path to save file into
    :return: downloaded file path
    """
    downloaded_total = 0

    max_size = max_size * 1e+6  # convert to bytes

    try:
        response = requests.get(url, stream=True)

        content_length = int(response.headers.get('Content-Length', 0))

        # initialize progress bar with total file size
        progress_bar = tqdm(
            desc="Downloading log file",
            total=content_length,
            unit='B',
            unit_scale=True
        )

    except requests.RequestException as e:
        print(e)
        raise

    except Exception as e:
        print(e)
        raise

    local_filename = url.split('/')[-1]

    full_path = path + local_filename

    with open(full_path, 'wb') as log_file:

        # iterate over the file by lines to prevent its content at once
        for line in response.iter_lines(delimiter=b'\n'):

            if line:  # filter out keep-alive new lines

                # if set maximum download size reached
                if downloaded_total >= max_size > 0:
                    progress_bar.close()
                    return full_path

                try:
                    # get byte size of loaded line
                    line_size = getsizeof(line)

                    # write log line to local storage
                    log_file.write(line + b'\n')
                    log_file.flush()

                    # prepare loaded log to save in DB
                    log_entry = log_parser.parse(line.decode("utf-8"))
                    log = parse_log_entry_to_log_model(log_entry)
                    write_log_to_db(log)

                    # update progress bar with downloaded size
                    progress_bar.update(line_size)

                    # accumulate total downloaded bytes to check if limit exceeded
                    downloaded_total += line_size

                except Exception as e:
                    print(e)
                    raise

        progress_bar.close()

    return full_path


def write_log_to_db(log: Log):
    """
    Saves apache Log instance to DB
    :param log: Log class instance
    :return:
    """
    return log.save()


def parse_log_entry_to_log_model(logentry: LogEntry) -> Log:
    """
    Converts LogEntry instance to apache DB model Log
    :param logentry: LogEntry object instance
    :return: Log object instance
    """
    if logentry is None:
        return Log()

    url = logentry.headers_in["Referer"]
    urn = logentry.request_line.split()[1]
    uri = url  # TODO correctly concatenate URI from URL+URN

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

    log.clean_fields()

    return log
