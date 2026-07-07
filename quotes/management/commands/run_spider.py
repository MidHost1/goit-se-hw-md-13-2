from django.core.management.base import BaseCommand
from quotes.utils.scraper import run_my_spider

class Command(BaseCommand):
    help = 'Запуск скрапера для збору цитат'

    def handle(self, *args, **options):
        run_my_spider()
        self.stdout.write(self.style.SUCCESS('Скрапінг завершено успішно!'))