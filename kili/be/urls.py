from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, AccountViewSet, MovementViewSet


urlpatterns = ([
    path('clients/<int:pk>/', ClientViewSet.as_view()),
    path('accounts/', AccountViewSet.as_view()),
    # path('movements/<int:pk>/', MovementViewSet.as_view())
])

router = DefaultRouter()
router.register('movements', MovementViewSet)
urlpatterns += router.urls
