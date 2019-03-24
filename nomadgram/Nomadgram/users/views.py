from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class ExploreUsers(APIView):

    def get(self, request, format=None):

        # 가입시간 기준으로 최근 5명 유저 가져오기
        last_five = models.User.objects.all().order_by('-date_joined')[:5]

        # 최근 5명 유저의 정보 가져오기
        serializer = serializers.ExploreUserSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FollowUser(APIView):

    def post(selfe, request, id, format=None):

        user = request.user # access the data sent in a POST request

        try:
            user_to_follow = models.User.objects.get(id = id) # 팔로우 할 유저 찾기
        except models.User.DoesNotExist: # 팔로우할 유저를 찾지 못했을 때
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 유저 팔로잉 리스트에 추가
        user.following.add(user_to_follow) # add a object to a ManyToMany Relationship

        # 팔로잉한 유저의 팔로워 리스트에 추가
        user_to_follow.followers.add(user)

        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):

    def post(selfe, request, id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id = id) # 언팔로우 할 유저 찾기
        except models.User.DoesNotExist: # 언팔로우할 유저를 찾지 못했을 때
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 유저 팔로잉 리스트에서 삭제
        user.following.remove(user_to_follow) # remove an object from a ManyToMany Relationship

        # 언팔로잉한 유저의 팔로워 리스트에서 삭제
        user_to_follow.followers.remove(user)

        return Response(status=status.HTTP_200_OK)



# from django.contrib.auth import get_user_model
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse
# from django.views.generic import DetailView, ListView, RedirectView, UpdateView

# User = get_user_model()


# class UserDetailView(LoginRequiredMixin, DetailView):

#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"


# user_detail_view = UserDetailView.as_view()


# class UserListView(LoginRequiredMixin, ListView):

#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"


# user_list_view = UserListView.as_view()


# class UserUpdateView(LoginRequiredMixin, UpdateView):

#     model = User
#     fields = ["name"]

#     def get_success_url(self):
#         return reverse("users:detail", kwargs={"username": self.request.user.username})

#     def get_object(self):
#         return User.objects.get(username=self.request.user.username)


# user_update_view = UserUpdateView.as_view()


# class UserRedirectView(LoginRequiredMixin, RedirectView):

#     permanent = False

#     def get_redirect_url(self):
#         return reverse("users:detail", kwargs={"username": self.request.user.username})


# user_redirect_view = UserRedirectView.as_view()
