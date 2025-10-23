

class LikeableMixin:
    def get_likes_count(self):
        return self.likes.count()

    def toggle_like(self, user):
        like, created = self.likes.get_or_create(user=user)
        if not created:
            like.delete()
        return created

    def has_liked(self, user):
        return self.likes.filter(user=user).exists()
