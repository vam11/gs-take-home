from django.contrib.auth.models import User, Group
from rest_framework import serializers

from geosite.sysinfo.models import Request


class SimpleRequestSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    req_type = serializers.IntegerField(read_only=True, required=False)
    req_date = serializers.DateTimeField(read_only=True, required=False)
    comment = serializers.CharField()

    def create(self, validated_data):
        return Request.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.req_type = validated_data.get('req_type', instance.req_type)
        instance.req_date = validated_data.get('req_date', instance.req_date)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
