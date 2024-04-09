from django.urls import path
from .views import user_registration,UserDetailsView,ReferralsView

urlpatterns = [
    path('register/', user_registration, name='user_registration'),
    path('user-details/', UserDetailsView.as_view(), name='user_details'),
    path('referrals/', ReferralsView.as_view(), name='referrals'),

]
