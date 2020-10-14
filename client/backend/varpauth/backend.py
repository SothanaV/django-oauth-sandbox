from six.moves.urllib.parse import urljoin
from social_core.backends.oauth import BaseOAuth2
import requests
from django.conf import settings

class CustomOAuth2(BaseOAuth2):
    # name = settings.OAUTH_SERVER_NAME or 'custom'
    # AUTH_SERVER = settings.OAUTH_SERVER_BASEURL or 'auth.ei.team'
    # AUTHORIZATION_URL = 'https://{}/o/authorize'.format(AUTH_SERVER)
    # ACCESS_TOKEN_URL = 'https://{}/o/token/'.format(AUTH_SERVER)
    # REFRESH_TOKEN_URL = 'https://{}/o/token/'.format(AUTH_SERVER)
    # ACCESS_TOKEN_METHOD = 'POST'
    # REVOKE_TOKEN_METHOD = 'GET'
    # USER_DATA_URL = 'https://{}/api/me/'.format(AUTH_SERVER)
    name = settings.OAUTH_SERVER_NAME
    AUTH_SERVER = settings.OAUTH_SERVER_BASEURL
    AUTHORIZATION_URL = 'http://{}/o/authorize'.format(AUTH_SERVER)
    ACCESS_TOKEN_URL = 'http://{}/o/token/'.format(AUTH_SERVER)
    REFRESH_TOKEN_URL = 'http://{}/o/token/'.format(AUTH_SERVER)
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_METHOD = 'GET'
    USER_DATA_URL = 'http://{}/api/v1/profile/'.format(AUTH_SERVER)

    SCOPE_SEPARATOR = ' '
    EXTRA_DATA = [
        ('expires_in', 'expires_in'),
        ('refresh_token', 'refresh_token'),
        ('scope', 'scope'),
    ]

    def get_user_id(self, details, response):
        return details['username']

    def get_user_details(self, response):
        res = {'username': response.get('username'),
                    'email': response.get('email'),
                    'first_name': response.get('first_name'),
                    'last_name': response.get('last_name'),
                }
        return res

    def user_data(self, access_token, *args, **kwargs):
        data = self._user_data(access_token)
        return data
                        
    def _user_data(self, access_token, path=None):
        headers = {
            'Authorization': 'Bearer {0}'.format(access_token)
        }

        extra_data = requests.get(self.USER_DATA_URL, headers=headers)

        user_profile = extra_data.json()

        return user_profile
