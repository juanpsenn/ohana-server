from django.core.management.base import BaseCommand

from app.events.tests.factories.events import EventFactory


class Command(BaseCommand):
    help = "Creates events and related models instance for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument("n", type=int)

    def handle(self, *args, **options):
        for _ in range(options["n"]):
            EventFactory()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {options["n"]} events.')
        )
