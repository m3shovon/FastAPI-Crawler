# serializers.py
from rest_framework import serializers

class CrawlRequestSerializer(serializers.Serializer):
    url = serializers.URLField()
