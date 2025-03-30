from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import IndividualRegistrationSerializer, NGORegistrationSerializer
from .models import CustomUser

class IndividualRegistrationView(generics.CreateAPIView):
    serializer_class = IndividualRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            return Response({
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "user_type": user.user_type
                }
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "error": "Registration failed"
            }, status=status.HTTP_400_BAD_REQUEST)


class NGORegistrationView(generics.CreateAPIView):
    serializer_class = NGORegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Handle file upload separately
            verification_docs = request.FILES.get('verification_docs')
            if not verification_docs:
                return Response({
                    "success": False,
                    "message": "Verification documents are required"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            ngo_user = serializer.save(verification_docs=verification_docs)
            return Response({
                "success": True,
                "message": "NGO registration submitted for verification",
                "data": {
                    "org_name": ngo_user.ngo_profile.org_name,
                    "email": ngo_user.email,
                    "status": "Pending verification"
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "error": "NGO registration failed"
            }, status=status.HTTP_400_BAD_REQUEST)