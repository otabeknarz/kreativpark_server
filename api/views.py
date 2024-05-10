import pytz
from core.models import People, QrCode, Data
from datetime import datetime, timedelta
from .serializers import PeopleSerializer, QrCodeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# APIs for people model
@api_view(["GET"])
def people_get(request):
    people = People.objects.all()
    serializer = PeopleSerializer(people, many=True)
    return Response({"people_count": people.count(), "people": serializer.data})


@api_view(["POST"])
def people_post(request):
    serializer = PeopleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def people_check(request, ID):
    try:
        people = People.objects.get(ID=ID)
    except People.DoesNotExist:
        return Response({"status": "false"})
    return Response(
        {
            "status": "true",
            "people": {
                "name": str(people.name),
                "ID": str(people.ID),
                "phone_number": str(people.phone_number),
                "created": str(people.created),
                "updated": str(people.updated),
            },
        }
    )


@api_view(["GET"])
def people_IDs(request):
    people = People.objects.values_list("ID", flat=True)
    return Response({"IDs": people})


# APIs for QrCode model
@api_view(["GET"])
def qrcode_get(request):
    qrcode = QrCode.objects.all()
    serializer = QrCodeSerializer(qrcode, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def qrcode_delete(request, user_ID):
    try:
        people = People.objects.get(ID=user_ID)
        qrcode = QrCode.objects.get(people=people)
    except:
        return Response({"status": "false"})
    image_path = qrcode.image_path
    qrcode.delete()
    return Response({"status": "true", "image_path": image_path})


@api_view(["POST"])
def qrcode_post(request):
    serializer = QrCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def qrcode_check(request, ID):
    try:
        qrcode = QrCode.objects.get(ID=ID)
    except QrCode.DoesNotExist:
        return Response({"status": "false"})
    return Response(
        {
            "status": "true",
            "qrcode": {
                "people": {"name": qrcode.people.name, "ID": str(qrcode.people.ID)},
                "ID": str(qrcode.ID),
                "created": str(qrcode.created),
                "type": str(qrcode.type),
                "purpose": str(qrcode.purpose),
                "image_path": str(qrcode.image_path),
            },
        }
    )


@api_view(["GET"])
def people_has_qrcode(request, people_id):
    try:
        people = People.objects.get(ID=people_id)
    except People.DoesNotExist:
        return Response({"status": "poeple does not exist"})
    try:
        qrcode = QrCode.objects.get(people=people)
    except QrCode.DoesNotExist:
        return Response({"status": "false"})
    return Response({"status": "true"})


@api_view(["GET"])
def login_library(request, qrcode_ID):
    try:
        qrcode = QrCode.objects.get(ID=qrcode_ID)
    except QrCode.DoesNotExist:
        return Response({"status": "false"})
    data = Data.objects.create(
        people=qrcode.people, purpose=qrcode.purpose, type=qrcode.type
    )
    qrcode.delete()
    return Response({"status": "true"})


# Functions for admins
@api_view(["GET"])
def stats(request, days):
    if days == 0:
        data = Data.objects.filter()
        people = People.objects.filter()
    else:
        ending_date = datetime.today()
        starting_date = ending_date - timedelta(days=days)
        data = Data.objects.filter(created__range=[starting_date, ending_date])
        people = People.objects.filter(created__range=[starting_date, ending_date])
    people_json = []
    data_json = {}
    for p in people:
        people_dict = {
            "ID": p.ID,
            "name": p.name,
            "phone_number": p.phone_number,
            "passport_data": p.passport_data,
            "created": str(p.created),
        }
        people_json.append(people_dict)

    data_types = {}

    for d in data:
        data_json["ID"] = d.pk
        data_json["people"] = d.people.ID
        data_json["purpose"] = d.purpose
        data_json["type"] = d.type
        data_json["created"] = str(d.created)
        if d.purpose != "":
            try:
                data_types[d.purpose] += 1
            except KeyError:
                data_types[d.purpose] = 1

    return Response(
        {
            "people_count": people.count(),
            "data_count_IN": data.filter(type="IN").count(),
            "data_count_OUT": data.filter(type="OUT").count(),
            "purposes": data_types,
            "people": people_json,
        }
    )
