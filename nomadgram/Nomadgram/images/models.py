from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from Nomadgram.users import models as user_models
from taggit.managers import TaggableManager


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
    location = models.CharField(max_length=140) # CharField(): A string field, for small- to large-sized strings. max_length 설정이 필수
    caption = models.TextField() # TextField(): A large text field
    # ForeignKey field makes Many to One Relationship between models
    # on_delete=models.PROTECT -> ForeignKeyField가 바라보는 값이 삭제될 때 삭제가 되지않도록 ProtectedError를 발생시킨다.
    # on_delete=models.CASCADE -> ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 포함하는 모델 인스턴스(row)도 삭제된다.
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='images')
    tags = TaggableManager()

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

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