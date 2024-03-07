from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework import status , permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from  medicines.forms import MedicineForm
from  medicines.models import Medicine
from .serializers import MedicineSerializer




@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_medicine(request):
    form = MedicineForm(request.POST)
    if form.is_valid():
        medicine = form.save()
        return Response({'id': medicine.id}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes((AllowAny,))
def list_medicines(request):
    medicines = Medicine.objects.all()
    serializer =MedicineSerializer(medicines, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    form = MedicineForm(request.data, instance=medicine)
    if form.is_valid():
        form.save()
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_medicine(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk)
    except Medicine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    medicine.delete()
    return Response("deleted successfully")


@api_view(['GET'])
@permission_classes((AllowAny,))
def search_medicines(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        medicines = Medicine.objects.filter(name__icontains=search_query)
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Please provide a search query"}, status=400)