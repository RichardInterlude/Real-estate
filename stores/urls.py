from django.urls import path, include
from . views import * 

urlpatterns = [
    path('listings/',ListingsView.as_view()),
    path('listing/<str:slug>/',ListingView.as_view()),
    path('inquiry/<str:id>/',InquiryView.as_view()),
]
