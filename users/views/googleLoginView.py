from django.shortcuts import redirect
from django.contrib import messages
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import oauth2_login


def google_login_wrapper(request):
    """
    Wrapper view for Google OAuth login that checks if SocialApp is configured.
    """
    try:
        # Check if Google SocialApp exists
        social_app = SocialApp.objects.get(provider='google')
        if not social_app.client_id or not social_app.secret:
            messages.error(
                request,
                'Google OAuth no está configurado correctamente. '
                'Por favor, contacte al administrador. GERR-001.'
            )
            print("Google OAuth no está configurado correctamente. corra el comando: python manage.py setup_google_oauth --client-id YOUR_ID --secret YOUR_SECRET")
            return redirect('login')
        
        # If everything is OK, proceed with the OAuth flow
        return oauth2_login(request)
    except SocialApp.DoesNotExist:
        messages.error(
            request,
            'Google OAuth no está configurado. '
            'Por favor, contacte al administrador. GERR-002'
        )
        print("Google OAuth no está configurado correctamente. corra el comando: python manage.py setup_google_oauth --client-id YOUR_ID --secret YOUR_SECRET")
        return redirect('login')

