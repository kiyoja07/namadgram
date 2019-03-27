from rest_framework import serializers # To translate JSON <-> Python objects
from . import models
from Nomadgram.users import serializers as user_serializers
from Nomadgram.images import serializers as image_serializers

class NotificationSerializer(serializers.ModelSerializer):

    creator = user_serializers.ListUserSerializer()
    image = image_serializers.SmallImageSerializer()

    class Meta:
        model = models.Notification
        fields = '__all__'