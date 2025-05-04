from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, Kudo
from .serializers import UserSerializer, KudoSerializer, GiveKudoSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see others in their organization
        return self.queryset.filter(organization=self.request.user.organization)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class KudoViewSet(viewsets.ModelViewSet):
    queryset = Kudo.objects.all()
    serializer_class = KudoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see kudos they've given or received
        return self.queryset.filter(
            models.Q(from_user=self.request.user) | 
            models.Q(to_user=self.request.user)
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
