from .models import Tag


class SectionMixin:
    """Добавляет в context section."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.request.resolver_match.url_name
        context['section'] = section
        return context


class TagMixin:
    def __init__(self, **kwargs) -> None:
        self.all_tags = Tag.objects.all()
        super().__init__(**kwargs)
