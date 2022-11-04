from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import RidersTravelInfo, RidersInfoSerializer, RequesterHistory, RequesterHistorySerializer


@api_view(('GET',))
def show(request):
    return Response({"data": "Random data"})


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
    requester_detail = RequesterHistory.objects.filter(requester_id=requester_id)

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
            return Response({"data": matched_data}, status=status.HTTP_200_OK)

    return Response({"message": "No data matched"}, status=status.HTTP_204_NO_CONTENT)

