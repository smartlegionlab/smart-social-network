from django.contrib import admin

from apps.posts.models import Post, PostLike, PostComment, PostCommentLike

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(PostCommentLike)
