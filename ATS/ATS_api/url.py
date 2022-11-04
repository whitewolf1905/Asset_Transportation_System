from django.urls import path
from . import views

urlpatterns = [
    path('rider_info/<int:rider_id>', views.share_rider_info),
    path('asset_request/<int:requester_id>', views.requester_asset),
    path('matched_rider/<int:requester_id>', views.match_requests),
    path('apply_request', views.apply_request)
]
