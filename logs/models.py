from django.db import models
from django.utils import timezone


class Log(models.Model):
    ip_address = models.GenericIPAddressField()
    created_date = models.DateTimeField()  # datetime when log was created originally
    published_date = models.DateTimeField(auto_now=True, blank=True, null=True)  # datetime when log was added in DB
    http_method = models.CharField(max_length=10)
    uri = models.URLField(blank=True, null=True)  # URL + URN  http://almhuette-raith.at/administrator/index.php
    url = models.URLField(blank=True, null=True)  # http://almhuette-raith.at/administrator/
    urn = models.CharField(max_length=255)  # /administrator/index.php
    response_code = models.PositiveIntegerField()
    content_length = models.PositiveIntegerField()

    user_agent = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.ip_address
