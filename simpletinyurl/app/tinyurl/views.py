from urllib.parse import urlparse

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.core.cache import cache

from rest_framework import generics

from .serializers import TinyURLSerializer
from .models import TinyURL


def index(request):
    # home/landing page
    return render(request, 'tinyurl/index.html')


def alias(request, alias):
    # alias/redirect path
    
    # retrieve alias from cache
    url = cache.get(alias)
    if url is None:
        url = get_object_or_404(TinyURL, alias=alias).long_url
        cache.set(alias, url)

    return redirect(url)


class TinyURLCreateAPI(generics.CreateAPIView):
    # Create API
    serializer_class = TinyURLSerializer

    def create(self, request, *args, **kwargs):
        # override create, generate random alias when alias is empty
        if request.data.get('alias', '') == '':
            # random generated value
            random_alias = get_random_string(length=10)
            while TinyURL.objects.filter(alias=random_alias).exists():
                random_alias = get_random_string(length=10)
            request.data['alias'] = random_alias
        # add simple url validation
        parse_result = urlparse(request.data.get('long_url', ''))
        if parse_result.scheme == '':
            request.data['long_url'] = parse_result._replace(
                scheme='http').geturl().replace('//', '/')
        return super(TinyURLCreateAPI, self).create(request, *args, **kwargs)