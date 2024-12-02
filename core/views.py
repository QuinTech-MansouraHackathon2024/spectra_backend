from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer
from .models import MedicalData, User
from .models import Doctor
from .serializers import DoctorSerializer
from .serializers import MedicalDataSerializer
class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


class DoctorListView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class MedicalDataDetailView(generics.RetrieveUpdateAPIView):
    queryset = MedicalData.objects.all()
    serializer_class = MedicalDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override this method to retrieve the medical data for the current user.
        """
        if self.request.user.medical_data is not None:
            return self.request.user.medical_data
        return "User has no medical data"


@api_view(['POST'])
def create_medical_data(request):
    user_id = request.user.id
    if user_id is None:
        return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "user": user_id,
        "test_results": request.data.get('test_results'),
        "A1": request.data.get('A1'),
        "A2": request.data.get('A2'),
        "A3": request.data.get('A3'),
        "A4": request.data.get('A4'),
        "A5": request.data.get('A5'),
        "A6": request.data.get('A6'),
        "A7": request.data.get('A7'),
        "A8": request.data.get('A8'),
        "A9": request.data.get('A9'),
        "A10": request.data.get('A10'),
        "additional_info": request.data.get('additional_info')
    }

    serializer = MedicalDataSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

