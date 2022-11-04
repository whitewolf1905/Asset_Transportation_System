from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import RidersTravelInfo, RidersInfoSerializer, RequesterHistory, RequesterHistorySerializer



@api_view(['GET', 'POST'])
def shareRiderInfo(request, rider_id):
    if request.method == 'GET':
        riderDetail = RidersTravelInfo.objects.filter(riders_id=rider_id)

        if len(riderDetail):
            serialize_data = RidersInfoSerializer(riderDetail, many=True)
            return Response(serialize_data.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        rider_data = request.data
        rider_data["riders_id"] = rider_id
        RiderInfoData = RidersInfoSerializer(data=rider_data)

        if RiderInfoData.is_valid():
            RiderInfoData.save()
            return Response(RiderInfoData.data, status=status.HTTP_200_OK)

        return Response(RiderInfoData.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def requesterAsset(request, requester_id):
    if request.method == 'GET':
        requester_detail = RequesterHistory.objects.filter(requester_id=requester_id)

        if len(requester_detail):
            serialize_data = RequesterHistorySerializer(requester_detail, many=True)
            return Response(serialize_data.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        requester_data = request.data
        requester_data["requester_id"] = requester_id
        requesterInfoData = RequesterHistorySerializer(data=requester_data)

        if requesterInfoData.is_valid():
            requesterInfoData.save()
            return Response(requesterInfoData.data, status=status.HTTP_200_OK)

        return Response(requesterInfoData.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def matchRequests(request, requester_id):
    requester_detail = RequesterHistory.objects.filter(requester_id=requester_id,
                                                       transportation_status="NOT_APPLIED")

    if len(requester_detail):
        serialize_requester_data = RequesterHistorySerializer(requester_detail, many=True)
        # print(serialize_requester_data.data)
        matched_data = []
        for each in serialize_requester_data.data:
            print(each["pick_from"])
            rider_info = RidersTravelInfo.objects.filter(travel_from=each["pick_from"],
                                                         travel_to=each["deliver_to"],
                                                         travel_date=each["deliver_date"],
                                                         asset_quantity__gte=each["asset"])
            if len(rider_info):
                serialize_rider_info = RidersInfoSerializer(rider_info, many=True)

                if len(serialize_rider_info.data):
                    data = {
                        "Matched_Rider": serialize_rider_info.data[0]["riders_id"],
                        "Rider_row_id": serialize_rider_info.data[0]["id"],
                        "id": each["id"],
                        "pick_from": each["pick_from"],
                        "deliver_to": each["deliver_to"],
                        "deliver_date": each["deliver_date"],
                        "asset": each["asset"],
                        "asset_type": each["asset_type"],
                        "asset_sensitivity": each["asset_sensitivity"],
                        "transportation_status": each["transportation_status"]
                    }
                    matched_data.append(data)

        if len(matched_data):

            pagintor = Paginator(matched_data, 2)
            try:
                page_number = request.GET.get('page')
                page_obj = pagintor.page(page_number)
            except:
                page_obj = pagintor.page(1)

            data = {
                'count': len(matched_data),
                'previous_page': page_obj.has_previous() and page_obj.previous_page_number() or None,
                'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
                'data': list(page_obj)
            }
            return Response({"data": data}, status=status.HTTP_200_OK)

    return Response({"message": "No data matched"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def applyRequest(request):
    rider_row_id = request.data["rider_row_id"]
    requester_row_id = request.data["requester_row_id"]
    try:
        requester_info = RequesterHistory.objects.get(id=requester_row_id)
        rider_info = RidersTravelInfo.objects.get(id=rider_row_id)
        if requester_info.transportation_status == "APPLIED":
            return Response({"message": "Request already applied"}, status=status.HTTP_200_OK)
        rider_info.asset_quantity -= requester_info.asset
        rider_info.save()
        requester_info.transportation_status = "APPLIED"
        requester_info.save()
        return Response({"message": "Request Applied successfully"}, status=status.HTTP_200_OK)

    except:
        return Response({"message": "Couldn't apply the request"}, status=status.HTTP_400_BAD_REQUEST)
