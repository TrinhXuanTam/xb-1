from django.core.management.base import BaseCommand
from datetime import date

from xb1.articles.models import Article

class Command(BaseCommand):
    def handle(self, **options):
        today = date.today()

        Article.objects.filter(published_from__date=today).update(article_state=Article.PUBLISHED)
        Article.objects.filter(published_to__date=today).update(article_state=Article.HIDDEN)
