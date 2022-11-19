from django.urls import path
from requester import views

urlpatterns = [
    path('add_transport_request', views.AddRiderTravelInfo.as_view()),
    path('request_rider', views.GetRiderTravelInfo.as_view()),
    path('get_requests', views.GetRiderTravelInfo.as_view())
]
