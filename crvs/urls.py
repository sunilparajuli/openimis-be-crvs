from .views import *
from django.urls import path, include
from django.conf import settings



urlpatterns = [
    path('get-patient/<str:patient_id>/', GetPatientAPIView.as_view(), name='get_patient_api'),
]

urlpatterns+= [
    path('opencrvs/', PostOpenCrvsDataThroughOpenHIM.as_view(), name='opencrvs'),
]


if settings.DEBUG:
    urlpatterns += []
