from django.db import models
from Nomadgram.users import models as user_models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True => It saves the current date and time to the model when he is created
    updated_at = models.DateTimeField(auto_now=True) # auto_now=True => It saves the current date and time to the model when he is updated

    # Abstract model do not save on the database but is used by other models to extend from it
    class Meta: 
        abstract = True 

@python_2_unicode_compatible  # only if you need to support Python 2
class Image(TimeStampedModel):

    """ Image Model """

    file = models.ImageField()
    location = models.CharField(max_length=140) # CharField에는 max_length 설정이 필수
    caption = models.TextField()
    # ForeignKey field makes Many to One Relationship between models
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='images')

    @property
    def like_count(self):
        return self.likes.all().count()

    # change the string representation of the model
    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

    class Meta:
        ordering = ['-created_at'] # 기본값은 오름차순으로 정렬하고 -를 붙이면 내림차순으로 정렬

@python_2_unicode_compatible  # only if you need to support Python 2
class Comment(TimeStampedModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, related_name='comments')

    def __str__(self):
        return self.message

@python_2_unicode_compatible  # only if you need to support Python 2
class Like(TimeStampedModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, related_name='likes')

    def __str__(self):
        return 'User:{} - Image Caption:{}'.format(self.creator.username, self.image.caption)