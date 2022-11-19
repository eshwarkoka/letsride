from django.urls import path
from rider import views

urlpatterns = [
    path('add_travel_info', views.AddRiderTravelInfo.as_view()),
    path('get_travel_info', views.GetRiderTravelInfo.as_view()),
    path('check_requests', views.CheckRequests.as_view()),
    path('update_request', views.UpdateRequest.as_view())
]
