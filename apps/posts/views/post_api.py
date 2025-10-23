from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models import Post
from apps.posts.services import PostService
from apps.posts.serializers import PostSerializer
from apps.users.models import User


class PostView(APIView):
    def get(self, request, user_id=None):
        try:
            if user_id:
                user = User.objects.get(id=user_id)
                posts = PostService.get_user_posts(user.id)
            else:
                posts = Post.objects.none()

            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
