from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Kudo
from .serializers import UserSerializer, KudoSerializer, GiveKudoSerializer
from rest_framework import permissions 
from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = []  # Remove TokenAuthentication
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Temporarily allow all users to be fetched for testing purposes
        return self.queryset

    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class KudoViewSet(viewsets.ModelViewSet):
    queryset = Kudo.objects.all()
    serializer_class = KudoSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = []  # Remove TokenAuthentication
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     print("Requesting user:", self.request.user)
    #     return self.queryset.filter(
    #         Q(from_user=self.request.user) | 
    #         Q(to_user=self.request.user)
    #     ).order_by('-created_at')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Kudo.objects.none()  # or return an empty queryset safely
        return self.queryset.filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)
        ).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def give_kudo(self, request):
        request.user.reset_kudos()
        
        if request.user.remaining_kudos <= 0:
            return Response(
                {"error": "You have no kudos remaining this week."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GiveKudoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_user = get_object_or_404(
            User, 
            id=serializer.validated_data['to_user_id'],
            organization=request.user.organization
        )

        if to_user == request.user:
            return Response(
                {"error": "You cannot give kudos to yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        kudo = Kudo.objects.create(
            from_user=request.user,
            to_user=to_user,
            message=serializer.validated_data['message']
        )

        request.user.remaining_kudos -= 1
        request.user.save()

        return Response(KudoSerializer(kudo).data, status=status.HTTP_201_CREATED)
