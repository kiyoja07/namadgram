from django.urls import path
from . import views

app_name = "images"

# URL 경로들을 파이썬 콜백 함수들("views")로 연결
# as_view() : 클래스로 진입하기 위한 진입 메소드를 제공
urlpatterns = [
    path("", view=views.Images.as_view(), name="feed"), 
    path("<int:image_id>/", view=views.ImageDetail.as_view(), name="image_detail"),
    path("<int:image_id>/likes/", view=views.LikeImage.as_view(), name="like_image"),
    path("<int:image_id>/unlikes/", view=views.UnlikeImage.as_view(), name="unlike_image"),
    path("<int:image_id>/comments/", view=views.CommentOnImage.as_view(), name="comment_image"),
    path("<int:image_id>/comments/<int:comment_id>/", view=views.ModerateComments.as_view(), name="moderate_comments"),
    path("comments/<int:comment_id>/", view=views.Comment.as_view(), name="comment"),
    path("search/", view=views.Search.as_view(), name="search"),
]

# urlpatterns = [
#     path("all/", view=views.ListAllImages.as_view(), name="all_imaes"), # as_view() : Returns a callable view that takes a request and returns a response
#     path("comments/", view=views.ListAllComments.as_view(), name="all_comments"),
#     path("likes/", view=views.ListAllLikes.as_view(), name="all_likes"),
# ]
