from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Create default admin user if no user exists
    """
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'admin'
                print('Creating account for %s (%s)' % (username, email))
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()

                admin_user = User.objects.get(username=admin)

                # check admin User created succesfully
                if admin_user is not None:
                    self.stdout.write(self.style.SUCCESS('Successfully created User: "%s"' % admin_user.username))
                else:
                    self.stdout.write(self.style.ERROR('ERROR! Cannot create User: "%s"' % admin_user.username))
