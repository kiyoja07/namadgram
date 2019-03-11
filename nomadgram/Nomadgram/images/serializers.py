from rest_framework import serializers # To translate JSON <-> Python objects
from . import models
from Nomadgram.users import models as user_models


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )


class CommentSerializer(serializers.ModelSerializer):

    creator= FeedUserSerializer()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator'
        )



class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    # likes = LikeSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count', 
            'creator'
        )