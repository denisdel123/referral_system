import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from userApp.models import User

load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create_superuser(
            phone_number=os.environ.get("PHONE_SUPERUSER"),
            password=os.environ.get("PASSWORD_SUPERUSER")
        )
