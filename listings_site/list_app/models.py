from django.db import models


class Listing(models.Model):
    last_edit_date = models.DateTimeField('date last edited')
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    creator_email = models.CharField(max_length=100)
    edit_token = models.CharField(max_length=16)
