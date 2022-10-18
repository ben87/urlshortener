from django.db import models

class TinyURL(models.Model):
    # customised url link
    alias = models.CharField(max_length=10, primary_key=True)
    # long url for redirection
    long_url = models.URLField()