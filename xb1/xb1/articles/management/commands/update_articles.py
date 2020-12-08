from django.core.management.base import BaseCommand
from datetime import date

from xb1.articles.models import Article

class Command(BaseCommand):
    def handle(self, **options):
        today = date.today()

        Article.objects.filter(published_from__date__lte=today, article_state=Article.HIDDEN).exclude(published_to__date__lte=today).update(article_state=Article.PUBLISHED)
        Article.objects.filter(published_to__date__lte=today, article_state=Article.PUBLISHED).update(article_state=Article.HIDDEN)
