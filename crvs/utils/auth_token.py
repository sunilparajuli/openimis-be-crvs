import requests
import logging
from urllib.parse import urljoin
from django.conf import settings
# Constants
config = settings.OPENHIM_CONFIG

AUTH_URL = config.get('AUTH_URL')  
CLIENT_ID = config.get('CLIENT_ID')  
CLIENT_SECRET = config.get('CLIENT_SECRET')  

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def verify_opencrvs_auth_token(token):
    """Verify OpenCRVS auth token."""
    if not AUTH_URL:
        return True

    try:
        response = requests.post(
            urljoin(AUTH_URL, 'verifyToken'),
            data={'token': token},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response_data = response.json()
        return response_data.get('valid', False)
    except requests.RequestException as error:
        logger.error(f"Failed verifying token: {error}")
        return False

def get_opencrvs_auth_token():
    """Get OpenCRVS auth token."""
    token_endpoint = urljoin(AUTH_URL, 'token')
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(token_endpoint, json=payload, headers=headers)
        response_data = response.json()
        logger.info(f"This is the authToken request response: {response_data}")
        return response_data.get('access_token', '')
    except requests.RequestException as error:
        logger.error(f"Request failed: {error}")
        return ''
