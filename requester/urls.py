from django.urls import path
from requester import views

urlpatterns = [
    path('add_transport_request', views.AddTransportRequest.as_view()),
    path('get_transport_requests', views.GetTransportRequests.as_view()),
    path('request_rider', views.RequestRider.as_view()),
]
