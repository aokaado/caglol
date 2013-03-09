from django.core.management.base import BaseCommand, CommandError
from tournament.models import Tournament


class Command(BaseCommand):
    args = '<tournamet_id>'
    help = 'Generates matchups for the given tournamet'

    def handle(self, *args, **options):
        try:
            tournament_id = args[0]
        except:
            raise CommandError('Invalid argument')

        try:
            tournament = Tournament.objects.get(pk=int(tournament_id))
        except Tournament.DoesNotExist:
            raise CommandError('Tournamet "%s" does not exist' % tournament_id)

        tournament.generate()
        tournament.generated = True
        self.stdout.write('Successfully generated tournamet matchups for "%s"' % tournament_id)
