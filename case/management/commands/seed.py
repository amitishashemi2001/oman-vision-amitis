from django.core.management.base import BaseCommand
from case.management.commands.CaseStepSeed import Command as CaseStepSeed
from case.management.commands.CaseSubStepSeed import Command as CaseSubStepSeed
from case.management.commands.CaseLogSeed import Command as CaseLogSeed
from accounts.management.commands.UserSeed import Command as UserSeed
from case.management.commands.CaseSeed import Command as CaseSeed
from case.management.commands.AdminInterfaceThemeSeed import Command as AdminInterfaceThemeSeed
class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        CaseStepSeed().handle()
        CaseSubStepSeed().handle()
        UserSeed().handle()
        CaseSeed().handle()
        CaseLogSeed().handle()
        AdminInterfaceThemeSeed().handle()
        self.stdout.write('done.')