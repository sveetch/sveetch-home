from django.core.management.base import CommandError, BaseCommand

from ...initial_loader import InitialDataLoader


class Command(BaseCommand):
    """
    Initial data loader.
    """
    help = (
        "Populate site with initial data loaded from a JSON file."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "dump",
            metavar="FILEPATH",
            help="Filepath to the JSON file with structure to load."
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("=== Loading initial data ===")
        )

        self.stdout.write("* Opened JSON source: {}".format(options["dump"]))

        maker = InitialDataLoader()
        maker.load(options["dump"])
