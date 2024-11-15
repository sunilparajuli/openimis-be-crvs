import requests
import logging
from .auth_token import get_opencrvs_auth_token
from requests.auth import HTTPBasicAuth
from django.conf import settings
# Constants
OPENHIM_MEDIATOR_URL = settings.OPENHIM_CONFIG.get('openhim_core_url') 

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def put_data_to_openhim_mediator(auth_token, data):
    """Send data to OpenHIM Mediator with provided auth token."""
    try:
        response = requests.post(
            OPENHIM_MEDIATOR_URL,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            }
        )
        if response.status_code != 200:
            logger.error(f"Failed response from OpenHIM Mediator: {response.status_code} - {response.text}")
            return None
        return response
    except requests.RequestException as error:
        logger.error(f"Request failed: {error}")
        return None

def put_data_to_openhim_mediator_with_token(data):
    """Get auth token and send data to OpenHIM Mediator."""
    auth_token = get_opencrvs_auth_token()
    if not auth_token:
        logger.error("Cannot create token")
        return None
    return put_data_to_openhim_mediator(auth_token, data)


def send_fhir_request_opencrvs_hearth_db(endpoint_path, data):
    """Send a request to OpenHIM FHIR endpoint with a specific path."""
    from django.conf import settings
    # Build the full URL by appending the endpoint path to the base OpenHIM FHIR URL
    url = f"{settings.OPENHIM_CONFIG['openhim_core_url']}/fhir"
    try:
        # Send a POST request to the OpenHIM FHIR endpoint
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth('test', 'test')
        )

        if response.status_code != 200:
            logger.error(f"Failed response from OpenHIM: {response.status_code} - {response.text}")
            return None

        logger.info("Data sent successfully to OpenHIM FHIR endpoint")
        return response.json()
    
    except requests.RequestException as error:
        logger.error(f"Request to OpenHIM FHIR endpoint failed: {error}")
        return None