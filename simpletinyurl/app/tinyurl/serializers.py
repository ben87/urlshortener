from django.urls import reverse
from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import TinyURL

class TinyURLSerializer(serializers.ModelSerializer):
    # Allow blank and only alphanumeric is allowed
    alias = serializers.RegexField(
        regex='^[a-zA-Z0-9]*$', min_length=5, max_length=10,
        allow_blank=True,
        validators=[
            UniqueValidator(
                queryset=TinyURL.objects.all(),
                message='Alias is not available'
            )
        ]
    )
    long_url = serializers.URLField(required=True, allow_blank=False)
    alias_url = serializers.SerializerMethodField('get_alias_url')

    def get_alias_url(self, obj):
        return '{}{}'.format(settings.HOST, reverse('alias', args=(obj.alias,)))

    class Meta:
        model = TinyURL
        fields = ('alias', 'long_url', 'alias_url')