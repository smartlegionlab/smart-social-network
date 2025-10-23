from django.core.paginator import Paginator


class CachedCountPaginator(Paginator):
    def __init__(self, object_list, per_page, total_count=None, **kwargs):
        super().__init__(object_list, per_page, **kwargs)
        self._cached_count = total_count

    @property
    def count(self):
        if self._cached_count is not None:
            return self._cached_count
        return super().count
