from django.urls import path
from rider import views

urlpatterns = [
    path('rider/add_travel_info/', views.AddRiderTravelInfo.as_view()),
    path('rider/get_travel_info/', views.GetRiderTravelInfo.as_view()),
    path('rider/get_requests/', views.GetRiderTravelInfo.as_view())
]
