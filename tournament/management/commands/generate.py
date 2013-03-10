from django.core.management.base import BaseCommand, CommandError
from tournament.models import Tournament, Matchup


class Command(BaseCommand):
    args = '<tournamet_id> <randomize_seeds>'
    help = 'Generates matchups for the given tournament'

    def handle(self, *args, **options):
        try:
            tournament_id = args[0]
            shuffle = True if args[1] else False
        except:
            raise CommandError('Invalid argument')

        try:
            c = Matchup.objects.filter(tournament=tournament_id).count()
            if c > 0:
                self.stdout.write('Deleting %s old matchups\n' % c)
                Matchup.objects.filter(tournament=tournament_id).delete()
            tournament = Tournament.objects.get(pk=int(tournament_id))
        except Tournament.DoesNotExist:
            raise CommandError('Tournamet "%s" does not exist' % tournament_id)

        if shuffle:
            tournament.randomize_seeds()
        tournament.generate()
        self.stdout.write('Successfully generated tournament matchups for: %s\n' % tournament.name)
