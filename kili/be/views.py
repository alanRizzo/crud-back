from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import mixins
from .models import Client, CurrentAccount, Movement
from .serializers import ClientSerializer, CurrentAccountSerializer, MovementSerializer


class ClientViewSet(RetrieveAPIView):
    """
    A read only client retrieve view.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class AccountViewSet(ListAPIView):
    """
    A read only account per client retrieve view.
    """
    serializer_class = CurrentAccountSerializer

    def get_queryset(self):
        client = self.request.user.id
        return CurrentAccount.objects.filter(client_id=client)


class MovementViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Allows to read, update or create movements.
    """
    queryset = Movement.objects.filter()
    serializer_class = MovementSerializer
