# apache_log_parser

##Getting started
1. Build your application container: `docker build -t apache-log-parser .`
2. Run previously built container: `docker run -d -it -p 8000:8000 --rm --name alp-app apache-log-parser`  

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