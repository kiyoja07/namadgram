from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from Nomadgram.notifications import views as notification_views


class Feed(APIView):

    # handle a GET request on an APIView
    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list =[]

        for following_user in following_users:

            user_images = following_user.images.all()[:2] # following_user의 image 전체 중 앞의 2개를 선택

            for image in user_images:

                image_list.append(image)

        # 내가 생성한 최근 이미지 2개도 피드에 포함
        my_images = user.images.all()[:2]

        for image in my_images:

            image_list.append(image)

        # image.created_at의 역순으로 정렬
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        # Response class which allows you to return content that can be rendered into multiple content types, depending on the client request.
        return Response(serializer.data)


class LikeImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        # find the image
        try:
            found_image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image
            )

            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator = user,
                image = found_image
            )

            new_like.save()

            # 좋아요 완료 된 후 알림 생성
            notification_views.create_notification(user, found_image.creator, 'like', found_image)


            return Response(status=status.HTTP_201_CREATED)


class UnlikeImage(APIView):

    def delete(self, request, image_id, format=None):

        # find the image
        try:
            found_image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image
            )

            preexisting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:

            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        # find the image
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # create a new comment
        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():
            
            serializer.save(creator=user, image=found_image)

            # 댓글 완료 된 후 알림 생성
            notification_views.create_notification(user, found_image.creator, 'comment', found_image, serializer.data['message'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        # delete the image
        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtags', None)

        if hashtags is not None:

            hashtags = hashtags.split(",") # string -> array

            images =  models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):

        user = request.user

        try:
            comment_to_delete = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetail(APIView):

    def get(self, request, image_id, format=None):

        user = request.user

        try:
            image = models.Image.objects.get(id = image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ImageSerializer(image)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# class ListAllImages(APIView):

#     def get(self, request, format=None):
        
#         all_images = models.Image.objects.all()

#         serializer = serializers.ImageSerializer(all_images, many=True)

#         return Response(data=serializer.data)

# class ListAllComments(APIView):

#     def get(self, request, format=None):

#         all_comments = models.Comment.objects.all()

#         serializer = serializers.CommentSerializer(all_comments, many=True)

#         return Response(data=serializer.data)

# class ListAllLikes(APIView):

#     def get(self, request, format=None):

#         all_likes = models.Like.objects.all()

#         serializer = serializers.LikeSerializer(all_likes, many=True)

#         return Response(data=serializer.data)