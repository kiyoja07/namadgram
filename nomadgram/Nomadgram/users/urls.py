from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('explore/', view=views.ExploreUsers.as_view(), name='explore_users'),
    path('<int:id>/follow/', view=views.FollowUser.as_view(), name='follow_user'),
    path('<int:id>/unfollow/', view=views.UnFollowUser.as_view(), name='unfollow_user'),
]



# from Nomadgram.users.views import (
#     user_list_view,
#     user_redirect_view,
#     user_update_view,
#     user_detail_view,
# )

# app_name = "users"
# urlpatterns = [
#     path("", view=user_list_view, name="list"),
#     path("~redirect/", view=user_redirect_view, name="redirect"),
#     path("~update/", view=user_update_view, name="update"),
#     path("<str:username>/", view=user_detail_view, name="detail"),
# ]
