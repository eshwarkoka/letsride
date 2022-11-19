from django.urls import path
from rider import views

urlpatterns = [
    path('add_travel_info', views.AddRiderTravelInfo.as_view()),
    path('get_travel_info', views.GetRiderTravelInfo.as_view()),
    path('get_requests', views.GetRiderTravelInfo.as_view())
]
