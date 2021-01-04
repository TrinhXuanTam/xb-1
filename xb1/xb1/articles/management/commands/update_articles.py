from django.core.management.base import BaseCommand
from django.utils import timezone

from xb1.articles.models import Article

class Command(BaseCommand):
    def handle(self, **options):
        today = timezone.now().date()

        # Publish hidden articles
        Article.objects \
            .filter(published_from__date=today, article_state=Article.HIDDEN) \
            .update(article_state=Article.PUBLISHED)

        # Hide published articles
        Article.objects \
            .filter(published_to__date=today, article_state=Article.PUBLISHED) \
            .update(article_state=Article.HIDDEN)
