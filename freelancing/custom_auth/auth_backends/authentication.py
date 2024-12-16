from rest_framework.authentication import TokenAuthentication

from freelancing.custom_auth.models import MultiToken


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiToken
