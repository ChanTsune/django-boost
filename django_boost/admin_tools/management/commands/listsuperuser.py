from django.contrib.auth import get_user_model

from django_boost.core.management import BaseCommand


class Command(BaseCommand):
    """List super users."""

    help = "List super users."

    def handle(self, *args, **options):
        User = get_user_model()
        qureyset = User.objects.filter(is_superuser=True)
        for user in qureyset:
            self.stdout.write(str(user))
