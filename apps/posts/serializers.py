from rest_framework import serializers

from apps.posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author_id',
            'author_name',
            'content',
            'created_at',
            'avatar',
        ]

    def get_avatar(self, obj):
        obj.author.get_avatar_url()

    def get_author_name(self, obj):
        return obj.author.full_name

    def get_author_id(self, obj):
        return obj.author.id
