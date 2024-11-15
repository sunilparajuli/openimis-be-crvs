
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
from crvs.utils.openhim_interceptor import send_fhir_request_opencrvs_hearth_db

class GetPatientAPIView(APIView):
    """
    API View to retrieve a patient from the OpenHIM FHIR endpoint.
    """
    def get(self, request, patient_id):
        endpoint_path = f"/fhir/Patient/{patient_id}"
        
        # Send the GET request to the OpenHIM FHIR endpoint
        response = send_fhir_request_opencrvs_hearth_db(endpoint_path, data={})
        
        # Handle the response
        if response is None:
            return Response(
                {'error': 'Failed to retrieve patient from OpenHIM'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(response, status=status.HTTP_200_OK)     


class PostOpenCrvsDataThroughOpenHIM(APIView):
    
    def post(self, request):
        print("request", request.data)
        return Response({}, status=status.HTTP_200_OK)     