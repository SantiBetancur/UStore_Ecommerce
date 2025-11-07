from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


class Command(BaseCommand):
    help = 'Set up Google OAuth SocialApp for django-allauth'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client-id',
            type=str,
            help='Google OAuth Client ID',
        )
        parser.add_argument(
            '--secret',
            type=str,
            help='Google OAuth Client Secret',
        )

    def handle(self, *args, **options):
        # Get the site (should be site with ID=1 based on settings.py)
        try:
            site = Site.objects.get(id=settings.SITE_ID)
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Site with ID {settings.SITE_ID} does not exist. Please run migrations first.')
            )
            return

        # Get client ID and secret from arguments or environment variables
        client_id = options.get('client_id') or settings.GOOGLE_OAUTH_CLIENT_ID if hasattr(settings, 'GOOGLE_OAUTH_CLIENT_ID') else None
        secret = options.get('secret') or settings.GOOGLE_OAUTH_SECRET if hasattr(settings, 'GOOGLE_OAUTH_SECRET') else None

        if not client_id or not secret:
            self.stdout.write(
                self.style.WARNING(
                    'Google OAuth credentials not provided.\n'
                    'Usage: python manage.py setup_google_oauth --client-id YOUR_CLIENT_ID --secret YOUR_SECRET\n'
                    'Or set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_SECRET in settings.py'
                )
            )
            return

        # Check if SocialApp already exists
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': secret,
            }
        )

        if not created:
            # Update existing app
            social_app.client_id = client_id
            social_app.secret = secret
            social_app.save()
            self.stdout.write(self.style.SUCCESS('Updated existing Google SocialApp'))
        else:
            self.stdout.write(self.style.SUCCESS('Created Google SocialApp'))

        # Add site to the social app if not already added
        if site not in social_app.sites.all():
            social_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f'Added site "{site.domain}" to Google SocialApp'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Site "{site.domain}" already associated with Google SocialApp'))

        self.stdout.write(
            self.style.SUCCESS(
                '\nGoogle OAuth setup complete!\n'
                'Make sure your Google OAuth credentials are configured in Google Cloud Console:\n'
                '1. Go to https://console.cloud.google.com/\n'
                '2. Create OAuth 2.0 Client ID\n'
                '3. Add authorized redirect URI: http://localhost:8000/accounts/google/login/callback/'
            )
        )

