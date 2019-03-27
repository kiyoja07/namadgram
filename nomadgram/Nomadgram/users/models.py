from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    """ User Model """

    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('not-specified', 'Not specified')
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    profile_image = models.ImageField(null=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    website = models.URLField(null = True)
    bio = models.TextField(null = True)
    phone = models.CharField(max_length = 140, null = True)
    gender = models.CharField(max_length = 80, choices = GENDER_CHOICE, null = True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followers_set") # blank=True를 추가하여 필수가 아니라, 선택필드로 지정
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followings_set")

    def __str__(self):
        return self.username

    @property
    def post_count(self):
        return self.images.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()
