from rest_framework.routers import DefaultRouter
from .views import RaffleConfigurationViewSet

router = DefaultRouter()
router.register(r'raffle', RaffleConfigurationViewSet, basename="raffle_configuration")

urlpatterns = router.urls
