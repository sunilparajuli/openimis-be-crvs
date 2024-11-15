import requests
from django.conf import settings
import json
from uptime import uptime

def register_mediator():
    config = settings.OPENHIM_CONFIG
    auth = (config['username'], config['password'])
    headers = {'Content-Type': 'application/json'}

    # Define mediator registration details
    mediator_definition = {
        "urn": f"urn:mediator:{config['mediator_name']}",
        "version": "1.0.0",
        "name": config['mediator_name'],
        "description": "openIMIS-openCRVS-Mediator",
        "defaultChannelConfig": [
            {
                "name": "Default Channel",
                "urlPattern": "^/api/crvs/opencrvs.*",
                "routes": [
                    {
                        "name": "Primary Route",
                        "host": config['host'],
                        "path": "/api/opencrvs/",
                        "port": config['port'],
                        "primary": True,
                        "type": "http"
                    }
                ]
            }
        ],
        # Ensure at least one endpoint is defined
        "endpoints": [
            {
                "name": "Primary Endpoint",
                "host": config['host'],
                "path": "/api/crvs/opencrvs/",
                "port": config['port'],
                "primary": True,
                "type": "http"
            }
        ]
    }

    config = settings.OPENHIM_CONFIG
    response = requests.post(
        f"{config['url']}/mediators",
        auth=auth,
        headers=headers,
        data=json.dumps(mediator_definition),
        verify=config.get('verify_ssl', True)  # Use SSL config setting
    )

    # Check response and print for debugging
    if response.status_code in [200, 201]:  # Success codes
        print("Mediator registered successfully with OpenHIM!")
    else:
        print("Failed to register mediator:", response.status_code, response.text)


def send_heartbeat():
    """Sends a heartbeat signal to OpenHIM."""
    config = settings.OPENHIM_CONFIG
    auth = (config['username'], config['password'])
    headers = {'Content-Type': 'application/json'}
    body = {'uptime': uptime()}
    urn = f"urn:mediator:{config['mediator_name']}"
    mediators_url = f"{config['url']}/mediators/{urn}/heartbeat"
    print("mediator_url", mediators_url)
    response = requests.post(
        url=mediators_url,
        auth=auth,
        headers=headers,
        json=body,
        verify=False#config.get('verify_ssl', True)
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(f"Heartbeat unsuccessful, received status code: {response.status_code}")
    print("Heartbeat sent successfully!")