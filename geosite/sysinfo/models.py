from django.db import models
from django.utils import timezone


class Request(models.Model):

    # In order to be efficient, the request type can be an integer since there will
    # only be handful of options. sqlite should maintain that as a 1 byte integer
    req_type = models.IntegerField()
    req_date = models.DateTimeField(default=timezone.now)

    # It seems that sqlite does not enforce the length of VARCHAR
    # so there is no point right now to specify something like max_length=40
    comment = models.CharField(null=True, max_length=40)

    class Meta:
        db_table = 'requests'
