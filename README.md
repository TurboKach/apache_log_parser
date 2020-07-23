# apache_log_parser

## Getting started
1. Build and up your containers: `docker-compose -f docker-compose.prod.yml up -d --build`  
2. Visit http://127.0.0.1:1337/ to see it works  
3. Login as `admin:admin`


Custom Django management commands:
 - `python manage.py loadlog <url:str>`  
 download apache log file into *data/* project directory and parse its lines to database.  
 *additional params:*  
 `-s, --size` - Megabytes size limit for downloading a part of log file.  
 *example:*  
 `python manage.py loadlog https://raw.githubusercontent.com/TurboKach/apache_log_parser/master/test_data/test_access.log --size 1`  
 above example downloads first 1 MB of log file.
 
 - `python manage.py initadmin`  
 create default admin user if no user exists.  
 this command also executed on container run.
