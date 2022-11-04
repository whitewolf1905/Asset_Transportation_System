from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import RidersTravelInfo, RidersInfoSerializer, RequesterHistory, RequesterHistorySerializer


@api_view(['GET', 'POST'])
def share_rider_info(request, rider_id):
    if request.method == 'GET':
        try:
            rider_detail = RidersTravelInfo.objects.filter(riders_id=rider_id)

            if len(rider_detail):
                serialize_data = RidersInfoSerializer(rider_detail, many=True)
                return Response(serialize_data.data, status=status.HTTP_200_OK)

            return Response({"message": "Rider not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_409_CONFLICT)

    elif request.method == 'POST':
        try:
            rider_data = request.data
            rider_data["riders_id"] = rider_id
            rider_info_data = RidersInfoSerializer(data=rider_data)

            if rider_info_data.is_valid():
                rider_info_data.save()
                return Response(rider_info_data.data, status=status.HTTP_200_OK)

            return Response(rider_info_data.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_409_CONFLICT)


@api_view(['GET', 'POST'])
def requester_asset(request, requester_id):
    if request.method == 'GET':
        try:
            requester_detail = RequesterHistory.objects.filter(requester_id=requester_id)

            if len(requester_detail):
                serialize_data = RequesterHistorySerializer(requester_detail, many=True)
                return Response(serialize_data.data, status=status.HTTP_200_OK)

            return Response({"message": "Requester not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_409_CONFLICT)

    elif request.method == 'POST':
        try:
            requester_data = request.data
            requester_data["requester_id"] = requester_id
            requester_info_data = RequesterHistorySerializer(data=requester_data)

            if requester_info_data.is_valid():
                requester_info_data.save()
                return Response(requester_info_data.data, status=status.HTTP_200_OK)

            return Response(requester_info_data.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_409_CONFLICT)



@api_view(['GET'])
def match_requests(request, requester_id):
    try:
        requester_detail = RequesterHistory.objects.filter(requester_id=requester_id,
                                                           transportation_status="NOT_APPLIED")

        if len(requester_detail):
            serialize_requester_data = RequesterHistorySerializer(requester_detail, many=True)
            # print(serialize_requester_data.data)
            matched_data = []
            for each in serialize_requester_data.data:
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

                paginator = Paginator(matched_data, 2)
                try:
                    page_number = request.GET.get('page')
                    page_obj = paginator.page(page_number)
                except:
                    page_obj = paginator.page(1)

                data = {
                    'count': len(matched_data),
                    'previous_page': page_obj.has_previous() and page_obj.previous_page_number() or None,
                    'next_page': page_obj.has_next() and page_obj.next_page_number() or None,
                    'data': list(page_obj)
                }
                return Response({"data": data}, status=status.HTTP_200_OK)

        return Response({"message": "No data matched"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def apply_request(request):
    try:
        rider_row_id = request.data["rider_row_id"]
        requester_row_id = request.data["requester_row_id"]

    except Exception as e:
        return Response({"message": "Id's not found"}, status=status.HTTP_204_NO_CONTENT)
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
