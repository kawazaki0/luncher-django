from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", False)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "GOOGLE_ACCOUNT_ALLOW_REGISTRATION", False)

    def pre_social_login(self, request, sociallogin):
        email_domain = sociallogin.user.email.split('@')[1].lower()
        if email_domain not in settings.ALLOWED_EMAIL_DOMAINS:
            # TODO nice template
            raise ImmediateHttpResponse(HttpResponse(
                sociallogin.user.email + ' is not valid member of ' + str(
                    settings.ALLOWED_EMAIL_DOMAINS)))
