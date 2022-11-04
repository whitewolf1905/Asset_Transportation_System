from django.urls import path
from . import views

urlpatterns = [
    path('rider_info/<int:rider_id>', views.shareRiderInfo),
    path('asset_request/<int:requester_id>', views.requesterAsset),
    path('matched_rider/<int:requester_id>', views.matchRequests),
    path('apply_request', views.applyRequest)
]
